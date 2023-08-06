from setuptools import setup, find_packages

setup(
    name='t3dn-sdk',
    author='3D Ninjas GmbH',
    author_email='niklas@3dninjas.io',
    description='3D Ninjas Python SDK',
    classifiers=[
        'Programming Language :: Python',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    license='Proprietary',
    packages=find_packages(),
    install_requires=[
        'python-xlib',
        'ewmh',
    ],
    python_requires='>=2.7',
)
