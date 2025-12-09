from setuptools import setup, find_packages

setup(
    name="pte-mocktest",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "httpx",
    ],
    python_requires=">=3.8",
) 