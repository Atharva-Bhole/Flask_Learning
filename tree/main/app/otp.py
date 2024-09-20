import random 
from twilio.rest import Client

otp = random.randint(1000,9999)
name = "Atharva"
email = "atharvabhole239@gmail.com"
account_sid = "AC6a2513332fbdfa46ab8206ab2619d2f2"
auth_token = "8df1b75bd9551005c23088f980b87dd6"

client = Client(account_sid, auth_token)

verification = client.verify \
    .v2 \
    .services('VAc2d5fc01541224b40d39eedd4115c955') \
    .verifications \
    .create(to='+918208868362', channel='sms')
print("Message Sent")
message = client.messages.create(
    to='+918208868362',
    from_='+17608527109',
    body=f'Registration Process initiated on our Platform ABCD Name : {name}, Email: {email}, otp={otp}'
)
print("Message Sent")