from setuptools import setup, find_packages



# Thanks to this guy who helped me a lot for writing this package
# https://www.youtube.com/watch?v=GIF3LaRqgXo

setup(
    name='pyatmp',
    version='0.9.0',
    description='Package for interfacing with ATMP software',
    author='Sébastien Deriaz',
    author_email='sebastien.deriaz1@gmail.com',
    #url='https://github.com/SebastienDeriaz/pyatmp',
    package_dir={'' : 'src'},
    #license='...'
    packages=find_packages(where="src"),
    #install_requires=['enum', 'socket', 'struct', 'importlib', 'sqlite3', 'numpy', 'time']
)