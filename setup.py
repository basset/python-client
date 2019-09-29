from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='basset-python-client',
      version='1.0.0-beta',
      description='Python client for submitting snapshots to basset',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://basset.io',
      project_urls = {
            "Source Code": 'https://github.com/basset/python-client',
      },
      author='Jeremy Gonzalez',
      author_email='jeremy@jeremyg.net',
      license='MIT',
      packages=find_packages(),
      )