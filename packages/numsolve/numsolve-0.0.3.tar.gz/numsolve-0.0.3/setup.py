from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="numsolve",
    version='0.0.3',
    description="Numerical Methods to solve various equation",
    long_description_content_type='text/markdown',
    long_description=long_description,
    keywords=['python', 'numerical methods', 'equation solver'],
    author="Harshal Dupare",
    author_email="<harshal3hd@gmail.com>",
    install_requires=['numpy'],
    py_modules=['numsolve'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={'': "src"},
    python_requires=">=3.6",
)