import json

def writeJSON(password, storeNum='3311', user = 'cxc6eys'):
    signInData = {
        'storeNum':storeNum,
        'username':user,
        'password':password
    }
    jsonData = json.dumps(signInData)
    with open('data.json', 'w') as outfile:
        json.dump(jsonData, outfile)
    print("data printed to data.json")

#this is an easy way to not store my raw password. Sure, it's not properly secure. But whatever. At least it's not raw text
#XORs with a pin
def cypher(rawPassword,key):
    keyLength = len(key)
    count = 0
    outputString = ""
    for i in rawPassword:
        count+=1
        I = count % int(keyLength)
        current = key[I]
        outputString += chr(ord(i)^ord(current))
    return outputString

#read a JSON and get the data
def getLoginData():
    with open('data.json') as f:
        data = json.load(f)

    return json.loads(data)


