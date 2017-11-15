from setuptools import setup, find_packages

setup(
    name='fpyutils',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.rst').read(),
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@student.unife.it',
    keywords='utilities',
    url='https://github.com/frnmst/fpyutils',
    python_requires='>=3',
    # This part was inspired by:
    # https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-script$
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
#        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[],
)

