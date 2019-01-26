"""
Database interface
"""

import os

from botocore.exceptions import ClientError
from chalice import NotFoundError, BadRequestError
import boto3
import hashids

from . import regexs


PROFILE = os.environ.get("AWS_PROFILE")
TABLE_NAME = os.environ.get("TABLE_NAME", "dev-urls")
TABLE_DEFINITION = {
    "TableName": TABLE_NAME,
    "KeySchema": [
        {
            'AttributeName': 'uid',
            'KeyType': 'HASH'
        }
    ],
    "AttributeDefinitions": [
        {
            'AttributeName': 'uid',
            'AttributeType': 'N'
        }
    ],
    "ProvisionedThroughput": {
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }
}


class Urls:
    """
    Database interface for ShortUrl - URL pairing based on hashing approach.
    """

    def __init__(self):
        """Initialize hasher and init_tables"""
        self.init_table()
        self._hasher = hashids.Hashids(salt="Your parrot is death")

    def init_table(self):
        """"assures table exists"""
        self.session = boto3.Session(profile_name=PROFILE)
        self.dynamodb = self.session.resource("dynamodb")
        self.table = self.dynamodb.Table(TABLE_NAME)

        try:
            self.dynamodb.meta.client.describe_table(TableName=TABLE_NAME)
        except ClientError as error:
            if error.response['Error']['Code'] == 'ResourceNotFoundException':
                self.table = self.dynamodb.create_table(**TABLE_DEFINITION)
                client = self.table.meta.client
                client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
            else:
                raise


    def shorten(self, long_url):
        """
        Given a long_url, creates a uid to store the relationship between the
        hash of this uid and the long url.
        """
        if not regexs.url.match(long_url):
            raise BadRequestError("'%s' is not a valid url" % long_url)
        uid = self._get_new_id()
        short_url = self._hasher.encode(uid)
        self.table.put_item(Item={"uid": uid, "long_url": long_url})
        return short_url


    def lengthen(self, short_url):
        """
        Given a short url, gets the related uid, fetches the record, and
        returns the corresponding long_url.
        """
        try:
            uid = self._hasher.decode(short_url)[0]
        except:
            raise BadRequestError("'%s' is not a valid shourturl" % short_url)

        response = self.table.get_item(Key={"uid": uid})
        if "Item" in response:
            long_url = response["Item"]["long_url"]
            return long_url
        else:
            raise NotFoundError("Shorturl '%s' not recognized" % short_url)


    def _get_new_id(self):
        """
        Atomic operation to create a new uid enusirng to avoid collitions.
        """
        response = self.table.update_item(
            Key={"uid": -1},
            UpdateExpression="add last_id :inc",
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="ALL_NEW"
        )
        return int(response["Attributes"].get("last_id", 1))
