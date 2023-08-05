# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='lms-id-generator',
    version='0.0.2',
    packages=find_packages(exclude=("tests",)),
    url='https://github.com/WisdomGardenInc/lms-id-generator',
    description='ID generator for lms',
    author='ZhangJianli',
    author_email='zhangjianli@wisdomgarden.com',
    license='',
    keywords=['lms'],
    classifiers=['Programming Language :: Python :: 3.6'],
    project_urls={
        'Bug Reports': 'https://github.com/WisdomGardenInc/lms-id-generator/issues',
        'Source': 'https://github.com/WisdomGardenInc/lms-id-generator',
    },
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-xprocess",
    ],
    zip_safe=True
)