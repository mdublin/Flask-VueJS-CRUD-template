#!/usr/bin/env python

#coverage watches our script as tests run, it will show report which lines of code were missed, what tests we missed, etc
import coverage
# tell coverage to monitor anything inside app package
# branch=True tests all brances of conditional statements 
COV = coverage.coverage(branch=True, include='app/*')
COV.start()


# creating a test suite, telling unittest to go look for directory called tests
import unittest
suite = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2).run(suite)

COV.stop()
COV.report()


