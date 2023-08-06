import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="berre_deneme",
    version="0.0.1",
    author="berre",
    author_email="berre@gmailc.om",
    packages=["berre_deneme"],
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/gituser/test-tackage",
    license='MIT',
    python_requires='>=2',
    install_requires=[]
)