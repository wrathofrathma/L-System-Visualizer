import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="L-System-Visualizer",
    version="1.0.0",
    author="Team BRAWT",
    author_email="lbones1@gulls.salisbury.edu",
    description="Generates visualizations of L Systems after a certain number of productions.",
    url="https://github.com/wrathofrathma/L-System-Visualizer.git",
    license="Unknown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Licence::TBD::TBD"
        "Operating System::OS Independent"
    ],
    python_requires='>=3.7',
)
