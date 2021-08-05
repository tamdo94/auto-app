#!/usr/bin/python3

from botocore.exceptions import NoCredentialsError
import boto3
import glob
import os
from datetime import datetime
import logging
import json

logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))

SENDER = "tamcr94@gmail.com"
RECIPIENT = "tamcr94.dev@gmail.com"
SUBJECT = "Amazon SES Test (SDK for Python)"
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
            
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """            

CHARSET = "UTF-8"


AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_PRIVATE_KEY = os.getenv('AWS_PRIVATE_KEY')
AWS_REGION = os.getenv('AWS_REGION')

sns_email_msg = (
    "Heap OOM Error \r\n"
    "ENV: {0} \r\n"
    "Timestamp: {1} \r\n"
    "File: {2} \r\n" 
)

def upload_to_aws(bucket, folder):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_PRIVATE_KEY)
    ses = boto3.client('ses', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_PRIVATE_KEY)
    sns = boto3.client('sns', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_PRIVATE_KEY)

    try:
        heap_files = glob.glob(folder + "/oom.tgz")

        for filename in heap_files:
            key = os.path.basename(filename)
            name, ext = os.path.splitext(key)
            key = "%s_%s%s" % (name, datetime.now().strftime("%Y%m%d%H%M%S"), ext)

            print("Putting %s as %s" % (filename,key))

            s3.upload_file(filename, bucket, key, ExtraArgs={'ACL': 'public-read'})

            location = s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
            url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket, key)

            sns_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sns_default_msg = {
                'timestamp': sns_timestamp,
                'url': url
            }

            response = sns.publish(
                            TopicArn='arn:aws:sns:ap-southeast-1:458401166084:MyTopic',
                            Message=json.dumps({'default': json.dumps(sns_default_msg),
                                               'email': sns_email_msg.format("alpha", sns_timestamp, url) }),
                            Subject='HEAP OOM ERROR',
                            MessageStructure='json'
                        )

            logging.info("Message publish suscess: {0}".format(response))
            
        logging.info("Upload Successful")

        response = ses.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER
        )   

        return True
    except FileNotFoundError:
        logging.info("The file was not found")
        return False
    except NoCredentialsError:
        logging.info("Credentials not available")
        return False

if __name__ == "__main__":
    # execute only if run as a script
    os.system("cd /var/log && mkdir oom && mv *.hprof ./oom && tar -czvf oom.tgz oom && rm -r oom")
    upload_to_aws('tamaws2', '/var/log/')
