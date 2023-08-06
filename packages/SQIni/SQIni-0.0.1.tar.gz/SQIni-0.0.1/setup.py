from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = 'connect table settings of a sqlite database with a ini file for better editing '
LONG_DESCRIPTION = 'connect table settings of a sqlite database with a ini file for better editing '

# Setting up
setup(
    name="SQIni",
    version=VERSION,
    author="Miku",
    license='MIT',
    description=DESCRIPTION,
    url='https://github.com/princessmiku/SQIni',
    install_requires=[],
    keywords=['python', 'sqlite3', 'sqlite', 'ini'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={'':'sqini/'},
)