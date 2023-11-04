#!/usr/bin/env python

import subprocess

subprocess.run(["curl", "-o", "content.html", "https://www.nrk.no/"])