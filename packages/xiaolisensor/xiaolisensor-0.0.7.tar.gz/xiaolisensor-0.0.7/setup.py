from setuptools import setup, find_packages

setup(
    name="xiaolisensor",
    version="0.0.7",
    keywords=("xiaolisensor", "sdk", "xialingming"),
    description="xiaili sensors sdk",
    long_description="xiaoli sensors sdk for python",
    license="MIT Licence",

    url="http://xialingming",
    author="lmxia",
    author_email="xialingming@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["dht11", "adafruit-circuitpython-hcsr04"]
)