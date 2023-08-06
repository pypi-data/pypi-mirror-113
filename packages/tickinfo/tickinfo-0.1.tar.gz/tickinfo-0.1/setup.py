from setuptools import setup

setup(name='tickinfo',
      version='0.1',
      description='get ticker data and create SMA plot',
      url='http://github.com/ivanpuzako/tickinfo.git',
      author='Ivanpuzako',
      author_email='Ivanpuzako@gmail.com',
      license='MIT',
      setup_requires=[
        'pytest-runner',
    ],
      install_requires=[
          'yfinance', 
          'pandas', 
          'matplotlib'
      ],
      tests_require=['pytest'],
      packages=['tickinfo'],
      zip_safe=False)