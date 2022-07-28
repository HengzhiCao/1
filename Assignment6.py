import pymysql
import webbrowser
import os
import requests
import html5lib
from bs4 import BeautifulSoup

def read_password():
    with open("password.txt") as file:
        password = file.read().strip()
    return password


def connect_to_mars():
    password = read_password()
    conn = pymysql.connect(host="mars.cs.qc.cuny.edu", port=3306, user="cahe9544", passwd=password, database="cahe9544")
    # cursor = conn.cursor()
    # cursor.execute("SHOW DATABASES")
    # for row in cursor:
    #     print(row)
    return conn


def get_state_data():
    url = 'https://www.thespreadsheetguru.com/blog/list-united-states-capitals-abbreviations'
    # get URL html
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = []
    items = soup.find_all('p')


    capitol_data = ""
    abbvr_data = ""

    for item in items:
        if "Alabama" in item:
            state_data = str(item)
        if "NJ" in item:
            abbvr_data = str(item)
        if "Juneau" in item:
            capitol_data = str(item)
    #print(f"test_data = {test_data}")

    index = state_data.index("Alabama")
    state_data = state_data[index:].split("<br/>")

   # print(state_data)

    index = abbvr_data.index("AL")
    abbvr_data = abbvr_data[index:].split("<br/>")
    #print(abbvr_data)

    index = capitol_data.index("Montgomery")
    capitol_data  = capitol_data[index:].split("<br/>")
    #print(capitol_data)
    state_data[49] = state_data[49].replace('</p>', '')
    abbvr_data[49] = abbvr_data[49].replace('</p>', '')
    capitol_data[49] = capitol_data[49].replace('</p>', '')
    states = []
    for i in range(50):
        states.append([state_data[i], abbvr_data[i], capitol_data[i]] )

    return states


def insert_state_data(states):
    conn = connect_to_mars()
    cursor = conn.cursor()
    for state in states:
        query = "insert into state values ('"+state[1]+"','"+state[0]+"','"+state[2]+"')"
        print(query)
        cursor.execute(query)
    conn.commit()
    conn.close()


def main():
    connect_to_mars()
    states = get_state_data()
    insert_state_data(states)


if __name__ == '__main__':
    main()

