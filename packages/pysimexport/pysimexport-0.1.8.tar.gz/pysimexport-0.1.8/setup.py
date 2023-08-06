from setuptools import setup

setup(
    name='pysimexport',
    version='0.1.8',    
    description='A Python package to export simulation data',
    url='https://github.com/vincentchoqueuse/pysimexport',
    author='Vincent Choqueuse',
    author_email='vincent.choqueuse@gmail.com',
    license='BSD 2-clause',
    packages=['pysimexport'],
    install_requires=['numpy>=1.20',
                      'boto3>=1.16'                     
                      ],

    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',       
        'Programming Language :: Python :: 3'
    ],
)