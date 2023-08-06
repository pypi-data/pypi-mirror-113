from setuptools import setup, find_packages

setup(
    name="hgco_download",
    version="0.0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "hgco_download=hgco_download.download_cli:main",
        ]
    },
)

"""
python setup.py sdist bdist_wheel
twine upload dist/*
"""
