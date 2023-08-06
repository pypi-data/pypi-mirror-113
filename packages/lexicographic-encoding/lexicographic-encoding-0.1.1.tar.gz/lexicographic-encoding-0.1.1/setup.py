import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lexicographic-encoding",
    version="0.1.1",
    author="Dario Balboni",
    author_email="dario.balboni.96+lexenc@gmail.com",
    description="Encode tuples of primitive types into bytestrings preserving the lexicographic order",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dlnet/lexicographic-encoding.git",
    packages=["lexicographic_encoding"],
    zip_safe=False,
    test_suite="nose2.collector.collector",
    tests_require=["nose2"],
    include_package_data=True,
    license="GPL-3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)
