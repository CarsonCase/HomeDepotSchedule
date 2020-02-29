from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from loginCrypto import *

#class structure of a "workday"
class workday:
    date = ""
    start_time = ""
    end_time = ""
    lunch = False

#used to log in
def Clear_and_enter_box(element,toEnter):
    element.clear()
    element.send_keys(toEnter)
#PIN needed to decrypt password
PIN = str(input("What is the PIN your password is encrypted with?: "))
#get JSON file
loginData = getLoginData()

#Open the webdriver
PATH = os.getcwd()+"\chromedriver.exe"
driver = webdriver.Chrome(executable_path=PATH)

#Define Variables
URL = 'https://hdapps.homedepot.com/LaborMgtTools/WFMEssLauncher'
STORE_NUMBER = loginData["storeNum"]
USER = loginData["username"]
PASS = cypher(loginData["password"],PIN)
#go to the URL
driver.get(URL)
#Get elements to log in
storeNum_box = driver.find_element_by_name('j_storenumber')
userId_box = driver.find_element_by_name('j_username')
pass_box = driver.find_element_by_name('j_password')
signIn_button = driver.find_element_by_name('action')
#Enter info to log in
Clear_and_enter_box(storeNum_box,STORE_NUMBER)
Clear_and_enter_box(userId_box, USER)
Clear_and_enter_box(pass_box, PASS)
signIn_button.click()

#wait until schedule is loaded (hopefully)
driver.implicitly_wait(10)

#get a list of all the day elements, put them in a big list
workDaysRaw = []
for i in range(1,8):
    workDaysRaw += driver.find_elements_by_class_name("child"+str(i))

#analize each element in list. Create a JSON object for each
toJSON = []

for day in workDaysRaw:
    #get the text of the current day object and format it
    textDay = day.text
    textDay = textDay.replace(" ","")
    textDay = textDay.replace("\n","")
    #if day includes a time (means I am working that day)
    if ("-" in textDay):
        #format string appropriatly and build into a workday object
        currentDay = workday()
        #this is always 5 digits
        currentDay.date = textDay[:5]
        #this depends on if it's a 4 or 3 digit time. So we base it on the location of -
        currentDay.start_time = textDay[5:textDay.find("-")]

        #if contains an L that means I have a lunch. Handle end date differently if we do
        if("L" in textDay):
            currentDay.lunch = True
            #this also depends on digits but also needs to stop before a potential L character (meaning lunch)
            currentDay.end_time = textDay[textDay.find("-")+1:textDay.find("L")]
        else:
            currentDay.lunch = False
            currentDay.end_time = textDay[textDay.find("-")+1:]
        #add to a list of workdays
        toJSON.append(currentDay)
    
json_string = json.dumps([ob.__dict__ for ob in toJSON])
with open('workdays.json', 'w') as outfile:
        json.dump(json_string, outfile, indent=4, sort_keys=True)
print("success! Data is in workdays.json")

#helps me
while True:
    pass

driver.quit()



