# Serverless URL Shortener

This is a toy implementation of a URL Shortener service with a
serverless aproach. It includes good practices structure for:

- predictable development enviroment setup with GNU Make
- testing and coverage enabled
- local dependences
- sub-modules
- direct deployment
- pipeline deployment


## Overview

While the problem could be resolved faster and easier with any of several
micro-framework available for Python. I am using a complete serveless to show
how simple it can be to create fully scalable solutions.

### src/app.py

[App][app] is the handler, it is called as entrypoint when deployed as Lambda
Function.

### src/chalicelib/database.py

[Urls][Urls] this class implements the interface for dynamo and the model logic.
It's '__init__' method ensure the table exists.
I, as well, implements a missing DynamoDB feature, atomic [autoincremental uid][getuid].

### Makefile

Python is so simple to setup/use it doesn't require a Makefile most of the
time. But in my experience this reduces the surface of error and enables new
developers to get to speed faster.


## Dependencies

- It should run with Python2.+ and Python3+ (use Python3, please)
- It doesn't have external dependences (they would be in requirement.txt if
  any)

## How to build/run

To clone a local copy:

```sh
git clone git@github.com:pointtonull/serverless_shortener.git
cd serverless_shortener
```

To install dependences:

```sh
make deps
```

After this step you should have a `_buld` directory where all the relevant
libraries are stored. The mechanism used by this command should work in any
Posix enviroment but I was not able to test on legacy systems, if you find a
problem please issue a bug.

To run tests and coverage you can use the respective targets:

```sh
make test
make coverage
```

This should output current status of the project:

```sh
% make coverage
Pulling in dependencies...
================================== test session starts ==================================
platform darwin -- Python 3.6.1, pytest-3.1.3, py-1.4.34, pluggy-0.4.0
rootdir: /Users/ccabrera/programacion/github/neu, inifile:
plugins: cov-2.5.1
collected 1 item s

../tests/test__example.py .

---------- coverage: platform darwin, python 3.6.1-final-0 -----------
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
lib/__init__.py       0      0   100%
lib/matrix.py        77      3    96%   6-7, 102
main.py              13     13     0%   3-18
-----------------------------------------------
TOTAL                90     16    82%


=============================== 1 passed in 0.27 seconds ================================
```

The tests includes given example.

### Running

To run you can execute simply execute `make run`:

```sh
$ make run
Pulling in dependencies...
Intruction: bot 75 gives low to bot 145 and high to bot 95
  > bot 75 had been created
Intruction: bot 116 gives low to bot 157 and high to bot 197
  > bot 116 had been created
Intruction: bot 185 gives low to bot 57 and high to bot 139
  > bot 185 had been created

(...)

bot 1 is shuting down
bot 113 is shuting down
bot 136 is shuting down
bot 192 is shuting down
bot 98 is shuting down
===
The result is bot 141
```

[Complete example output][example_output].

### Debuging

To run a Interactive shell in the enviroment of the program you can run:

```sh
make shell
```

Like me, do you love IPython?, you can use it with:

```sh
make PYTHON_VERSION=ipython shell
```

And even use it to run the main routine with PDB:

```sh
make PYTHON_VERSION="ipython --pdb" run
```

And the same trick can be used to test specific python versions:

```sh
make PYTHON_VERSION=python2.6 run
```

```sh
make PYTHON_VERSION=python3.6 run
```

(you should be using Python3 tough)



[app]: https://github.com/pointtonull/serverless_shortener/blob/master/src/app.py#L17
[Urls]: https://github.com/pointtonull/serverless_shortener/blob/master/src/celib/database.py#L38
[getuid]: https://github.com/pointtonull/serverless_shortener/blob/master/src/celib/database.py#L96

<!-- vim: set sw=4 et ts=4 :-->
