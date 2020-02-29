import json
from loginCrypto import *

store_number = input("What is your store number? ")
username = input("What is your Home Depot username? ")
password = input("What is your Home Depot Password? (don't worry, this will be encrypted with the PIN you give next and not stored in plaintext): ")
pin = input("What is your pin? This can be any number of unicode characters. Make it as simple or complex as you like. You will need it every time you scan your schedule: ")

writeJSON(cypher(password,pin), store_number, username)

