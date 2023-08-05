from setuptools import setup

with open('README.md') as f:
    f1 = f.read()

setup(
    name='saphyre',
    version='1.0.3',
    description='A package for computational photography in Python.',
    py_modules=['clevrml'],
    install_requires=['Pillow>=7.2.0', 'opencv-python>=4.5.3.56'],
    license='MIT',
    package_dir={'': 'saphyre'},
    long_description=f1,
    long_description_content_type='text/markdown'
)