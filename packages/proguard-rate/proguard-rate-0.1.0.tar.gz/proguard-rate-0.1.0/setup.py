import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proguard-rate",
    version="0.1.0",
    author="weidongjian",
    author_email="weidongjian@gmail.com",
    description="计算代码混淆率",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weidongjian/proguardRate",
    project_urls={
        "Bug Tracker": "https://github.com/weidongjian/proguardRate/issues",
    },
    entry_points={
        "console_scripts": [
            "calRate=proguard:calrate"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "proguard"},
    packages=setuptools.find_packages(where="proguard"),
    python_requires=">=3.6",
)
