import pip

from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=pip.download.PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(name='sonic_app',
      version='0.1',
      description='App server for controll sonic devices',
      url='https://github.com/sumanthns/sonic-app.git',
      author='Sumanth Nagadavalli Suresh',
      author_email='nsready@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=reqs,
      zip_safe=False)
