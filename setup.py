from setuptools import setup, find_packages

setup(
    name="telegraf",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.9.1",
        "python-dotenv==1.0.0",
        "flask==3.0.2",
        "schedule==1.2.1",
    ],
    python_requires=">=3.13",
) 