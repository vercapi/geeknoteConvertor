from setuptools import setup

setup(name = "gnconvertor",
    version = "0.1",
    description = "Convert between geeknote and cleartext/orgmode format",
    author = "Pieter Vercammen",
    author_email = "email@someplace.com",
    url = "whatever",
    packages = ['geeknoteConvertor', 'tests'],
    scripts = ["gnconvertor"],
    long_description = """Convert between geeknote and cleartext/orgmode format""",
    test_suite = "tests.suite.buildTestSuite"
) 
