#!/usr/bin/env python3
""" Main file """

get_page = __import__('web').get_page

con = get_page('http://slowwly.robertomurray.co.uk')
print(con)
