import setuptools

setuptools.setup(
    name="request-time-tracker",
    version="0.0.5",
    author="Roman Karpovich",
    author_email="roman@razortheory.com",
    description="Requests time tracker from being captured by proxy (e.g. nginx) till being executed by django",
    long_description="i will update readme with more info. honestly. bit later",
    long_description_content_type="text/markdown",
    url="https://github.com/razortheory/request-time-tracker",
    project_urls={
        "Bug Tracker": "https://github.com/razortheory/request-time-tracker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)