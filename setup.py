import setuptools

setuptools.setup(name='strategy_trading',
      version='0.0.1',
      description='A simple library to backtest on a pandas dataframe',
      author='Juan Marquez git@numberjuani',
      author_email='juanignaciomarquez@gmail.com',
      packages=setuptools.find_packages(),
      install_requires=['numpy>=1.21.5',
                        'pandas>=1.3.5',
                        'python-dateutil>=2.8.2',
                        'pytz>=2022.1',
                        'six>=1.16.0'])
