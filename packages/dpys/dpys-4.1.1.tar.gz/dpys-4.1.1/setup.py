from setuptools import setup, find_packages

REQUIREMENTS = ['discord.py==1.7.3', 'aiosqlite']
DOCS = "https://sites.google.com/view/dpys"

classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='dpys',
  version='4.1.1',
  description='A library to simplify discord.py',
  long_description="The goal of DPYS is to make basic functionalities that every good bot needs easy to implement for beginners.",
  url=DOCS,  
  author='George Luca',
  author_email='fixingg@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='discord', 
  packages=find_packages(),
  install_requires=REQUIREMENTS
)