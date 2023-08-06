from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
    name='py_D',
    version='0.0.1',
    description='Simple Downloader',
    Long_description= open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='Muhammad Muzammil Alam',
    author_email='muzammil.alam231@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='downloader',
    packages=find_packages(),
    install_requires=['requests']

)