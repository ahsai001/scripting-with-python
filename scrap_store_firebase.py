import firebase_admin
from firebase_admin import credentials, firestore


import requests 
from bs4 import BeautifulSoup 
  

# Replace 'path/to/your/credentials.json' with the path to your downloaded JSON file.
cred = credentials.Certificate('/mnt/c/Users/ahmad/Downloads/simple-tools-3e1db-firebase-adminsdk-t11uo-be1ef1e24a.json')

# Initialize Firebase app
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()
  
# Making a GET request 

for index in range(227):
    r = requests.get(f'https://equran.id/doa/{index+1}') 
    # Parsing the HTML 
    soup = BeautifulSoup(r.content, 'html.parser') 
    
    #title
    result = soup.select('body>div#__next>div:nth-of-type(2)>main.flex-1.p-4>div:nth-of-type(1)>main:nth-of-type(1)>div:nth-of-type(2)>div:nth-of-type(1)') 
    title = result[0].text
    # print(title)

    #arabic
    result = soup.select('body>div#__next>div:nth-of-type(2)>main.flex-1.p-4>div:nth-of-type(1)>main:nth-of-type(1)>div:nth-of-type(2)>div:nth-of-type(2)>p:nth-of-type(2)') 
    arabic = result[0].text
    # print(arabic)

    #transliterasi
    result = soup.select('body>div#__next>div:nth-of-type(2)>main.flex-1.p-4>div:nth-of-type(1)>main:nth-of-type(1)>div:nth-of-type(2)>div:nth-of-type(2)>p:nth-of-type(3)') 
    transl = result[0].text
    # print(transl)

    #arti
    result = soup.select('body>div#__next>div:nth-of-type(2)>main.flex-1.p-4>div:nth-of-type(1)>main:nth-of-type(1)>div:nth-of-type(2)>div:nth-of-type(2)>p:nth-of-type(4)') 
    arti = result[0].text
    # print(arti)

    #ref
    result = soup.select('body>div#__next>div:nth-of-type(2)>main.flex-1.p-4>div:nth-of-type(1)>main:nth-of-type(1)>div:nth-of-type(2)>div:nth-of-type(2)>p:nth-of-type(5)') 
    ref = result[0].text
    # print(ref)

    # Define data to be posted
    data = {
        "title": title,
        "arabic": arabic,
        "trans": transl,
        "arti": arti,
        "ref": ref 
    }

    # Add data to Firestore
    # Replace 'your-collection' with the name of your collection
    # Firestore will create the collection if it doesn't exist
    db.collection('doa').document().set(data)

    print(f"Data ke {index} added successfully to Firestore!")
