from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_desc = readme.read()

requires = ['Sphinx>=7.0', 'setuptools']

setup(
    name='sphinx-embedPDF',
    version='0.1',
    url='https://github.com/steinerAdi/sphinx-embedPDF.git',
    download_url='https://github.com/steinerAdi/sphinx-embedPDF.git',
    license='MIT',
    author='Adrian STEINER',
    author_email='sna4@bfh.ch',
    description='Sphinx embed PDF extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 0.0.1',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxEmbedPDF'],
)