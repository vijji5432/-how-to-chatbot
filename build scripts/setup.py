from setuptools import setup, find_packages

setup(
    name="chatbot-docs-fetcher",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "flask",
        "openai",
        "langchain"
    ],
)
