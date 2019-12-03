# Scrape
Scrapes the WebAdvisor for course information

2nd Dec -> Made the scraper to scrape through a year's calendar for all the subject's courses
           It now stores course ID, name, credits worth, offering semesters, prerequisite, restrictions,
           course offering(in terms of distance learning etc), and course description

           It is important that there are no extra ','s in any columns the csv

           Fixed the bug where the files would give empty results even though they should contain data
           Fix: check if the df is empty -> i.e URL pages which had no relevant data would still save the csv but on
           the same name as the previous file, due to the specific file naming convention used
