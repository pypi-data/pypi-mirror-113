from setuptools import setup

def readme():
    
    with open("README.md") as f:
        README = f.read()
        
    return README


setup(
    
    name = "bidamic-challenge",
    version="1.0.1",
    description = "A python package for calculating ROAS",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelQuant4R/bidamic_test_1",
    author="Michael S. Russell",
    author_email="michael.r2014@yahoo.co.uk",
    license="MIT",
    classifiers=[
        
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
        
    ],
    packages = ["bidamic"],
    include_package_data = True,
    install_requires=["numpy", "pandas"]

)
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
