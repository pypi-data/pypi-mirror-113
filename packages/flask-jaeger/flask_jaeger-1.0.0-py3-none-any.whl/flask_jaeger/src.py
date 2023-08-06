# -*- coding: utf8 -*-
import functools
import inspect
import logging
import opentracing
import time
from flask import _app_ctx_stack, request
from jaeger_client import Config, codecs
from opentracing import tags
from typing import Dict

from flask_jaeger.constants import CUSTOM_TRACE_ID, JAEGER_TRACE_ID

logger = logging.getLogger('flask-jaeger')


# ####################
# 注意, 一共有两种id，trace_id和x-trace-id
# trace_id为自定义的，可直接搜索
# x-trace-id为用来链接多个请求在一个栈的
# ####################


def get_custom_trace_id(default="unknown") -> str:
    """
    获取自定义的trace_id value.
    :param default:
    :return:
    """
    return request.form.get(CUSTOM_TRACE_ID) or \
           request.args.get(CUSTOM_TRACE_ID) or \
           request.headers.get(CUSTOM_TRACE_ID) or \
           (request.json or {}).get(CUSTOM_TRACE_ID) or default


class FlaskJaeger(object):
    def __init__(self, app=None):
        self.app = app

        self.tracer = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = Config(config={
            # 为 jaeger 的 traceid
            'trace_id_header': JAEGER_TRACE_ID,
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': app.config.get('JAEGER_HOST', '127.0.0.1'),
                'reporting_port': app.config.get('JAEGER_PORT', '5775'),
            },
            'logging': True,
        },
            service_name=app.config.get('SERVICE_NAME', 'without_service_name'),
            validate=True
        )
        self.tracer = config.initialize_tracer()

        # app.teardown_appcontext(self.teardown)

        @app.after_request
        def end_trace(response):
            ctx = _app_ctx_stack.top
            if hasattr(ctx, 'jaeger_trace_id'):
                response.headers[JAEGER_TRACE_ID] = ctx.jaeger_trace_id
                return response
            elif hasattr(ctx, 'trace_stack') and ctx.trace_stack:
                c = ctx.trace_stack[-1]
                final_trace_id = codecs.span_context_to_string(
                    trace_id=c.trace_id, span_id=c.span_id,
                    parent_id=c.parent_id, flags=c.flags
                )
                response.headers[JAEGER_TRACE_ID] = final_trace_id
                return response
            else:
                return response

    # def teardown(self, exception):
    #     ctx = _app_ctx_stack.top
    #     if hasattr(ctx, 'trace_stack'):
    #         del ctx.trace_stack

    def _check_is_in_context(self) -> bool:
        try:
            _ = request.remote_addr
            return True
        except RuntimeError:
            return False

    def get_jaeger_ctx_from_other_requ(self):
        for payload in (
                request.headers,
                request.form.to_dict(),
                request.args.to_dict(),
                (request.json or {})
        ):
            span_ctx = self.tracer.extract(opentracing.Format.HTTP_HEADERS, payload)
            if span_ctx:
                return span_ctx

    def trace_info(self, func_name: str, info: Dict, trace_start_time: float, trace_end_time: float):
        # tracer not init.
        if not self.tracer:
            logger.warning('tracer not init.')
            return
        # check RuntimeError: Working outside of request context.
        if not self._check_is_in_context():
            logger.warning('tracer not in flask context.')
            return

        ctx = _app_ctx_stack.top
        if not ctx:
            return
        if not hasattr(ctx, "trace_stack"):
            ctx.trace_stack = []
            try:
                span_ctx = self.get_jaeger_ctx_from_other_requ()
                if span_ctx:
                    ctx.jaeger_trace_id = codecs.span_context_to_string(
                        trace_id=span_ctx.trace_id, span_id=span_ctx.span_id,
                        parent_id=span_ctx.parent_id, flags=span_ctx.flags
                    )
                    ctx.trace_stack = [span_ctx]
            except (opentracing.InvalidCarrierException,
                    opentracing.SpanContextCorruptedException):
                pass
        if ctx.trace_stack:
            last_span = ctx.trace_stack[-1]
        else:
            last_span = None
        # Notice: the result express like algo -> route. not route -> algo
        # if you want to modify it, notice here.
        span = self.tracer.start_span(func_name, child_of=last_span, start_time=trace_start_time)
        span.log_kv(info)
        span.set_tag(CUSTOM_TRACE_ID, get_custom_trace_id())
        # span.set_tag(tags.HTTP_METHOD, request.method)
        span.set_tag(tags.HTTP_URL, request.base_url)
        # span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
        span.set_tag('remote_addr', request.remote_addr)
        span.set_tag('endpoint', request.endpoint)
        span.finish(finish_time=trace_end_time)
        ctx.trace_stack.append(span)

    def log_decorator(self, trace_info: Dict):
        trace_info = trace_info or {}

        def wrapper_func(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    is_method = inspect.getfullargspec(func)[0][0] == 'self'
                    name = f'{func.__module__}.{args[0].__class__.__name__}.{func.__name__}'
                except:
                    is_method = False
                    name = f'{func.__module__}.{func.__name__}'
                start_time = time.time()
                func_result = func(*args, **kwargs)
                end_time = time.time()
                trace_info.update({"func_cost_time": f'{end_time - start_time}(s)'})

                self.trace_info(func_name=name, info=trace_info, trace_start_time=start_time, trace_end_time=end_time)

                return func_result

            return wrapper

        return wrapper_func
