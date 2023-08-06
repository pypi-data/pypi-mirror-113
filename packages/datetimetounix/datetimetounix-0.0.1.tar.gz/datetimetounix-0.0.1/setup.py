from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Simple datetime to unix converter'

# Setting up
setup(name='datetimetounix',
      author='drapes',
      author_email='lildrapesbusiness@gmail.com',
      url='https://github.com/drapespy/datetimetounix',
      version=VERSION,
      packages=find_packages(),
      license='MIT',
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      description=DESCRIPTION,
      python_requires='>=3.5.3',
      keywords = ['datetime converter', 'unix converter', 'unix', 'datetime', 'converter'],
      classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)