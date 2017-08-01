# Serverless URL Shortener

This is a toy implementation of a URL Shortener service with a
serverless aproach. It includes good practices structure for:

- predictable development enviroment setup with GNU Make
- testing and coverage enabled
- local dependences
- sub-modules
- direct deployment
- pipeline deployment

For this it declares and deploys this infraestructure:

- the code in lambda functions
- a apigateway that triger the functions
- a dynamodb table to store the urls
- a role with policies to allow the parts to interact

Since DynamoDB is the botleneck, this app should scale up to read/write
throuput capacity. The tables are created with auto-scale by default, so, with
sostained high load it with scale up and keep with the load. The only limit is
in your wallet.

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

The mechanism used by this command should work in any Posix enviroment but I
was not able to test on legacy systems, if you find a problem please issue a
bug.

To run tests and coverage you can use the respective targets:

```sh
make test
make coverage
```

This should output current status of the project:

```sh
% make coverage
cd /Users/ccabrera/programacion/github/serverless_shortener/src;\
	python -m pytest ../tests --cov /Users/ccabrera/programacion/github/serverless_shortener/src --cov-report=term-missing ../tests
================================== test session starts ==================================
platform darwin -- Python 2.7.13, pytest-3.0.7, py-1.4.33, pluggy-0.4.0
rootdir: /Users/ccabrera/programacion/github/serverless_shortener, inifile:
plugins: cov-2.4.0
collected 9 items

../tests/test__app.py ..
../tests/test__regexs.py ..
../tests/test_database.py .....

---------- coverage: platform darwin, python 2.7.13-final-0 ----------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
app.py                      29     12    59%   41-45, 55-58, 64-67
chalicelib/__init__.py       0      0   100%
chalicelib/database.py      45      1    98%   62
chalicelib/regexs.py         2      0   100%
------------------------------------------------------
TOTAL                       76     13    83%


=============================== 9 passed in 1.78 seconds ================================
[:~/programacion … serverless_shortener] [27] master(+178/-99)* ±
```

### Running

To run you can execute simply execute `make run`:

```sh
$ make run
chalice --project-dir /Users/ccabrera/programacion/github/serverless_shortener/src local
Serving on localhost:8000
```

This starts a local simulation of the server, you can now use curl to test it:
```sh
curl -s localhost:8000| jq .
{
  "endpoints": [
    {
      "url": "POST /short",
      "description": "Receives url as DATA:\n        {\"long_url\": \"http://google.com\"}\n       returns shorten url:\n        {\"short_url\": \"gy\"}\n    "
    },
    {
      "url": "GET /short",
      "description": "Receives url as URL param <Q>:\n        service.com?q=http://google.com\n    "
    },
    {
      "url": "GET /{short_url}",
      "description": "Re-direct to the original url."
    },
    {
      "url": "GET /",
      "description": "Describes available endpoints"
    }
  ],
  "service": "serverless url shortener"
}
```

The root endpoint does instrospection and describes the service. If you dont
have 'jq' installed you may want to use your browser.

There is a live instance running on https://eaqpv7zc11.execute-api.eu-west-1.amazonaws.com/dev/
To register a new url you can run: https://eaqpv7zc11.execute-api.eu-west-1.amazonaws.com/dev/short?q=http://Engrish.com
To use a shortened url you can go to: https://eaqpv7zc11.execute-api.eu-west-1.amazonaws.com/dev/n1


[app]: https://github.com/pointtonull/serverless_shortener/blob/master/src/app.py#L17
[Urls]: https://github.com/pointtonull/serverless_shortener/blob/master/src/celib/database.py#L38
[getuid]: https://github.com/pointtonull/serverless_shortener/blob/master/src/celib/database.py#L96

<!-- vim: set sw=4 et ts=4 :-->
