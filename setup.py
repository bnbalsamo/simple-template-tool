from setuptools import setup, find_packages


# Provided Package Metadata
NAME = "simple-template-tool"
DESCRIPTION = "A simple tool for rendering templates."
VERSION = "0.0.1"
AUTHOR = "Brian Balsamo"
AUTHOR_EMAIL = "Brian@BrianBalsamo.com"
URL = 'https://github.com/bnbalsamo/simple-template-tool'
PYTHON_REQUIRES= ">=3.6,<4"
INSTALL_REQUIRES = [
    "click",
    "jinja2",
]
EXTRAS_REQUIRE = {
    "dev": [
        "bump2version",
        "invoke",
        "isort[pyproject] >= 5.0.0",
        "pylint >= 2.6.0",
        "black",
        "wheel",
        "pep517",
        "twine",
        "blacken-docs",
    ],
    "tests": [
        "tox",
        "tox-pyenv",
        "pytest",
        "coverage[toml]",
        "pytest-cov",
    ],
    "docs": [
        "sphinx",
        "sphinx_rtd_theme",
    ]
}
ENTRY_POINTS = {
    'console_scripts': ['stt=simple_template_tool:cli'],
}


def readme():
    try:
        with open("README.md", 'r') as f:
            return f.read()
    except:
        return False


# Derived Package Metadata
LONG_DESCRIPTION = readme() or DESCRIPTION
if LONG_DESCRIPTION == DESCRIPTION:
    LONG_DESCRIPTION_CONTENT_TYPE = "text/plain"
else:
    LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"


# Set it up!
setup(
    name=NAME,
    description=DESCRIPTION,
    version=VERSION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    package_dir={"": "src"},
    packages=find_packages(
        where="src"
    ),
    entry_points=ENTRY_POINTS,
    include_package_data=True,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=PYTHON_REQUIRES
)
