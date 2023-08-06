import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    _description = f.read()

setuptools.setup(
    name="pilmoji_fixed",
    version="1.3.2",
    author="jay3332 (fix by stunnerr)",
    description="Pilmoji is a fast and reliable emoji renderer for PIL.",
    long_description=_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stunnerr/pilmoji",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
        "pillow",
        "emoji",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
