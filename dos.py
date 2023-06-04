import requests
inval={"textfield":"tfgh","textfield2":"ertyu"}
while True:
    print("erty")
    res=requests.post("http://192.168.18.152:5000/login_code",data=inval)
    print(res.text)
