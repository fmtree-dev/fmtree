import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fmtree",
    version="0.0.9",
    author="Huakun Shen",
    author_email="huakun.shen@huakunshen.com",
    description="Scrape File System and output in different formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fmtree-dev/fmtree",
    project_urls={
        "Bug Tracker": "https://github.com/fmtree-dev/fmtree/issues",
        "Documentation": "https://fmtree-dev.github.io/fmtree/"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pathlib2==2.3.5',
        'Jinja2==2.11.3'
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    package_data={
        'fmtree': [
            "visualizer/template/*",
            "visualizer/template/assets/*",
        ]
    }
)

# python -m build
# python -m twine upload dist/* --verbose --repository testpypi
