import random 
from twilio.rest import Client

name = "Atharva"
email = "atharvabhole239@gmail.com"
account_sid = "AC6a2513332fbdfa46ab8206ab2619d2f2"
auth_token = "8df1b75bd9551005c23088f980b87dd6"

client = Client(account_sid, auth_token)


def send_msg(name, email, otp, address, mobile):
    message = client.messages.create(
        to=f'+91{mobile}',
        from_ = '+17608527109',
        body=f"Registration Process Inititated on our Application \nName:{name}, email={email}, address={address} \n Your OTP for registration is {otp}"   
    )
