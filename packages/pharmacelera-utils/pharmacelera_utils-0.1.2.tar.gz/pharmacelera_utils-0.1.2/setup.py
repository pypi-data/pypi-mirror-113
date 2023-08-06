from setuptools import setup, find_packages

setup(
    name="pharmacelera_utils",
    version="0.1.2",
    description="Pharmacelera script to execute experiments",
    url="https://bitbucket.org/pharmacelera/pharmqsar-examples.git",
    author="Pharmacelera developers",
    author_email="info@pharmacelera.com",
    license="Mozilla Public License Version 2.0",
    packages=find_packages(),
    install_requires=[
        "requests==2.25.1",
        "PyYAML==5.4.1",
        "boto3==1.17.76"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=[
        "launch",
        "services",
        "utils",
        "__init__",
    ],
    package_dir={"": "src"},
    entry_points={"console_scripts": ["pharmacelera-launch=src.launch:run"]},

)