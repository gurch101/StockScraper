"""stockretriever"""

from setuptools import setup

setup(
    name='stockretriever',
    version='1.0',
    description='retrieves stock information from Yahoo! Finance using YQL',
    url='https://github.com/gurch101/StockScraper',
    author='Gurchet Rai',
    author_email='gurch101@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='yahoo finance stocks',
    py_modules=['stockretriever']
)
