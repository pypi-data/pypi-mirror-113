import setuptools
import os
print(os.system('dir'))
with open('readme.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name = "pyco",
    version = "1.0.0",
    author = "Duplexes",
    maintainer = "LemonPi314",
    author_email = "no@email.com",
    description = "Colorized console printing and input, ANSI escape codes, and logging functions.",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Duplexes/pyco',
    keywords=['console', 'terminal', 'ansi', 'color', 'logging'],
    license = "MIT",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    packages = setuptools.find_packages(),
    python_requires = '>=3.6.8'
)
