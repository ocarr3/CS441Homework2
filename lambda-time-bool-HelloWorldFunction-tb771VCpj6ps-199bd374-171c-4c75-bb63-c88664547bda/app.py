import json
import boto3
import os
from io import StringIO
from datetime import datetime as dt

s3_client = boto3.client("s3")
S3_BUCKET = "cs441hw2"
S3_PREFIX = "Log"
# import requests
# Lambda function for opening files in S3 bucket and verifying the existence of logs within a given interval

def lambda_handler(event, context):
    #Opening multiple objects in an S3 bucket
    response = s3_client.list_objects_v2(
        Bucket=S3_BUCKET, Prefix=S3_PREFIX,)
    s3_files = response["Contents"]
    print("\n")
    file_content = ""
    for s3_file in s3_files:
        file_content += s3_client.get_object(
            Bucket=S3_BUCKET, Key=s3_file["Key"])["Body"].read().decode("utf-8")
    lines = file_content.splitlines()
    print(lines)
    message = "Opening File"
    try:
        firstline = lines[0]
        finalline = lines[-1]
    except IndexError:
        message = "unable to open file"
    
    # Create Date objects the given intervals 
    
    testLowerString = event['params']['querystring']['lower']
    testUpperString = event['params']['querystring']['upper']
    
    # Create a Date objects of the log entries at the beggining and the end
    
    testLowerDateString = firstline[0:12]
    testUpperDateString = finalline[0:12]

    testLowerDateInput = dt.strptime(testLowerString, "%H:%M:%S.%f")
    testUpperDateInput = dt.strptime(testUpperString, "%H:%M:%S.%f")
    testLowerDate = dt.strptime(testLowerDateString, "%H:%M:%S.%f")
    testUpperDate = dt.strptime(testUpperDateString, "%H:%M:%S.%f")
    
    dateZero = dt.strptime("00:00:00.000", "%H:%M:%S.%f")
    
    finalUpperDate = (testLowerDateInput - dateZero + testUpperDateInput)

    bool = False
    
    # Ensure that the interval exists at least partially within the log entries for use
    
    if(testLowerDateInput < testUpperDate and finalUpperDate > testLowerDate):
        bool = True

    #for line in lines:
    #    count += 1
    #    print("Line{}: {}".format(count, line.strip()))


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": message,
            "bool": bool,
            # "location": ip.text.replace("\n", "")
        }),
    }