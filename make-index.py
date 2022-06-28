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

import os, sys, time, zipfile
import urllib.error, urllib.request
from io import BytesIO

check_headings = ["Status", "Name", "Publisher", "UEF", "ROMs", "Options", "URL", "Files"]

lines = open("roms.csv").readlines()

headings = lines.pop(0).strip().split(",")
if headings != check_headings:
    sys.stderr.write("Headings in the roms.csv file were not as expected.\n")
    sys.exit(1)

uef_dir = "UEFs"

if not os.path.isdir(uef_dir):
    os.mkdir(uef_dir)

new_lines = ["<html>", "<head>", "<title>UEF2ROM Tests</title>", "</head>",
             "<body>", "<h1>UEF2ROM Tests</h1>", "<ul>"]

jsbeeb_url = "https://bbc.godbolt.org/"
rom_base_url = "https://dboddie.github.io/UEF2ROM-recipes-BBC-Micro/ROMs/"

for line in lines:

    pieces = line.strip().split(",")
    if len(pieces) != len(check_headings):
        print("Invalid entry:", pieces)
        continue

    d = {}
    for key, value in zip(check_headings, pieces):
        d[key] = value

    if not d["Status"].startswith("OK"):
        print("Skipping", d["Name"], "-", d["Status"])
        continue

    rom_urls = []
    for rom in d["ROMs"].split():
        rom_urls.append("rom=" + rom_base_url + rom)

    if "-rn" in d["Options"]:
        command = "*" + d["Options"].split("-rn")[1].split()[0]
    else:
        command = '*ROM%0aCHAIN%22%22'

    link = jsbeeb_url + "?" + "&".join(rom_urls) + "&autotype=" + command + "%0a"
    new_lines += ["<li>", '<a href="' + link + '">' + d["Name"] + '</a>']

new_lines += ["</ul>", "</body>", "</html>"]

open("index.html", "w").write("\n".join(new_lines) + "\n")
