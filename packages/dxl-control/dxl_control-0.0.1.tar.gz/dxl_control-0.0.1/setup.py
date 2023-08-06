import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dxl_control",
    version="0.0.1",
    author="Nikolay Podkolzin",
    author_email="nickolay.podkolzin@gmail.com",
    description="Dynamixel control with Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nik-Pod/dxl_control",
    project_urls={
        "Bug Tracker": "https://github.com/Nik-Pod/dxl_control/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
       "pyserial>=3.5",
       "RPi.GPIO>=0.7.0",
    ],
    python_requires=">=3.6",
)

