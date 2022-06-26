#!/usr/bin/env python3

"""
Copyright (C) 2022 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys

check_headings = ["Disk", "UEF", "Files"]

lines = open("disks.csv").readlines()

headings = lines.pop(0).strip().split(",")
if headings != check_headings:
    sys.stderr.write("Headings in the disks.csv file were not as expected.\n")
    sys.exit(1)

bf = open("disks.sh", "w")
bf.write("#!/bin/sh\n\nset -e\n\n")

for line in lines:

    pieces = line.strip().split(",")
    if len(pieces) != len(check_headings):
        print("Invalid entry:", pieces)
        continue
    
    d = {}
    for key, value in zip(check_headings, pieces):
        d[key] = value
    
    d["Files"] = d["Files"].replace(":", ",")
    
    bf.write("SSD2UEF.py %(Disk)s %(UEF)s %(Files)s\n" % d)

bf.close()
