import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="L-System-Visualizer",
    version="1.0.0",
    author="Team BRAWT",
    author_email="lbones1@gulls.salisbury.edu",
    keywords="pyside2 qt5 lsystem",
    description="Generates visualizations of L Systems after a certain number of productions.",
    url="https://github.com/wrathofrathma/L-System-Visualizer.git",
    license="Unknown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Licence::TBD::TBD"
        "Operating System::OS Independent"
    ],
    install_requires=["pyside2", "matplotlib", "numpy", "Pillow", "PyGLM", "PyOpenGL", "pyparsing", "pyqtgraph", "scipy", "pyscreenshot"],
    py_modules=['lsystem'],
    python_requires='>=3.7',
    package_data={
      "": ["*.json"]
      },
    include_package_data=True
)
