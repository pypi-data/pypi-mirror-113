from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="nexusconverter",
    version="0.0.3",
    description='将 PyTorch 模型转换为 Nexus 代码',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Guo Shuai",
    author_email="gs0801@foxmail.com",
    py_modules=["convert"],
    install_requires=["parse"],
    python_requires=">=3.6, <4",
)
