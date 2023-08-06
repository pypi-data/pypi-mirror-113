import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'schooloam',      
  packages = ['schooloam'], 
  version = '0.0.1',  
  license='MIT', 
  description = 'Libaries OOP by Chaiyapat Oam',
  long_description=DESCRIPTION,
  author = 'Chaiyapat Oam',                 
  author_email = 'chaiyapatoam12@gmail.com',     
  url = 'https://github.com/chaiyapatoam/schooloam',  
  download_url = 'https://github.com/chaiyapatoam/schooloam/archive/0.0.1.zip',  
  keywords = ['OOP', 'school', 'Chaiyapat Oam'],   
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)