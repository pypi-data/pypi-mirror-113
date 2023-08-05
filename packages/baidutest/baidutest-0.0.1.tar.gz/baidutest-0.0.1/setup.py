from setuptools import setup, find_packages

setup(
    name = "baidutest",
    version = "0.0.1",
    keywords = ("pip", "baidutest"),
    description = "test pip module-wxp",
    long_description = "test how to define pip module and upload to pypi-wxp",
    license = "MIT",

    url = "https://wxp.com",          # your module home page, such as
    author = "MySoul",                         # your name
    author_email = "1813057526@qq.com",    # your email

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)