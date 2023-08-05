import setuptools

# Package meta-data.
with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('LICENSE') as f:
    license = f.read()

NAME = 'rmti'
DESCRIPTION = 'An AI application that determines your Myers-Briggs Type Indicator.'
URL = 'https://github.com/jonwilami323/RedditAPI'
EMAIL = 'jonwiljunkmail@gmail.com'
AUTHOR = 'Jonathan Wilson'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0dev'
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/jonwilami323/RedditAPI/issues",
    "Source Code": "https://github.com/jonwilami323/RedditAPI",
}
REQUIRED = [
    # 'praw', 'numpy', 'pandas', 'scipy',
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    license=license,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    install_requires=REQUIRED,
    project_urls=PROJECT_URLS,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "rmti"},
    packages=setuptools.find_packages(where="rmti"),
    python_requires=">=3.6",
)

