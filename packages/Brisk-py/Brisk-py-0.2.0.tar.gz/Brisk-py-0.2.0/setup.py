import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

gh = 'https://github.com/briskpy/brisk'

setuptools.setup(
    name='Brisk-py',
    version='0.2.0',
    author='Reet Singh',
    author_email='reet22singh+brisk@gmail.com',
    description='A way to create a lightning fast HTTP server using ASGI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=gh,
    project_urls={
        'Bug Tracker': f'{gh}/issues',
        'Documentation': f'{gh}'
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.7'
)
