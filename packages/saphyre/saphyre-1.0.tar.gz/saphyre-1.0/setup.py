from setuptools import setup

with open('README.md') as f:
    fh = f.read()

setup(
    name='saphyre',
    version='1.0',
    description='A package for computational photography in Python',
    py_modules=['saphyre'],
    install_requires=['Pillow>=7.2.0', 'opencv-python>=4.5.3.56'],
    license='MIT',
    package_dir={'': 'saphyre'},
    long_description=fh,
    long_description_content_type='text/markdown'
  
)