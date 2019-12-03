import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

# currentURL is the course descriptions homepage for the year 2019-2020 i.e. current year
currentURL = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12/index.shtml'
response = requests.get(currentURL)

yearSoup = BeautifulSoup(response.text, 'lxml')

print(yearSoup.find_all('a')[9:-1])

urlExtension = yearSoup.find_all('a')[9:-1]  # gets all extension urls from Accounting to Zoology


# go to each extended url page for the given year
for urlExtension in yearSoup.find_all('a')[9:-1]:
    urlExtension = urlExtension['href']
    url = 'https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12/{}'.format(
        urlExtension.split('/')[1])

    response = requests.get(url)

    courseSoup = BeautifulSoup(response.text, "lxml")  # can also use html.parser

    print(courseSoup.prettify())

    courseIDs = []
    courseNames = []
    courseCredits = []
    courseOfferingsSemesters = []
    coursePrerequisites = []
    courseRestrictions = []
    courseOfferings = []
    courseDescriptions = []

    # go to each course in the given field of subject in the given year
    for course in courseSoup.find_all('div', class_="course"):

        courseID = course.a.text.split(' ')[0]

        courseName = course.a.text.split(' ')[1:-3]
        courseName = ' '.join(courseName)

        courseCredit = course.a.text.split(' ')[-1][1:-1]

        courseOfferingSemesters = course.a.text.split(' ')[-3].replace(',', ' ')

        courseIDs.append(courseID)
        courseNames.append(courseName)
        courseCredits.append(float(courseCredit))
        courseOfferingsSemesters.append(courseOfferingSemesters)

        if course.find('tr', class_="prereqs"):

            prerequisiteList = course.find('tr', class_="prereqs")

            myList = prerequisiteList.text.replace('\n', '').replace('Prerequisite(s):', '').replace(',', ' &').replace(
                'and', '&')
            myList = ' '.join(myList.split())

            coursePrerequisites.append(myList)
        else:
            coursePrerequisites.append('NONE')

        if course.find('tr', class_='restrictions'):
            restrictionList = course.find('tr', class_='restrictions')
            myList = restrictionList.text.replace('\n', '').replace('Restriction(s):', '').replace(',', ' &')

            myList = ' '.join(myList.split())
            courseRestrictions.append(myList)
        else:
            courseRestrictions.append('NONE')

        if course.find('tr', class_='offerings'):
            offeringList = course.find('tr', class_='offerings')
            myList = offeringList.text
            myList = ' '.join(myList.split())
            courseOfferings.append(myList)
        else:
            courseOfferings.append('NONE')

        if course.find('tr', class_='description'):
            descriptionList = course.find('tr', class_='description')
            myList = descriptionList.text.replace('\n', '').replace(',', '')
            myList = ' '.join(myList.split())
            courseDescriptions.append(myList)
        else:
            courseDescriptions.append('NONE')

    print(courseIDs)
    print(courseNames)
    print(courseCredits)
    print(courseOfferingsSemesters)
    print(coursePrerequisites)
    print(courseRestrictions)
    print(courseOfferings)
    print(courseDescriptions)

    df = pd.DataFrame({'ID': courseIDs,
                       'Name': courseNames,
                       'Credits': courseCredits,
                       'Offering Semesters': courseOfferingsSemesters,
                       'Prerequisites': coursePrerequisites,
                       'Restrictions': courseRestrictions,
                       'Offerings': courseOfferings,
                       'Description': courseDescriptions})
    print(df)

    # save only if the df is not empty, otherwise it will write over the previous csv file
    if df.empty is False:
        df.to_csv("csvFolder/{}courses.csv".format(courseID.split('*')[0]), index=False, encoding='utf-8')
    time.sleep(1)

print('finished')

