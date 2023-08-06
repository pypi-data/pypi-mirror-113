import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Setting up
setuptools.setup(
        name="dswPY", 
        version='0.0.1',
        author="Trevor Olsen",
        author_email="<trevorlewisolsen@gmail.com>",
        license='LICENSE.txt',
        description='wrapper utilities',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/trevorlolsen/dsw",
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        classifiers= [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        packages=setuptools.find_packages(),
        python_requires=">=3.8",
)