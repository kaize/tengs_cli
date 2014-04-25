from setuptools import setup

setup(
    name='tengs_cli',
    version='0.0.1',
    # packages=['towelstuff',],
    license='MIT',
    long_description=open('README.txt').read(),
    install_requires=[
        'pyyaml',
        'requests'
    ],
    entry_points = {
        'console_scripts': ['tengs=tengs_cli.cli:main'],
    }
)
