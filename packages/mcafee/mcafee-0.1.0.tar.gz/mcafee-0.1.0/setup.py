import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mcafee",
    version="0.1.0",
    author="Yuval Adam",
    author_email="_@yuv.al",
    description="Number four automated fee manager script in all of Kazakhstan.",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuvadm/mcafee",
    project_urls={
        "Bug Tracker": "https://github.com/yuvadm/mcafee/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    packages=setuptools.find_packages(exclude="tests"),
    python_requires=">=3.6",
    install_requires=["lndgrpc", "click"],
    entry_points={
        "console_scripts": [
            "mcafee = mcafee:cli",
        ]
    },
)
