import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FruitScript",
    version="1.0.0",
    author="Fruitsy",
    description="FruitScript is a module with multiple purposes, file management, on the spot being able to use things and maybe a bunch of useless shit that you don't need, lol. 😀",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ItzBlueBerries/FruitScript",
    project_urls={
        "Bug Tracker": "https://github.com/ItzBlueBerries/FruitScript/issues",
        "Pull Requests": "https://github.com/ItzBlueBerries/FruitScript/pulls",
        "Forks": "https://github.com/ItzBlueBerries/FruitScript/network/members"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['ext'],
    install_requires=[],
    python_requires=">=3.6",
)