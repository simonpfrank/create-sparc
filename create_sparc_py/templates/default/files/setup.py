from setuptools import setup, find_packages

setup(
    name="{{project_name}}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    author="{{author}}",
    author_email="your.email@example.com",
    description="{{project_description}}",
    keywords="{{project_name}}, python",
    url="",  # Project home page
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: {{license}} License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
