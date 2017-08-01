#!/usr/bin/env python
#_*_ coding: UTF_8 _*_

"""
    PoC of Serverless framework Chalice implementing clasic URL Shortener.
    It takes advantage of serverless AWS Ecosystem.
    Lambda functions for computing.
    DynamoDB as fast-hash table.

    It delivers amazinly fast and shorts urls.
"""

from chalice import Chalice, Response, BadRequestError

from chalicelib import database

app = Chalice(app_name='shortener')


URLS = database.Urls()


@app.route("/")
def get_root():
    """Describes available endpoints"""
    endpoints = []
    for path in app.routes.values():
        for handler in path.values():
            url = "%s %s" % (handler.method, handler.uri_pattern)
            description = handler.view_function.__doc__
            doc_item = {"url": url, "description": description}
            endpoints.append(doc_item)
    return {"service": "serverless url shortener", "endpoints": endpoints}


@app.route('/short')
def get_create_short():
    """Receives url as URL param <Q>:
        service.com?q=http://google.com
    """
    if not app.current_request.query_params:
        raise BadRequestError("expected '?q=url'")
    long_url = app.current_request.query_params["q"]
    short_url = URLS.shorten(long_url)
    return {'short_url': short_url}


@app.route('/short', methods=['POST'])
def post_create_short():
    """Receives url as DATA:
        {"long_url": "http://google.com"}
       returns shorten url:
        {"short_url": "gy"}
    """
    data = app.current_request.json_body
    long_url = data["long_url"]
    short_url = URLS.shorten(long_url)
    return {'short_url': short_url}


@app.route('/{short_url}')
def get_long(short_url):
    """Re-direct to the original url."""
    long_url = URLS.lengthen(short_url)
    response = Response("Redirecting to %s" % long_url,
                        headers={"Location": long_url}, status_code=301)
    return response
