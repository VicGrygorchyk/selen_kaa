from setuptools import setup, find_packages


def get_requirements():
    """Reads the installation requirements from requirements.pip"""
    with open("requirements.pip") as reqfile:
        return [line for line in reqfile.read().split("\n") if not line.startswith(('#', '-'))]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="selen-kaa",
    version="0.0.2",
    author="Viktor Grygorchuk",
    author_email="vvgrygorchuk@gmail.com",
    keywords=['Selenium', 'Test Automation'],
    description="A lightweight wrapper around Selenium python repo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VicGrygorchyk/selen_kaa.git",
    download_url="https://github.com/VicGrygorchyk/selen_kaa/archive/0.0.2.tar.gz",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "test*"]),
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing"
    ],
    python_requires='>=3.6',
)
