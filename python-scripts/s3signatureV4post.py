#!/usr/bin/env python

import base64
import hmac
import hashlib

# for AWS S3 getbekk@gmail.com account
AWSAccessKeyId = "AKIAJH2VHI3AI7RX2WEQ"

# needs to be updated
# ------------------
AWSSecretKey = "SECRET"
ScopeDate = "20140925"
# ------------------

PolicyDocument = """{"expiration": "2100-01-01T00:00:00Z",
  "conditions": [
    {"bucket": "dispatch-dev"},
    ["starts-with", "$key", ""],
    {"acl": "public-read"},
    ["starts-with", "$Content-Type", ""],
    ["starts-with", "$X-Amz-Date", ""],
    ["starts-with", "$X-Amz-Algorithm", ""],
    ["starts-with", "$X-Amz-Credential", "AKIAJH2VHI3AI7RX2WEQ"],
    ["content-length-range", 0, 104857600]
  ]
}"""

Policy = base64.b64encode(PolicyDocument)

DateKey = hmac.new("AWS4" + AWSSecretKey, ScopeDate, hashlib.sha256).digest()
DateRegionKey = hmac.new(DateKey, "us-west-2", hashlib.sha256).digest()
DateRegionServiceKey = hmac.new(DateRegionKey, "s3", hashlib.sha256).digest()
SigningKey = hmac.new(DateRegionServiceKey, "aws4_request", hashlib.sha256).digest()

SigningKeyHex = hmac.new(DateRegionServiceKey, "aws4_request", hashlib.sha256).hexdigest()


Signature = hmac.new(SigningKey, Policy, hashlib.sha256).hexdigest()

print "SingingKeyHex: " + SigningKeyHex
print "Policy document: " + PolicyDocument
print "Policy base64: " + Policy
print "Signature: " + Signature