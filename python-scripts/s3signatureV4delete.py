#!/usr/bin/env python

import hmac
import hashlib

# for AWS S3 getbekk@gmail.com account
AWSAccessKeyId = "AKIAJH2VHI3AI7RX2WEQ"

# needs to be updated
# ------------------
AWSSecretKey = "SECRET"
ScopeDate = "20140925"
Date = "20140926T083700Z"
FileKey = "2014/09/neidifuge334/mysuperfile1.jpg"
# ------------------

awsRegion = "us-west-2"
Host = "dispatch-dev.s3-us-west-2.amazonaws.com"

Scope = ScopeDate + "/us-west-2/s3/aws4_request"
Payload = ""
PayloadHash = hashlib.sha256(Payload).hexdigest()
SignedHeaders = "host;x-amz-date"

CanonicalRequest = "DELETE" + "\n" + "/" + FileKey +"\n\n" + "host:" + Host + "\n" + "x-amz-date:" + Date + "\n\n" + SignedHeaders + "\n" + PayloadHash
CanonicalRequestHash = hashlib.sha256(CanonicalRequest).hexdigest()
StringToSign = "AWS4-HMAC-SHA256" + "\n" + Date + "\n" + Scope + "\n" + CanonicalRequestHash

DateKey = hmac.new("AWS4" + AWSSecretKey, ScopeDate, hashlib.sha256).digest()
DateRegionKey = hmac.new(DateKey, awsRegion, hashlib.sha256).digest()
DateRegionServiceKey = hmac.new(DateRegionKey, "s3", hashlib.sha256).digest()
SigningKey = hmac.new(DateRegionServiceKey, "aws4_request", hashlib.sha256).digest()

Signature = hmac.new(SigningKey, StringToSign, hashlib.sha256).hexdigest()

print "Canonical Request: " + CanonicalRequest
print "String to sign: " + StringToSign
print "Signature: " + Signature