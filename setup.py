import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deep_doc-ciprian15", # Replace with your own username
    version="0.0.1",
    author="Ciprian Talmacel",
    author_email="ciprian.talmacel15@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ciprian15/DeepDoc",
    packages=setuptools.find_packages("./src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)