from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="erp-system",
    version="1.0.0",
    author="ERP Development Team",
    description="Professional Accounting + POS + Inventory System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aminrx86/erp-system",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Business/Enterprise",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.13",
    install_requires=requirements,
)
