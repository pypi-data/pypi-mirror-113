from setuptools import setup

VERSION_NUMBER = '0.1.8'

setup(
    name='architest',
    packages=['architest', 'architest.utils'],
    version=VERSION_NUMBER,
    license='MIT',
    description="Architest allows you to check your project's structure conformity to initial architecture",
    author='Vladimir Semenov',
    author_email='subatiq@gmail.com',
    url='https://github.com/VASemenov/architest',
    download_url='https://github.com/VASemenov/architest/archive/refs/tags/0.1.8.tar.gz',
    keywords=['architest', 'static', 'test', 'architecture', 'design'],
    install_requires=[
        'pyyaml',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
