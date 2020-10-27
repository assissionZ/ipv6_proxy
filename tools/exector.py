from selenium import webdriver
import requests
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.minimize_window()

while True:
    time.sleep(3)
    try:
        get_data = requests.get("http://203.195.243.234:12345/command").json()
        print(get_data)
        if get_data['code'] == 0:
            command = get_data['command']
            print("command", command)
            if command:
                driver.get(command)
                text = driver.page_source
                print(text)

                post_data = {
                    "return": text
                }
                try:
                    ret = requests.post("http://203.195.243.234:12345/return", post_data)
                    print("ret", ret)
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


# driver.find_element_by_id("VipDefaultAccount").clear()
# driver.find_element_by_id("VipDefaultAccount").send_keys(name)
# driver.find_element_by_id("VipDefaultPassword").clear()
# driver.find_element_by_id("VipDefaultPassword").send_keys(key_str)
#
# driver.find_element_by_xpath("//input[@name='0MKKey'][@type='submit']").click()

# end = re.findall(filt, text, re.S | re.M)




