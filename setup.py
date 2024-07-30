# For installing the local package in virtual environment

from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Ajay Kumar',
    author_email='ajayetw2009@gmail.com',
    packages=find_packages(),
    install_requires=[
        "openai",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ]
)

