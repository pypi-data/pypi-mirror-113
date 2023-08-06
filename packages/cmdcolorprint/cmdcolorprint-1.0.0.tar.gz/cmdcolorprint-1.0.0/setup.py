import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmdcolorprint", # Replace with your own username
    version="1.0.0",
    entry_points={
        'console_scripts': [
            'cprint=colorprint:cprint',
        ],
    },
    author="Columba_Karasu",
    description="cmd color print",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hashibutogarasu/cprint",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.5',
)

