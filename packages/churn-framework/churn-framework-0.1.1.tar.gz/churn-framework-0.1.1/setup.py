from distutils.core import setup
import os

setup(
  name = 'churn-framework', 
  packages = ['churn-framework'],
  version = '0.1.1',
  license='MIT',
  description = 'Find metrics that better separate recurring customers from customers who canceled the contract during the product/service usage journey',
  author = 'A3Data',
  author_email = 'gustavo.resende@a3data.com.br',
  url = 'https://github.com/A3Data/churn-framework',
  download_url = 'https://github.com/A3Data/churn-framework/archive/refs/tags/0.1.tar.gz',
  keywords = ['framework', 'churn', 'metric', 'optimizer'],
  install_requires=[
          'tqdm',
          'seaborn',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ]
)