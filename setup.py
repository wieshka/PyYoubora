from setuptools import setup

def read(filename):
    return open(filename).read()

setup(
    name='PyYoubora',
    version='0.2',
    description='Authentication library for amazing Python requests library against NPAW Youbora API.',
    long_description=read('readme.md'),
    url='http://github.com/wieshka/PyYoubora',
    author='Viesturs Proskins',
    author_email='viesturs.proskins@gmail.com',
    packages=['youbora'],
    zip_safe=False,
    install_requires=['requests'],
)