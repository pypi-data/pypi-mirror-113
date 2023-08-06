from setuptools import setup
import setuptools
setup(
name='PypiPro',
version='2.0.0',
packages=setuptools.find_packages(),
author="robin",
author_email="xiaoyaojianxians@163.com",
install_requires=['twine','wheel','setuptools'],  # 依赖的包
python_requires='>=3'#python版本大于3
)
