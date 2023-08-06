from setuptools import setup

version = '0.0.1'

setup(name='discord-ext-vector',
      author='drapes',
      url='https://github.com/Vector-Development1/discord-ext-vector',
      version=version,
      packages=['discord.ext.vector'],
      license='MIT',
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      description='An extension module with COOL stuff!',
      install_requires=['discord.py>=1.7.0'],
      python_requires='>=3.5.3'
)