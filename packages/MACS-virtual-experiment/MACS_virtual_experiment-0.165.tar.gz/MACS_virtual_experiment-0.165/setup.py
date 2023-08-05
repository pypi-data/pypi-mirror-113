from distutils.core import setup
from setuptools import setup, find_packages
setup(
  name = 'MACS_virtual_experiment',         # How you named your package folder (MyLib)
  packages = find_packages(),  # Chose the same as "name"
  version = '0.165',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python wrapper for Monte-carlo simulation of MACS instrument',   # Give a short description about your library
  author = 'Tom Halloran',                   # Type in your name
  author_email = 'thallor1@jhu.edu',      # Type in your E-Mail
  url = 'https://github.com/thallor1/MACS-Mcstas-Interface',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/thallor1/MACS-Mcstas-Interface/blob/main/macs_mcstas.tar.gz',    # I explain this later on
  keywords = ['MonteCarlo', 'Neutron', 'Instrumentation'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'joblib',
          'matplotlib',
          'pandas',
          'PyCifRw',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  include_package_data=True,

)