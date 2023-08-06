from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="sweet.client",
    version="0.0.0.1",
    author="tonglei",
    author_email="tonglei@qq.com",
    description="Sweet's client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sweeterio/client",
    packages=['sweetclient'],
    package_data={'.': ['*.py']},
    install_requires=[
    ],        
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)