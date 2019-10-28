from twilio.rest import Client


account_sid = "AC1935b47defc0badb34babdd737ee8ed0"
# Your Auth Token from twilio.com/console
auth_token = "22ebef54d96a9ec94b2525d2ec779791"
client = Client(account_sid, auth_token)
# message = client.messages.create(
#     to="+8613219721726",
#     from_="+12695038226",
#     body="Hello from Python Twilio!")
message = client.messages.create(
    to="+8613219721726",
    from_="+12078036219",
    body="hello mr zhang\r\n--from xiaojiaoya")