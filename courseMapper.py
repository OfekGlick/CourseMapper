from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium.webdriver.firefox.options import Options
import pyodbc
from sqlalchemy import create_engine

COURSE_LINK = "https://ug3.technion.ac.il/rishum/course/{}/202101"


def extract_data(course_number):
    soup = BeautifulSoup(requests.get(COURSE_LINK.format(course_number)).text, features="lxml")
    properties = soup.find_all("div", {"class": "property"})
    values = soup.find_all("div", {"class": "property-value"})
    course_data = {}
    for p, v in zip(properties, values):
        prop = ''.join([char for char in p.text if (ord(char) in range(1488, 1515) or char == " ")])
        val = ''.join(
            [char for char in v.text if (ord(char) in range(1488, 1515) or char == " ") or (
                    ord(char) in range(48, 58) and ord(char) not in range(1488, 1515))])
        course_data[prop] = val

    return course_data


if __name__ == '__main__':
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Firefox()
    driver.get("https://ug3.technion.ac.il/rishum/search")
    select_options = ["20", "13", "300", "1", "33", "7", "5", "8", "6", "4", "3", "9", "21", "350", "12", "32", "31",
                      "23", "99", "10", "11", "27", "450"]
    # select_options = ["9"]
    data = []
    for option in select_options:
        print(option)
        select = Select(driver.find_element_by_name('FAC'))
        select.select_by_value(option)
        driver.find_element_by_id("search_button").click()
        data.append(pd.DataFrame([extract_data(course.text) for course in
                                  driver.find_elements_by_class_name("course-number")]).reset_index().drop("index",
                                                                                                           axis=1))
        driver.back()
    driver.close()
    data = pd.concat(data)
    cols = ['שם מקצוע', 'מספר מקצוע', 'סילבוס', 'מקצועות קדם']
    data = data[cols]
    data.to_csv("tempDB.csv", encoding="utf-8-sig")
