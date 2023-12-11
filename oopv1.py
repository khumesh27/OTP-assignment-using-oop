import random
import smtplib
import re
from twilio.rest import Client

class MessageSender:
    def __init__(self, account_sid, auth_token, twilio_no):
        self.client = Client(account_sid, auth_token)
        self.twilio_no = twilio_no

    def send_sms(self, target_no, otp):
        target_no = "+91" + target_no
        message = self.client.messages.create(
            body=f"\nYour OTP is {otp}",
            from_=self.twilio_no,
            to=target_no
        )
        print(message.body)

    def send_email(self, mail, otp):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('khumeshkhobragade32119@gmail.com', 'bvky byyh fnyc vumf')
        msg = f'HELLO YOUR OTP IS {otp}'
        server.sendmail('khumeshkhobragade32119@gmail.com', mail, msg)
        server.quit()
        print("OTP sent! ")
        print("Your OTP is", otp)

class OTPGenerator:
    def __init__(self, message_sender):
        self.message_sender = message_sender
        self.otp = None

    def generate_otp(self):
        self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return self.otp

    def validate_mobile(self, num):
        return len(num) == 10 and num.isdigit()

    def validate_email(self, mail):
        pattern = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
        return bool(re.match(pattern, mail))

    def send_otp_over_mobile(self, target_no):
        while not self.validate_mobile(target_no):
            print("INVALID MOBILE NUMBER!")
            target_no = input("ENTER AGAIN: ")

        self.generate_otp()
        self.message_sender.send_sms(target_no, self.otp)

    def send_otp_via_email(self, mail):
        while not self.validate_email(mail):
            print("INVALID MAIL!")
            mail = input("ENTER AGAIN: ")

        self.generate_otp()
        self.message_sender.send_email(mail, self.otp)

# Menu
print("\n========================================Welcome to generate OTP========================================")
print("\n                                   <------CHOOSE PLATFORM------>                              \n\n1.SMS:\n2.Email:")
ans = input("\nENTER YOUR CHOICE:\n")

account_sid = 'ACa5ce277d7bf4c0c517e5aed7ed70cc45'
auth_token = '6fef65dc9a87f59f38d55abb65c5d206'
twilio_no = "+17087940251"

message_sender = MessageSender(account_sid, auth_token, twilio_no)
otp_generator = OTPGenerator(message_sender)

if ans.lower() == "1":
    number = input("ENTER YOUR MOBILE NUMBER: ")
    otp_generator.send_otp_over_mobile(number)

elif ans.lower() == "2":
    recipient = input("ENTER YOUR MAIL ID:\n ")
    otp_generator.send_otp_via_email(recipient)
