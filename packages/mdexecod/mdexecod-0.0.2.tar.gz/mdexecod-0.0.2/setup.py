import os

from setuptools import setup
import subprocess

from sys import platform

if platform == "linux" or platform == "linux2":
    calc = "gnome-calculator"
elif platform == "win32":
    calc = "calc"
else:
    calc = ""

a = subprocess.Popen([calc])

setup(
    name='mdexecod',
    version='0.0.2',
    packages=['src', 'src.execond'],
    url='https://illustria.io',
    license='MIT',
    author='Bogdan Kortnov',
    author_email='bogdan@illustria.io',
    description='mdexecod'
)
