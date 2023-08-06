# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='muldichinese',  
     version='0.1.1',
     author='Nannan Liu',
     author_email='liunannan.bfsumun@gmail.com',
     url='https://github.com/Nannan-Liu/Multidimensional-Analysis-Tagger-of-Mandarin-Chinese',
     description=('A Chinese register analyser.'),
     long_description=long_description,
     long_description_content_type="text/markdown",
     license='GNU',
     classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages_dir={"standardised_freqs": "src", "dimension_scores":'src'},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    keywords=['muldichinese', 'multidimensional', 'register', 'chinese', 'segmentation', 'nlp'],
 )