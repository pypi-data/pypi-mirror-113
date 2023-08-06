import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parallel-feature-selector",
    version="0.1.1",
    author="haeren",
    author_email="erenhalp@gmail.com",
    description="Package for parallelized feature selection methods",
    url="https://github.com/haeren/parallel-feature-selector",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["parallel_feature_selector"],
    package_dir={'':'parallel_feature_selector/src'},
    install_requires=[
        "pandas",
        "scikit-learn",
        "mpi4py",
        "arff2pandas",
        "openpyxl"
    ]
)