import setuptools

setuptools.setup(name='strategy',
      version='0.0.2',
      description='A simple library to backtest on a pandas dataframe',
      author='Juan Marquez git@numberjuani',
      author_email='juanignaciomarquez@gmail.com',
      packages=setuptools.find_packages(),
      install_requires=['numpy',
                        'pandas',
                        'python-dateutil',
                        'pytz',
                        'six'])
