from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="invoice-extractor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A robust PDF invoice extraction system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/invoice-extractor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyMuPDF>=1.23.8",
        "paddlepaddle>=2.5.2",
        "paddleocr>=2.7.0.3",
        "pandas>=2.1.4",
        "tabulate>=0.9.0",
        "click>=8.1.7",
        "joblib>=1.3.2",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "invoice-extractor=invoice_extractor.cli:cli",
        ],
    },
) 