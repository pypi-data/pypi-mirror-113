from setuptools import setup, find_packages

'''
python setup.py sdist
twine upload dist/*
'''


setup(
    name="angeutils",
    version="1.0.1",
    author="AngeXie",
    author_email="52370ht@sina.com",
    description="For software development.",
    long_description_content_type="text/markdown",
    url="https://github.com/AngeXie/ange_pyutils",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
)