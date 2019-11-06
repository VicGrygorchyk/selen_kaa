from setuptools import setup, find_packages


def get_requirements():
    """Reads the installation requirements from requirements.pip"""
    with open("requirements.pip") as reqfile:
        return [line for line in reqfile.read().split("\n") if not line.startswith(('#', '-'))]


def get_test_requirements():
    """Reads the installation requirements for tests"""
    with open("test-requirements.pip") as test_reqfile:
        return [line for line in test_reqfile.read().split("\n") if not line.startswith(('#', '-'))]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="selen-kaa",
    version="0.0.1",
    author="Viktor Grygorchuk",
    author_email="vvgrygorchuk@gmail.com",
    description="A lightweight wrapper around Selenium python repo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    test_suite="tests",
    tests_require=get_test_requirements()
)
