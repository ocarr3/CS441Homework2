from http.client import ImproperConnectionState
import hashlib
import json
from platform import python_branch
import boto3
from datetime import datetime as dt
from collections import OrderedDict as SortedDict
import re
import bisect
import operator
from itertools import islice

s3_client = boto3.client("s3")
S3_BUCKET = "cs441hw2"
S3_PREFIX = "Log"

PATTERN = re.compile("([a-c][e-g][0-3]|[A-Z][5-9][f-w]){5,15}")
# import requests
# Opens objects in an S3 Bucket and reads them 
# Creates a ordered "hash map" to binary search starting at the lower bound of the given time interval
# Then searches forward from that point for generated string containing the regex

def lambda_handler(event, context):
    
    response = s3_client.list_objects_v2(
        Bucket=S3_BUCKET, Prefix=S3_PREFIX,)
    s3_files = response["Contents"]


    print("\n")
    file_content = ""
    for s3_file in s3_files:
        file_content += s3_client.get_object(
            Bucket=S3_BUCKET, Key=s3_file["Key"])["Body"].read().decode("utf-8")
        #print(file_content)
    hashTable =  []
    
    print("LEN: " ,len(file_content.splitlines()))
    
    # Creating the "hash map that is just an array of tuple("time stamp", "rest of log")
    for line in file_content.splitlines():
        date = dt.strptime(line[0:11], "%H:%M:%S.%f")
        tuple = (date, line[13:])
        hashTable.append(tuple)
    
    testLowerString = event['params']['querystring']['lower']
    testUpperString = event['params']['querystring']['upper']

    target_date = dt.strptime(testLowerString, "%H:%M:%S.%f")
    upper_date_int = dt.strptime(testUpperString, "%H:%M:%S.%f")
    dateZero = dt.strptime("00:00:00.000", "%H:%M:%S.%f")

    finalUpperDate = (target_date - dateZero + upper_date_int)

    print("TARGET DATE: ", target_date.strftime("%H:%M:%S.%f"))
    print("TARGET UPPER: ", finalUpperDate.strftime("%H:%M:%S.%f"))

    class key(object):
        def __init__(self, l , key):
            self.l = l
            self.key = key
        def __len__(self):
            return len(self.l)
        def __getitem__(self, index):
            return self.key(self.l[index])
            
    # Binary search for index of lower bound time interval or where it would fit        
    index = bisect.bisect_left(key(hashTable, operator.itemgetter(0)), target_date)     
    print("INDEX", index)
    message = "Searching files!"
    statusCode = 200
    print(len(hashTable))
    if index == len(hashTable):
        message = "There was no logs found in the given interval."
        
    # Go over the logs in the interval and check for regex
    intervalArr = []
    for x in islice(hashTable, index, None):
        if(x[0]>finalUpperDate):
            break
        messagestrInd = x[1].index("- ")
        messageStr = x[1][messagestrInd+2:]
        if (PATTERN.search(messageStr)):
            addTuple = (x[0])
            hashStr = hashlib.md5(messageStr.encode())
            intervalArr.append(hashStr.hexdigest())
        #print(x[0].strftime("%H:%M:%S.%f"), messageStr)

    if(len(intervalArr)==0):
        statusCode = 400
        message = "No strings found in interval"
    
    # Send all the matched string as hashed string back to the client
    hashStringReturn = str(intervalArr)
    
    

    print("\n")
    return {
        "statusCode": statusCode,
        "body": json.dumps({
            "message": message,
            "hash string": hashStringReturn,
            # "location": ip.text.replace("\n", "")
        }),
    }
