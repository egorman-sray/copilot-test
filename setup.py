from setuptools import setup, find_packages

setup(
    name="entity-resolver",
    version="0.1.0",
    description="CLI tool to resolve company entity identifiers",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-mock>=3.11.0",
            "responses>=0.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "resolve-entity=entity_resolver.cli:main",
        ],
    },
    python_requires=">=3.8",
)
