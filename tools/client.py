import requests
import time

post_data = {
    "command": "https://www.cnblogs.com/rslai/p/8249812.html"
}
try:
    ret = requests.post("http://203.195.243.234:12345/command", post_data)
except Exception as e:
    print(e)

while True:
    time.sleep(5)
    try:
        get_data = requests.get("http://203.195.243.234:12345/return").json()
        if get_data["code"] == 0:
            text = get_data['return'].encode()
            print(text)
            with open('test.html', 'wb') as f:
                f.write(text)
            break
    except Exception as e:
        print(e)




