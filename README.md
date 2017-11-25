# run-tests

`run-tests.py` is a small and useful script for automatically checking a series
of acceptance tests (`at*.txt`) against a set of files containing the expected
outputs (`at*.expected.txt`) and reporting passed and failed tests. There's also
optional support for comparing against the output of an oracle, instead of the
`at*.expected.txt` files. Comparison is done using `diff`, and thus for a test
to succeed, the outputs must *exactly* match, character by character.

This script is meant to be used in a project with directory structure similar as
below:

```
.
├── exe
│   └── tracker.exe
├── project
│   └── tracker.exe
├── tests
│   └── acceptance
│       ├── instructor
│       │   ├── at0.expected.txt
│       │   └── at0.txt
│       └── student
│           ├── at1.expected.txt
│           ├── at1.txt
│           ├── at2.expected.txt
│           ├── at2.txt
│           ├── at3.expected.txt
│           └── at3.txt
└── utils
    └── run-tests.py
```

Where in this case our executable is `exe/tracker.exe` and the oracle provided
by instructor is `project/tracker.exe`.

When using without an oracle, each acceptance file is assumed to be accompanied
by an expected output file. For instance, the expected output of running
`at3.txt` must be in a file named `at3.expected.txt` in the same directory.

If the script is called with the optional `-o` (for **o**racle) option,
`at*.expected.txt` files will be ignored and each of the acceptance files will
be run through both the student's executable and the orcale provided by
instructor, and their outputs will be compared using `diff`.

`run-tests.py` uses ANSI colour codes to add basic formatting and colouring to
its output. This can be optionally disabled by issuing the `-nc`
(**n**o**c**olor) switch.

An example output of the script is as follows:

```
tests/acceptance/instructor
└── at0.txt: failed
diff <(exe/tracker.exe -b tests/acceptance/instructor/at0.txt) tests/acceptance/instructor/at0.expected.txt
43c43,50
<   state 7 e11: this container will exceed phase capacity
---
>   state 7 ok
>   max_phase_radiation: 50.00, max_container_radiation: 10.00
>   phases: pid->name:capacity,count,radiation
>     pid1->unpacking:2,1,3.00,{glass,metal,plastic,liquid}
>     pid2->compacting:2,1,5.50,{glass,metal,plastic}
>   containers: cid->pid->material,radioactivity
>     cid1->pid2->glass,5.50
>     cid4->pid1->metal,3.00
45c52,59
<   state 8 e11: this container will exceed phase capacity
---
>   state 8 ok
>   max_phase_radiation: 50.00, max_container_radiation: 10.00
>   phases: pid->name:capacity,count,radiation
>     pid1->unpacking:2,0,0.00,{glass,metal,plastic,liquid}
>     pid2->compacting:2,2,8.50,{glass,metal,plastic}
>   containers: cid->pid->material,radioactivity
>     cid1->pid2->glass,5.50
>     cid4->pid2->metal,3.00


tests/acceptance/student
├── at1.txt: passed
├── at2.txt: passed
└── at3.txt: passed
```

As we can see, in the case of a failure the script will display the `diff`
command used for the check, and will also display the output of the `diff` for
convenience.
