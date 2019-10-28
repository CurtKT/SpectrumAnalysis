from twilio.rest import Client
import socket


def send_msg(phone_num, msg_text):
    account_sid = "AC1935b47defc0badb34babdd737ee8ed0"
    # Your Auth Token from twilio.com/console
    auth_token  = "22ebef54d96a9ec94b2525d2ec779791"
    client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     to="+8613219721726",
    #     from_="+12695038226",
    #     body="Hello from Python Twilio!")
    message = client.messages.create(
        to="+8615928057586",
        from_="+12078036219",
        body=msg_text+"\r\n---from xiaojiaoya")
# send_msg("+8613219721726", "hello")
tcpServerSocket=socket.socket()#创建socket对象
host = socket.gethostname()#获取本地主机名
port=8899#设置端口
tcpServerSocket.bind((host,port))#将地址与套接字绑定，且套接字要求是从未被绑定过的
tcpServerSocket.listen(5)#代办事件中排队等待connect的最大数目
translate_dic = {
    b"00": " ",
    b"01": "a",
    b"02": "b",
    b"03": "c",
    b"04": "d",
    b"05": "e",
    b"06": "f",
    b"07": "g",
    b"08": "h",
    b"09": "i",
    b"10": "j",
    b"11": "k",
    b"12": "l",
    b"13": "m",
    b"14": "n",
    b"15": "o",
    b"16": "p",
    b"17": "q",
    b"18": "r",
    b"19": "s",
    b"20": "t",
    b"21": "u",
    b"22": "v",
    b"23": "w",
    b"24": "x",
    b"25": "y",
    b"26": "z",
    b"30": "0",
    b"31": "1",
    b"32": "2",
    b"33": "3",
    b"34": "4",
    b"35": "5",
    b"36": "6",
    b"37": "7",
    b"38": "8",
    b"39": "9",
    b"40": "^_^",
    b"41": ">_<",
    b"42": "!@_@",
}
msg_recv_all = b""
while True:
    c, addr = tcpServerSocket.accept()
    while True:
        msg_recv = c.recv(1024)
        msg_text = ""
        if msg_recv:
            print("msg_recv>>>>", msg_recv)
            if msg_recv == b"\r":
                print("chufa")
                msg_recv_split = msg_recv_all.split(b"@")
                print("chufa2")
                try:
                    print("chufa3")
                    for i in range(int(len(msg_recv_split[0])/2)):
                        print("chufa4")
                        msg_text = msg_text + translate_dic[msg_recv_split[0][i*2:i*2+2]]
                        phone_num = str(msg_recv_split[1], encoding="ASCII")
                except Exception as result:
                    print(result)
                try:
                    print(phone_num, msg_text)
                    print("chufa5")
                    send_msg(phone_num=phone_num, msg_text=msg_text)
                except:
                    pass


                msg_recv_all = b""
            else:
                msg_recv_all = msg_recv_all + msg_recv
            # msg_recv_split = msg_recv.split(b"@")
            # try:
            #     for i in range(int(len(msg_recv_split[0])/2)):
            #         msg_text = msg_text + translate_dic[msg_recv_split[0][i*2:i*2+2]]
            # except Exception as result:
            #     print(result)
            # print(msg_text)
            # print(msg_recv_split)
            # # print(str(msg_recv_split[0], encoding="ASCII"))
        else:
            c.close()
            break



