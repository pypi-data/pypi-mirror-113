from distutils.core import setup

setup(
    name='forefront-pytorch',
    packages=['forefront_pytorch'],
    version='0.2.3',
    license='MIT',
    description='Subpackage for forefront (helloforefront.com)',
    author='Forefront Technologies',
    author_email='pypi@helloforefront.com',
    url='https://github.com/TryForefront/forefront-pytorch',
    download_url='https://github.com/TryForefront/forefront-pytorch/archive/refs/tags/v0.2.3.tar.gz',
    keywords=['MACHINE LEARNING', 'DATA SCIENCE', 'ML', "PYTORCH"],
    install_requires=[
        'torch',
    ],
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
