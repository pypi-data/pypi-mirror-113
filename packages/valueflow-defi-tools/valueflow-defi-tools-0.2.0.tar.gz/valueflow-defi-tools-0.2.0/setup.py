from setuptools import setup

setup(
    name='valueflow-defi-tools',
    version='0.2.0',
    description='Defi tools',
    url='https://github.com/valueflowever/DefiTools',
    author='valueflow',
    author_email='valueflow@163.com',
    packages=["DefiTools"],
    license="MIT Licence",
    install_requires=['web3==5.19.0', 'websockets==8.1', 'requests==2.25.1', 'PyYAML==5.4.1'],
    python_requires=">=3.6"
)
