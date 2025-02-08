from setuptools import setup, find_packages

setup(
    name='NFT_Python_Generator',
    version='0.1.0',
    description='A Python-based tool for generating NFT collections from SVG files.',
    author='Ali Al-Yacoub',
    author_email='zude07@yahoo.com',
    url='https://github.com/your-repository-url',  #ToDo
    packages=find_packages(),
    install_requires=[
        'CairoSVG==2.5.2',
        'numpy==1.20.0',
        'pandas==1.3.4',
        'Pillow==9.2.0',
        'setuptools==69.5.1'
    ],
    entry_points={
        'console_scripts': [
            'nft_gen_tool=NFT_Python_Generator.nft_gen_tool:main', 
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)