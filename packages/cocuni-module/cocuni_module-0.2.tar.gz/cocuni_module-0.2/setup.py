import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = ['requests']

setuptools.setup(
    name="cocuni_module",
    version="0.2",
    author="Jorge Riveros",
    author_email="christian.riveros@outlook.com",
    license='MIT',
    description='A Python package for cocuni random numbers generation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cocuni80/package",
    packages=['cocunimodule'],
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
