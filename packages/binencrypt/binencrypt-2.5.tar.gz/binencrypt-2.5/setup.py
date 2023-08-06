from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "2.5"
DESCRIPTION = 'FILE ENCRYPTION EXEC'
LONG_DESCRIPTION = 'BINENCRYPT'

# Setting up
setup(
    name="binencrypt",
    version=VERSION,
    author="K.A.ISHAN OSHADA",
    author_email="<ic31908@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['binencrypt.crypter()','encrypt()','binencrypt.crypter_V2()','encrypt()','decrypt()'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
