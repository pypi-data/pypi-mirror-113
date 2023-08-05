from distutils.core import setup

setup(
    name='forefront',
    packages=['forefront'],
    version='0.2.5',
    license='MIT',
    description='Official library for use with Forefront (helloforefront.com)',
    author='Forefront Technologies',
    author_email='pypi@helloforefront.com',
    url='https://github.com/TryForefront/forefront',
    download_url='https://github.com/TryForefront/forefront/archive/refs/tags/0.2.5.tar.gz',
    keywords=['MACHINE LEARNING', 'DATA SCIENCE', 'ML', "TENSORFLOW"],
    install_requires=[
        'requests',
        'numpy',
        'tqdm',
        'prettytable',
        'pandas'
    ],
    extras_require={
        'pytorch': 'forefront-pytorch',
        'tensorflow': 'forefront-tensorflow',
        'sklearn': 'forefront-sklearn'
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
