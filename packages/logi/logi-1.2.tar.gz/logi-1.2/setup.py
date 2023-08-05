from setuptools import setup

setup(name='logi',
      version='1.2',
      description='a loging library',
      packages=['logi'],
      license='MPL-2.0 License',
      author = 'hiikion',
      url='https://github.com/hiikion/logi',
      install_requires=[ 
          'os',
          'time'
      ],
      author_email='mishptitsin@yandex.ru',
      zip_safe=False)
