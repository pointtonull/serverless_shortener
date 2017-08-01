# Serverless URL Shortener

This is a diferent implementation of a PoC URL Shortener. I've done this one in
an attempt to think outside of the server to tackle scalability issues from the
very begining. For this it difines and deploys this infraestructure:

- Lambda functions: code logic
- Cloudfront/API-Gateway: that exposes the functions as a restfull api
- Dynamodb table: our hash distributed table
- Needed roles and policies for this components

Since DynamoDB is the botleneck, this app should scale up to read/write
throuput capacity. The tables are created with auto-scale by default, so, with
sustained high load it will scale-up and keep up with any load. The only limit
is in your wallet.

- No need to worry about scaling since Amazon takes care of it nicely
- High availability of our backend services
- Resiliency since each execution is contained and isolated, and thus have no
  impact on other executions
- Great to handle spiky workload without paying any extra computing

Limitations of the approach?, there is not a way to implement socket endpoints
at the moment.

While the problem could be resolved faster and easier with any of several
micro-framework available for Python. I am using a complete serveless to show
how simple cat be to create highly scalable solutions.

## Source Code

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


### Dependencies

- It should run with any version of Python2.+
- There are two requirements.txt, [the first one][req1] if for the project
  managment and [the another][req2] is for Lambda Functions themselves.

## How to run/deploy

### Credentials

Before you can run/deploy the application, be sure you have credentials
configured.  If you have previously configured your machine to run boto3 (the
AWS SDK for Python) or the AWS CLI then you can skip this section.

If this is your first time configuring credentials for AWS you can follow these
steps to quickly get started:

```sh
$ mkdir ~/.aws
$ cat >> ~/.aws/config
[default]
aws_access_key_id=YOUR_ACCESS_KEY_HERE
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
region=YOUR_REGION (such as us-west-2, us-west-1, etc)
Assuming you have your '~/.aws/config' file defined. 
```

### Building

To clone a local of the project:

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

### Testing

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

### Deploying

Additionally, all you need to deploy is to run:
```sh
$ make deploy
chalice --project-dir /Users/ccabrera/programacion/github/serverless_shortener/src deploy --profile tudev --no-autogen-policy --stage dev
Initial creation of lambda function.
Creating role
The following execution policy will be used:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "dynamodb:*"
      ],
      "Resource": [
        "arn:aws:dynamodb:*:*:table/dev-urls"
      ],
      "Effect": "Allow"
    }
  ]
}
Would you like to continue?  [Y/n]: y
Creating deployment package.
Initiating first time deployment...
Deploying to: dev
https://pp7yyf75sb.execute-api.eu-west-1.amazonaws.com/dev/
```

You can specify **AWS_PROFILE** as a enviroment variable or as a Make flag.
To delete an existing stack you can run:

```sh
$ make delete
chalice --project-dir /Users/ccabrera/programacion/github/serverless_shortener/src delete --profile tudev --stage dev
Deleting rest API eaqpv7zc11
Deleting lambda function shortener-dev
Delete the role shortener-dev? [y/N]: y
Deleting role name shortener-dev
```

This will delete all but the DynamoDB table.

There is a live instance running on https://pp7yyf75sb.execute-api.eu-west-1.amazonaws.com/dev/
- To register a new url you can run: https://pp7yyf75sb.execute-api.eu-west-1.amazonaws.com/dev/short?q=http://Engrish.com
- To use a shortened url you can go to: https://pp7yyf75sb.execute-api.eu-west-1.amazonaws.com/dev/n1

### Deploying to production

Well, if everything went well on 'dev' (the default stage) you can now
deploy to production.

For this you can pass the 'STAGE' flag to 'make'. The Enviroment variables and other per/stage configuration can be defined [here][config].

[app]: https://github.com/pointtonull/serverless_shortener/blob/master/src/app.py#L17
[Urls]: https://github.com/pointtonull/serverless_shortener/blob/master/src/chalicelib/database.py#L38
[getuid]: https://github.com/pointtonull/serverless_shortener/blob/master/src/chalicelib/database.py#L96
[req1]: https://github.com/pointtonull/serverless_shortener/blob/master/requirements.txt
[req2]: https://github.com/pointtonull/serverless_shortener/blob/master/src/requirements.txt
[config]: https://github.com/pointtonull/serverless_shortener/blob/master/src/.chalice/config.json

<!-- vim: set sw=4 et ts=4 :-->
