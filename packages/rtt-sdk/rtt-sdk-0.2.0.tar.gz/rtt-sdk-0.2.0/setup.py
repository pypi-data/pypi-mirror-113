import setuptools


def get_version():
    with open("rtt_sdk/__version__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rtt-sdk",
    version=get_version(),
    author="Nick Landers, NetSPI",
    author_email="rtt.support@netspi.com",
    description="Scripting SDK for the Red Team Toolkit platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://netspi.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["colorful~=0.4.4", "pefile~=2021.5.13", "requests~=2.25.1", "websockets~=8.1"],
    python_requires=">=3.7",
)
