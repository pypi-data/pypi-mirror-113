import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlp_tracking",
    version="0.0.2",
    author="hazoth, LowinLi",
    author_email="hazoth@hotmail.com, idealway9@gmail.com",
    description="mlp_tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["confluent_kafka==1.7.0", "ml_platform_client>=0.3.18.5"],
    keywords="kafka issue tracking",
)
