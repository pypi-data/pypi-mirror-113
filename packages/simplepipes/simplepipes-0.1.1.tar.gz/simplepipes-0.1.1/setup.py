from setuptools import setup

setup(
    name="simplepipes",
    version="0.1.1",    
    description="A python library to interact with other programming languages that support the simplepipes project.",
    url="https://github.com/Matthias1590/SimplePipes",
    author="Matthias Wijnsma",
    author_email="matthiasx95@gmail.com",
    license="MIT",
    packages=["simplepipes"],
    install_requires=["typing",
                      ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
)