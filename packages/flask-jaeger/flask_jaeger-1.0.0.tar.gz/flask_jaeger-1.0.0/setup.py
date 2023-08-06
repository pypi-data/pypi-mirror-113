from setuptools import setup


def read():
    with open("./requirements.txt", "r") as f:
        return f.readlines()


setup(
    name='flask_jaeger',
    version='1.0.0',
    packages=['flask_jaeger', ],
    url='',
    license='',
    author='yuzhang',
    author_email='geasyheart@163.com',
    description='flask jaeger',
    install_requires=read()
)
