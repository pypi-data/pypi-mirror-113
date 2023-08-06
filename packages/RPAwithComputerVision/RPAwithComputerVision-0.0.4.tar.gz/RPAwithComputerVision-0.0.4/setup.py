from setuptools import setup, find_packages
from io import open

with open('requirements.txt', encoding="utf-8-sig") as f:
    requirements = f.readlines()

def readme():
    with open('readme.txt', encoding="utf-8-sig") as f:
        README = f.read()
    return README

setup(name='RPAwithComputerVision',
       version="0.0.4",
       packages=find_packages(),
       description="This is code with package",
       long_description=readme(),
       author='botways',
       install_requires=requirements,
       package_data={
           '':['pytransform/*.dll', 'VM_match_images/*.jpg']
           #'':['Models/*.h5','Models/*.pkl']
           }
       )