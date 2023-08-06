from setuptools import setup


with open('README') as file:
    readme = file.read()

setup(
    name='wsebas_attackoftheorcs',
    version='2.0.1',
    packages=['wargame'],
    url='https://pypi.org/project/wsebas_attackoftheorcs/',
    license='LICENSE.txt',
    description='Updated fantasy game',
    long_description_content_type='text/x-rst',
    long_description=readme,
    author='William',
    author_email='william@gmail.com'
)