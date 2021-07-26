from botocore.exceptions import NoCredentialsError
import boto3
import glob
import os
from datetime import datetime

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

def upload_to_aws(bucket, folder):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_PRIVATE_KEY)
    ses = boto3.client('ses', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_PRIVATE_KEY)

    try:
        heap_files = glob.glob(folder + "/*.hprof")

        for filename in heap_files:
            key = os.path.basename(filename)
            print("Putting %s as %s" % (filename,key))

            name, ext = os.path.splitext(key)
            s3.upload_file(filename, bucket, "%s_%s%s" % (name, datetime.now().strftime("%m%d%Y%H%M%S"), ext))
            
        print("Upload Successful")

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
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

if __name__ == "__main__":
    # execute only if run as a script
    upload_to_aws('tamaws2', '/var/log/')