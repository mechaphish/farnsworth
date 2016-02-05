from distutils.core import setup

setup(
    name='farnsworth',
    version='0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1',
    packages=['farnsworth'],
    install_requires=[i.strip() for i in open('requirements.txt').readlines() if 'git' not in i],
    description='Knowledge base of the Shellphish CRS',
    url='https://git.seclab.cs.ucsb.edu/cgc/farnsworth',
)
