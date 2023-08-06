import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proguard_rate",
    version="0.0.8",
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
            "calRate=proguard_rate:cal_rate"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "proguard_rate"},
    packages=setuptools.find_packages(where="proguard_rate"),
    python_requires=">=3.6",
)
