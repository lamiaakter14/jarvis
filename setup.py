"""Setup configuration for JARVIS monorepo."""
from setuptools import setup, find_packages

setup(
    name="jarvis",
    version="1.0.0",
    description="JARVIS: A Learning Operating System for Human Intelligence Amplification",
    author="Your Name",
    author_email="youremail@example.com",
    license="MIT",
    packages=find_packages(where="packages") + find_packages(where="apps/api") + find_packages(where="apps/cli"),
    package_dir={
        "": "packages",
        "jarvis_api": "apps/api/jarvis_api",
        "jarvis_cli": "apps/cli/jarvis_cli",
    },
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "openai",
        "langchain",
        "python-decouple",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "requests",
        "typer>=0.9.0",
        "rich>=13.0.0",
        "tqdm",
        "numpy",
        "scikit-learn",
        "pandas",
        "pyyaml",
        "flask",
        "markdown",
        "dependency-injector>=4.41.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "flake8",
            "black",
            "mypy",
            "isort",
        ],
    },
    entry_points={
        "console_scripts": [
            "jarvis-cli=jarvis_cli.main:app",
        ],
    },
)
