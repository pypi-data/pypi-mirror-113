from setuptools import setup, find_packages

setup(
    name="pharmacelera_utils",
    version="0.1.0",
    description="Utility functions to execute pharmacelera scripts",
    url="https://bitbucket.org/pharmacelera/pharmqsar-examples.git",
    author="Pharmacelera developers",
    author_email="info@pharmacelera.com",
    license="Mozilla Public License Version 2.0",
    packages=find_packages(where="src"),
    install_requires=[
        "requests",
        "PyYAML",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["utils", "services"],
    package_dir={"": "src"},
)