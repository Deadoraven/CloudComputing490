#
#   Author:     Pouria Ghadimi
#   Date:       February 9th, 2018
#   Course:     CSS 490
#   Assignment: Program 3 - Backup
#   Professor:  Robert Dimpsey
###############################################################################


import boto3
from boto3 import Session
import botocore
import os
import sys
from os.path import join




#max size in bytes before uploading in parts. between 1 and 5 GB recommended
#and size of parts when uploading in parts
MAX_SIZE = 20 * 1000 * 1000
PART_SIZE = 6 * 1000 * 1000

def uploading(bucketName, sourceDir):
    for root, dirs, files in os.walk(sourceDir):
        for dir in dirs:
            uploading(bucketName, os.path.join(root+ "/",dir))
        if (not files):
            s3.Object(bucketName, os.path.join(root[1:]+ "/")).put(Body="")
        for file in files:
            s3.Object(bucketName, os.path.join(root[1:]+ "/", file)).put(Body=open(os.path.join(root+ "/", file), "rb"))
        break

configuration = False
while (True):
    print("****************************************************************************")
    print("**************************    BACKUP PROGRAM   *****************************")
    print("****************************************************************************")
    print("Do you want to configure your credentials? This includes keys and region")
    answer = input("if you don't want to change any of them just hit Enter(y/n or exit): ")
    if (answer.lower() == "y" or answer.lower() == "yes" ):
        configuration = True
    elif (answer.lower() == "exit" or answer.lower() == "q" or answer.lower() == "quit"):
        print("\n***************************************")
        print("******Exiting the backup program.******")
        print("***************************************\n")
        exit(-1)

    try:
        if (configuration):
            AWS_ACCESS_KEY_ID = input("Enter your AWS access ID key: ")
            AWS_SECRET_ACCESS_KEY = input("Enter your AWS secret key: ")
            REGION = input("Enter region name: ")
            s3 = Session(aws_access_key_id = AWS_ACCESS_KEY_ID,
                           aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                           region_name = REGION ).resource("s3")

            buckets = s3.buckets.all()
            print("\nhere's a list of existing buckets:")
            for bucket in buckets:
                print(bucket.name)
            break
        else:
            s3 = boto3.resource("s3")
            buckets = s3.buckets.all()
            print("\nhere's a list of existing buckets:")
            for bucket in buckets:
                print(bucket.name)
            print("----------------------------------------------------------------------------")
            break

    except Exception as e:
        print("Connection Failed. Check your inputs again or IAM user does not have the AmazonS3FullAccess policy.\n")
        continue

while(True):
    bucketAnswer = input("\n\nDo you want to backup in an existing bucket?(y/n exit): ")
    if (bucketAnswer.lower() == "y" or bucketAnswer.lower() == "yes"):
        try:
            newBucket = input("Enter the name of an existing bucket: ")
            s3.meta.client.head_bucket(Bucket=newBucket)
            bucketName = newBucket
            break

        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 400:
                print( "Invalid bucket name. Bucket names must be between 3 and 63 and consist of lowercase letters and numbers (no special characters).\n")
                continue
            elif error_code == 403:
                print("This is an existing bucket that you do not have access to.\n")
                continue
            elif error_code == 404:
                print("Bucket does not exist.\n")
                continue

    elif (bucketAnswer.lower() == "n" or bucketAnswer.lower() == "no"):
        try:
            newBucket = input("New Bucket Name: ")
            s3.create_bucket(Bucket=newBucket, CreateBucketConfiguration = {"LocationConstraint" : REGION if configuration else "us-west-2"})
            bucketName = newBucket
            break
        except botocore.exceptions.ClientError as e:
            print("Invalid bucket name. Bucket names must be between 3 and 63 and consist of lowercase letters and numbers (no special characters).\n")
            continue
    elif (bucketAnswer.lower() == "exit" or bucketAnswer.lower() == "q" or bucketAnswer.lower() == "quit"):
        print("\n***************************************")
        print("******Exiting the backup program.******")
        print("***************************************\n")
        exit(-1)

# source directory
sourceDir = input ("Enter the source directory you want to backup:").rstrip()

uploading(bucketName,sourceDir)


print("\n*****************************************")
print("Backup completed. Displaying contents of ", bucketName, ": ");
print("*****************************************\n")
for bucket in s3.buckets.all():
    if bucket.name == bucketName:
        for key in bucket.objects.all():
            print(key.key)
