import os
import unittest
import datetime


# THIS IS A UNIT TEST 
#
# configure app to use testing configuration
# setting the CONFIG_PATH environment variable to point to a TestingConfig class.

if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

import blog
from blog.filters import * 

# FilterTests class holds all of our tests for dateformat function
class FilterTests(unittest.TestCase):
    
    # takes datetime object, runs it through dateformat function, use assertEqual
    # to ensure string is formatted correctly
    def test_date_format(self):
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, "%y/%m/%d")
        self.assertEqual(formatted, "99/12/31")

    # just passing in None and making sure None is returned 
    def test_date_format_none(self):
        formatted = dateformat(None, "%y/%m/%d")
        self.assertEqual(formatted, None)

# you can do a test run of test_filters.py by using $ PYTHONPATH=. python tests/test_filters.py
# here we are setting the PYTHONPATH environment variable so the tests can import
# the blog module correctly, even though it is in a different location to the testfiles

# Regarding PYTHONPATH:
# PYTHONPATH is an environment variable, much like PATH. You can get a list of
# environment variables on UNIX-like operating systems by running the 'env' command.
# PYTHONPATH is similar to PATH in another way, in that it defines a search path.
# However, unlike PATH (which tells the operating system which directories to look
# for executable files in), PYTHONPATH is used by the Python interpreter to find out
# where to look for modules to import.

if __name__ == "__main__":
    unittest.main()


