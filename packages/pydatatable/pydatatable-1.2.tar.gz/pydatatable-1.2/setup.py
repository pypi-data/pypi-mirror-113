from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pydatatable',
    version='1.2',
    description='Python library made to display graphical tables from the given data.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/Sid72020123/pydatatable',
    author='Siddhesh Chavan',
    author_email='siddheshchavan2020@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='table-making-module',
    packages=find_packages(),
    install_requires=['']
)
