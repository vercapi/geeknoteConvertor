from distutils.core import setup

setup(name = "gnconvertor",
    version = "0.1",
    description = "Convert between geeknote and cleartext/orgmode format",
    author = "Pieter Vercammen",
    author_email = "email@someplace.com",
    url = "whatever",
    packages = ['geeknoteConvertor'],
    scripts = ["gnconvertor"],
    long_description = """Convert between geeknote and cleartext/orgmode format""" 
) 
