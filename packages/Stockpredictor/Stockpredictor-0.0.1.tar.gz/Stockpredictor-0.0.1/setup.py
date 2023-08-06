from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name='Stockpredictor',
    version='0.0.1',
    description = 'Predicts the price of a stock in a given timeframe',
    long_description = 'A simple library that predicts the price of a stock using Machine Learning & Linear Regression. The library can use algorithms to decide whether it is a good time to buy or sell a stock. ',
    url = '',
    author = 'Aryaan Hegde',
    author_email = 'aryhegde@gmail.com',
    License = 'MIT',
    classifiers = classifiers,
    # keywords = 'stock price prediction machine learning python linear regression',
    keywords = ['stock price', 'python', 'machine learning', 'linear regression', 'prediction'],
    packages = find_packages(),
    install_requires = [
        'numpy', 
        'pandas', 
        'yfinance', 
        'sklearn', 
        'datetime'
    ]
)