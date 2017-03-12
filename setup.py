from setuptools import setup

description = (
'Recursively convert lists to tuples, sets to frozensets, dicts to mappingproxy etc.')


with open('README.rst') as readme:
    long_description = readme.read()

setup(name='freezedata',
      version='2.2.5',
      description=description,
      long_description=long_description,
      author='Terji Petersen',
      author_email='terji78@gmail.com',
      packages=['freezedata'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      test_suite='tests',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
