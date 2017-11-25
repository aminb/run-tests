#!/usr/bin/env python3

# run-tests.py - version 0.2.0
# Copyright (C) 2017 Amin Bandali
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# The latest version of run-tests.py is available at:
# https://github.com/aminb/run-tests

import os
import re
import subprocess
import sys


exe = "exe/tracker.exe"  # path to your executable
oracle = "project/tracker.exe"  # path to oracle executable

# directories containing at*.txt acceptance test files
test_dirs = [ "tests/acceptance/instructor"
            , "tests/acceptance/student" ]


def main():

    # if the '-o' command line argument is supplied, we
    # will use the output of the oracle executable specified
    # above. Otherwise, we'll use the at*.expected.txt files
    use_oracle = '-o' in sys.argv
    # if '-nc' is supplied, we won't use ANSI colour codes.
    nocolor = '-nc' in sys.argv

    for d in test_dirs:
        print()
        run_tests(d, use_oracle, nocolor)


def run_tests(d, use_oracle, nocolor):
    tests = []

    for dirpath, _, filenames in os.walk(d):
        for filename in sorted(filenames, key=natural):
            if not "expected" in filename:
                name, ext = os.path.splitext(filename)
                tests.append((dirpath, name + ext, name + ".expected" + ext))

    if nocolor:
        print(d)
    else:
        print(bcolors.BOLD + bcolors.OKBLUE + d + bcolors.ENDC)

    for i in range(0, len(tests)):
        exe_cmd = "{} -b {}".format(exe, os.path.join(tests[i][0], tests[i][1]))
        if use_oracle:
            oracle_cmd = "{} -b {}".format(oracle, os.path.join(tests[i][0], tests[i][1]))
            diff_cmd = "diff <(" + exe_cmd + ") <(" + oracle_cmd + ")"
        else:
            diff_cmd = "diff <(" + exe_cmd + ") " + os.path.join(tests[i][0], tests[i][2])

        diff_proc = subprocess.Popen(diff_cmd, stdout=subprocess.PIPE, shell=True, executable="/bin/bash")
        out, err = diff_proc.communicate()
        success = diff_proc.returncode == 0
        tree_symbol = "├" if i < len(tests) - 1 else "└"

        print_result(tests[i][1], nocolor, success, tree_symbol)
        if not success:
            print(diff_cmd)
            print(out.decode('utf-8'))


def print_result(filename, nocolor, success, c):
    result = "passed" if success else "failed"
    if nocolor:
        print("{}── {}: {}".format(c, filename, result))
    else:
        color = bcolors.OKGREEN if success else bcolors.FAIL
        print("{}── {}: {}{}{}".format(c, filename, bcolors.BOLD + color, result, bcolors.ENDC))


def natural(s, _nsre=re.compile('([0-9]+)')):
    # from https://stackoverflow.com/a/16090640
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == "__main__":
    main()
