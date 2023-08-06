import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="renderbox",
    version="0.0.2",
    author="Rajiv Sharma",
    author_email="rajiv.vfx@gmail.com",
    description="Artificial Intelligence Render Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vfxpipeline/renderbox",
    project_urls={
        "Bug Tracker": "https://github.com/vfxpipeline/renderbox/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)