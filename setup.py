from setuptools import setup,find_packages

setup(name='tvguidegen',
      version='0.2.3',
      description='TV Guide Generator',
      url='https://github.com/7jtv/tvguidegen',
      author='Kas IPTV',
      author_email='kas.iptv@gmail.com',
      license='MIT',
      packages=find_packages(exclude=('data', 'tests*')),
      scripts=['bin/tvgg'],
      include_package_data=True,
      install_requires=[
          'pymongo',
          'lxml',
          'pytz',
          'python-slugify',
          'fuzzywuzzy',
          #'python-Levenshtein'
      ],
      long_description = open("README.md").read(),
      zip_safe=False

)
