from distutils.core import setup

setup(
    name='dq',
    version='0.1.2',
    author='Michael Lamb',
    author_email='mr.lamby@gmail.com',
    packages=['dq', 'dq.test'],
    scripts=['bin/dq.py'],
    url='https://github.com/mlamby/dq',
    license='LICENSE.txt',
    description='Python Simple Data Query',
    long_description=open('README.md').read())
