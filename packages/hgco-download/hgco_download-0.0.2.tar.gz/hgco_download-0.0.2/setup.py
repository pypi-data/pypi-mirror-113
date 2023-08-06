from setuptools import find_packages, setup

setup(
    name="hgco_download",
    version="0.0.2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "hgco_download=hgco_download.download_cli:main",
        ]
    },
    install_requires=["hf-lfs"],
)

"""
python setup.py sdist bdist_wheel
twine upload dist/*
"""
