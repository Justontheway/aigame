from setuptools import setup, find_packages
import sys, os.path

# Don't import aigame module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'aigame'))
from version import VERSION

setup(name='aigame',
      version=VERSION,
      description='The AIGame: A toolkit for developing and comparing your reinforcement learning agents.',
      url='https://github.com/Justontheway/AI-Game',
      author='Justontheway',
      author_email='wcxontheway@126.com',
      license='MIT',
      packages=[package for package in find_packages()
                if package.startswith('aigame')],
      zip_safe=False,
      install_requires=[
          'numpy>=1.10.4',
      ],
)
