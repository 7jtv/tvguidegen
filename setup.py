from setuptools import setup

setup(name='tvguidegen',
      version='0.1',
      description='TV Guide Generator',
      url='',
      author='Kas IPTV',
      author_email='kas.iptv@gmail.com',
      license='MIT',
      packages=['tvguidegen'],
      scripts=['bin/tvguidegen'],
      install_requires=[
          'pymongo',
      ],
      zip_safe=False

)
