import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paginator.py",
    version="0.2",
    author="Flampt",
    license="MIT",
    description="Simple to use discord paginator for messages and embeds with reactions and buttons.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FlamptX/paginator.py",
    project_urls={
        "Source": "https://github.com/FlamptX/paginator.py",
        "Documentation": "https://gitbook.com"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=['aiohttp', 'discord.py', 'asyncio', 'discord-components'],
    keywords='discord paginator discord-paginator',
    packages=setuptools.find_packages(include=['paginator', 'paginator.*']),
    python_requires=">=3.6",
)