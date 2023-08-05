import unames
from setuptools import find_packages, setup

DEPENDENCIES = []

# The text of the README file
with open('README.md') as f:
    README = f.read()

setup(
    name=unames.__title__,
    version=unames.__version__,
    packages=find_packages(include=[f"{unames.__title__}"]),
    description='Generate username from the full name provided',
    url="https://github.com/chankruze/unames",
    long_description=README,
    long_description_content_type="text/markdown",
    author=unames.__author__,
    author_email=unames.__author_email__,
    classifiers=[
        f"License :: OSI Approved :: {unames.__license__}",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=DEPENDENCIES,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
