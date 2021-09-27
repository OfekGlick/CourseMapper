from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium.webdriver.firefox.options import Options
import networkx as nx
from networkx.readwrite import json_graph
import json

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
    course_data['link'] = COURSE_LINK.format(course_number)
    return course_data


def build_db():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Firefox()
    driver.get("https://ug3.technion.ac.il/rishum/search")
    select_options = ["20", "13", "300", "1", "33", "7", "5", "8", "6", "4", "3", "9", "21", "350", "12", "32", "31",
                      "23", "99", "10", "11", "27", "450"]
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
    cols = ['שם מקצוע', 'מספר מקצוע', 'סילבוס', 'מקצועות קדם', 'link']
    data = data[cols]
    data['מקצועות קדם'] = data['מקצועות קדם'].fillna("").apply(
        lambda x: ''.join(char for char in x if char.isdigit() or char == " ").split())
    data = data.explode('מקצועות קדם')
    print(data.columns)
    data.rename(columns={"מספר מקצוע": "course_id", "שם מקצוע": "course_name", 'סילבוס': 'description',
                         "מקצועות קדם": "prerequisites"}, inplace=True)
    data = data[['course_id', 'prerequisites', 'course_name', 'description', 'link']]
    data.to_csv("CourseData.csv", encoding="utf-8-sig", index=False)
    return data


def build_graph(df: pd.DataFrame):
    G = nx.from_pandas_edgelist(df, 'course_id', 'prerequisites', ['course_name', 'description', 'link'])
    nan_nodes = []
    import math
    for node in G.nodes():
        if math.isnan(node):
            nan_nodes.append(node)
    G.remove_nodes_from(nan_nodes)
    data1 = json_graph.node_link_data(G)
    s1 = json.dumps(data1, ensure_ascii=False)
    with open('data.json', 'w', encoding='utf-8-sig') as f:
        json.dump(s1, f, ensure_ascii=False, indent=4)
    return G

