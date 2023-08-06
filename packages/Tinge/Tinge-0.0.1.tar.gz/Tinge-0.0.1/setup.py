import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

# with open("README.md") as file:
#     # README = (HERE / "README.md").read_bytes()
#     README = file.read()

README = '''
ANSII color formattion for terminal output
'''

setup(
    name="Tinge",
    version="0.0.1",
    description="Colored text for terminal",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/g-paras/tinge",
    author="Paras Gupta",
    author_email="guptaparas039@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    packages=["tinge"],
    install_requires=["colorama"],
)
