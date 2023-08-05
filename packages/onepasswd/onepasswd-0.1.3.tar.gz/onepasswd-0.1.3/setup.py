import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onepasswd",
    version="0.1.3",
    author="agfn",
    author_email="lavender.tree9988@gmail.com",
    description="onepasswd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agfn/onepasswd",
    project_urls={
        "Bug Tracker": "https://github.com/agfn/onepasswd/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points='''
    [console_scripts]
        onepasswd=onepasswd.client:main
        onepasswd-upgrade=onepasswd.tools.upgrade:main
        onepasswd-merge=onepasswd.tools.jmerge:main
        onepasswd-diff=onepasswd.tools.jdiff:main
    '''
)
