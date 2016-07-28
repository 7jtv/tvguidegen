from setuptools import setup,find_packages

setup(name='tvguidegen',
      version='0.1.1',
      description='TV Guide Generator',
      url='https://github.com/7jtv/tvguidegen',
      author='Kas IPTV',
      author_email='kas.iptv@gmail.com',
      license='MIT',
      packages=find_packages(exclude=('data', 'tests*')),
      scripts=['bin/tvguidegen'],
      install_requires=[
          'pymongo',
      ],
      zip_safe=False

)
