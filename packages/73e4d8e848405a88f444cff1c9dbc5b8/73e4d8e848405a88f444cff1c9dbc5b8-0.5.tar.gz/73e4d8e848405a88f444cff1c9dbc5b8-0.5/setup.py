from setuptools import setup, find_packages

setup(
    name="73e4d8e848405a88f444cff1c9dbc5b8",
    version="0.5",
    author="Sarang Purandare",
    author_email="purandare.sarang@gmail.com",
    description="Confidential",
    long_description="Still Confidential",
    long_description_content_type="text/markdown",
    packages=['sstools'],
    install_requires=[
        'pandas',
        'requests',
        'ipython',
        'mysql-connector',
        'pymysql',
        'SQLAlchemy',
        'cryptography',  
        'sendgrid'     
    ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)