from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2"]

setup(
    name="xignitegh",
    version="0.0.2",
    author="Kapitalisman",
    author_email="hallo@kapitalisman.nl",
    license="MIT",
    description="A wrapper to the XigniteGlobalHistorical API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/xignite-python/xignitegh",
    python_requires=">=3",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="xignite api wrapper",
)
