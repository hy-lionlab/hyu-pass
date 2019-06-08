import boto3

from baro import app


CHARSET = "UTF-8"


def send_email(email, subject, body):
    ses = boto3.client(
        "ses",
        region_name=app.config["AWS_SES_REGION"],
        aws_access_key_id=app.config["AWS_SES_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["AWS_SES_ACCESS_SECRET_KEY"],
    )

    ses.send_email(
        Source=app.config["EMAIL_FROM"],
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Charset": CHARSET, "Data": subject},
            "Body": {"Html": {"Charset": CHARSET, "Data": body}},
        },
    )

    return True
