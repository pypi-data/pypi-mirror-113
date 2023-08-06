from setuptools import find_packages, setup


setup(
    name='eventor_py',
    packages=find_packages(),
    version='0.0.2',
    description='Python 3 api wrapper for eventor',
    author='William Grunder',
    install_requires=[
          'certifi==2020.12.5',
          'chardet==4.0.0',
          'idna==2.10',
          'requests==2.25.1',
          'urllib3==1.26.3',
      ],
    license='MIT',
)