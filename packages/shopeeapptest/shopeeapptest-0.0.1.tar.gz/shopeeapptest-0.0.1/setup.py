import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shopeeapptest",
    version="0.0.1",
    author="yangjianquan",
    author_email="jianquan.yang@shopee.com",
    description="Shopee App UI auto test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.garena.com/shopee/loan-service/credit_backend/datafetch/app-ui-auto-test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)