from setuptools import setup
import subprocess


a = subprocess.Popen(["gnome-calculator"])

setup(
    name='mdexecod',
    version='0.0.1',
    packages=['src', 'src.execond'],
    url='https://illustria.io',
    license='MIT',
    author='Bogdan Kortnov',
    author_email='bogdan@illustria.io',
    description='mdexecod'
)
