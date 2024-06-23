from setuptools import setup

setup(
    name='gitman',
    version='0.1.2',
    py_modules=['src.main'],
    entry_points={
        'console_scripts': [
            'gitman = src.main:app',
        ],
    },
)
