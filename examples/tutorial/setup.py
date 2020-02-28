from setuptools import find_packages
from setuptools import setup

setup(
    name="pet_shop",
    version="1.0.0",
    description="Basic Pet Shop API",
    url='https://example.com',
    author='Pet Shop Dev Team',
    author_email='pet_shop@example.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["dos", "flask"]
)
