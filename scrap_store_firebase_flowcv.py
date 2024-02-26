import firebase_admin
from firebase_admin import credentials, firestore


import requests 
from bs4 import BeautifulSoup 

import sys

def store_project(projectTitle, projectTitleLink, subTitle, description):
    # Define data to be posted
    data = {
        "projectTitle": projectTitle,
        "projectTitleLink": projectTitleLink,
        "subTitle": subTitle,
        "description": description
    }

    # Add data to Firestore
    # Replace 'your-collection' with the name of your collection
    # Firestore will create the collection if it doesn't exist
    db.collection('project').document().set(data)

    print(f"Data {projectTitle} added successfully to Project!")


def store_education(school, schoolLink, degree, city, country, startDate, endDate):
    # Define data to be posted
    data = {
        "school": school,
        "schoolLink": schoolLink,
        "degree": degree,
        "city": city,
        "country": country,
        "startDate": startDate,
        "endDate": endDate
    }

    # Add data to Firestore
    # Replace 'your-collection' with the name of your collection
    # Firestore will create the collection if it doesn't exist
    db.collection('education').document().set(data)

    print(f"Data {school} added successfully to Education!")

def store_work(employer, employerLink, jobTitle, city, country, startDate, endDate):
    # Define data to be posted
    data = {
        "employer": employer,
        "employerLink": employerLink,
        "jobTitle": jobTitle,
        "city": city,
        "country": country,
        "startDate": startDate,
        "endDate": endDate
    }

    # Add data to Firestore
    # Replace 'your-collection' with the name of your collection
    # Firestore will create the collection if it doesn't exist
    db.collection('work').document().set(data)
    print(f"Data {employer} added successfully to Work!")

def store_skill(skill, level, info):
    # Define data to be posted
    data = {
        "skill": skill,
        "level": level,
        "info": info
    }

    # Add data to Firestore
    # Replace 'your-collection' with the name of your collection
    # Firestore will create the collection if it doesn't exist
    db.collection('skill').document().set(data)
    print(f"Data {skill} added successfully to Skill!")

def store_interest(interest):
    # Define data to be posted
    data = {
        "interest": interest
    }

    # Add data to Firestore
    # Replace 'your-collection' with the name of your collection
    # Firestore will create the collection if it doesn't exist
    db.collection('interest').document().set(data)

    print(f"Data {interest} added successfully to Interest!")



# Access command-line arguments
# sys.argv[0] is the script name, and sys.argv[1:] are the arguments
if len(sys.argv) >= 2:
    email = sys.argv[1]
    password = sys.argv[2]

    # Replace 'path/to/your/credentials.json' with the path to your downloaded JSON file.
    firebase_cred = credentials.Certificate('C:/Users/ahmad/Downloads/portfolio-7ee13-firebase-adminsdk-e2qz5-d637806985.json')
    # cred = credentials.Certificate('/mnt/c/Users/ahmad/Downloads/portfolio-7ee13-firebase-adminsdk-e2qz5-d637806985.json')

    # Initialize Firebase app
    firebase_admin.initialize_app(firebase_cred)

    # Get a Firestore client
    db = firestore.client()
    
    # Making a post request 
    flowcv_cred = {
        "email": f"{email}",
        "password": f"{password}",
    }

    r = requests.post('https://app.flowcv.com/api/auth/login',json=flowcv_cred) 

    # Check if the request was successful (status code 200)
    if r.status_code == 200:
        # Handle JSON response
        json_response = r.json()
        #print("Response:", json_response)
        projects = json_response['data']['user']['resumes'][1]['content']['project']['entries']
        for project in projects:
            projectTitle = project.get('projectTitle','')
            projectTitleLink = project.get('projectTitleLink','')
            subTitle = project.get('subTitle','')
            description = project.get('description','')
            store_project(projectTitle,projectTitleLink,subTitle,description)
        educations = json_response['data']['user']['resumes'][1]['content']['education']['entries']
        for education in educations:
            school = education.get('school','')
            schoolLink = education.get('schoolLink','')
            degree = education.get('degree','')
            city = education.get('city','')
            country = education.get('country','')
            startDate = education.get('startDate','')
            endDate = education.get('endDate','')
            store_education(school,schoolLink,degree,city,country, startDate,endDate)
        works = json_response['data']['user']['resumes'][1]['content']['work']['entries']
        for work in works:
            employer = work.get('employer','')
            employerLink = work.get('employerLink','')
            jobTitle = work.get('jobTitle','')
            city = work.get('city','')
            country = work.get('country','')
            startDate = work.get('startDate','')
            endDate = work.get('endDate','')
            store_work(employer,employerLink,jobTitle,city,country, startDate,endDate)
        skills = json_response['data']['user']['resumes'][1]['content']['skill']['entries']
        for skill in skills:
            skillTitle = skill.get('skill','')
            level = skill.get('level','')
            info = skill.get('info','')
            store_skill(skillTitle,level,info)
        interests = json_response['data']['user']['resumes'][1]['content']['interest']['entries']
        for interest in interests:
            interestTitle = interest.get('interest','')
            store_interest(interestTitle)

    else:
        # If the request was not successful, print the error message
        print("Error:", r.text)
else:
    print("Usage: python scrap_store_firebase_flowcv.py <email> <password>")
  





