from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS :: MacOS X',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='onesignal-django',
  version='1.0.0',
  description='An interface to send push notification (both mobile and web) from Django using Onesignal',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Giacomo Venier',
  author_email='giacomo.venier@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='django, onesignal', 
  packages=find_packages(),
  install_requires=['requests'] 
)
