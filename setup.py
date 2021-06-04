from setuptools import find_packages, setup

PACKAGE_NAME = "fsm"


setup(
    name=PACKAGE_NAME,
    version="1.0",
    description="Package containing finite state machine",
    author="David Alvarez Lombardi",
    author_email="alvarezdqal@gmail.com",
    url="https://github.com/alvarezdqal/fsm",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
