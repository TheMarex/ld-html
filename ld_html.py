#!/usr/bin/python3
#
#  ld-html is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  git-bibisect is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ld-html. If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright ld-html 2013: Patrick Niklaus
#
#
# Html Linker
#
# Replaces the links generared by pandoc in for of
#   <a href="#id">Foo</a>
# with:
#   <a href="filename.html#id">Foo</a>
#

import sys
import os
import re
from html.parser import HTMLParser

def replace_ids(path, ids):
    f = open(path, "r")
    data = f.read()
    f.close()
    for i in ids:
        link1 = "href=\"%s\""
        link2 = "href='%s'"
        rel_id = "#%s" % i
        abs_id = "%s#%s" % (ids[i], i)
        data = data.replace(link1 % rel_id, link1 % abs_id)
        data = data.replace(link2 % rel_id, link2 % abs_id)
    f = open(path, "w")
    f.write(data)
    f.close()

class LinkParser(HTMLParser):
    def __init__(self, path, ids):
        HTMLParser.__init__(self)
        self._path = path
        self._ids = ids

    def handle_starttag(self, tag, attr):
        for name, value in attr:
            if name == "id":
                if value in self._ids:
                    print("Warning: ID %s was used twice." % value)
                ids[value] = self._path

if len(sys.argv) < 2:
    print("Error: Not enough arguments.")
    print("Usage: ld_html.py HTML_DIR")

output = sys.argv[1]
files = os.listdir(output)
files = [f for f in files if f.endswith(".html")]
files = [os.path.join(output, f) for f in files]

# Parse html file and generate dictionary
ids = {}
for path in files:
    parser = LinkParser(os.path.relpath(path, output), ids)
    f = open(path)
    data = f.read()
    f.close()
    parser.feed(data)
    parser.close()

for path in files:
    replace_ids(path, ids)
