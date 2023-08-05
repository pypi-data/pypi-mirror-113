from distutils.core import setup
from os import path
long_description= "simple lib to plot arrays in terminal more info -> https://github.com/pedro-design/terminal-plot-python"
setup(
  long_description=long_description,
  long_description_content_type='text/html',
  name = 'stplt',         # How you named your package folder (MyLib)
  packages = ['stplt'],   # Chose the same as "name"
  version = '0.2.0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple array  plotting in terminal',   # Give a short description about your library
  author = 'Pedro Alejandro',                   # Type in your name
  author_email = 'pedro13alejandro20@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/pedro-design/terminal-plot-python',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/pedro-design/terminal-plot-python/archive/refs/tags/1.tar.gz',    # I explain this later on
  keywords = ['Terminal', 'plotting', 'simple'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development ',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
