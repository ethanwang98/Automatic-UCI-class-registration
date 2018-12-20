#old code; will probably delete later once testing of current build finishes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import schedule, time


def job(user: str, pwd: str, lst: [int]) -> None:
    driver = webdriver.Chrome()
    time.sleep(57)
    driver.get("https://www.reg.uci.edu/registrar/soc/webreg.html")
    assert "UCI University Registrar - Course Enrollment: WebReg" in driver.title
    elem = driver.find_element_by_link_text("Access WebReg")
    elem.click()
    elem = driver.find_element_by_id("ucinetid")
    elem.send_keys(user)
    elem = driver.find_element_by_id("password")
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    assert "WebReg" in driver.title
    elem = driver.find_element_by_xpath("//input[@value='Enrollment Menu']")
    elem.click()
    for x in range(len(lst)):
        elem = driver.find_element_by_xpath("//input[@value='add']")
        elem.click()
        elem = driver.find_element_by_name("courseCode")
        elem.send_keys(lst[x])
        elem.send_keys(Keys.RETURN)
        try:
            driver.find_element_by_class_name("WebRegErrorMsg")
        except NoSuchElementException:
            print("Class successfully added.")


def main():
    lst = []
    file = open('info.txt', 'r')
    user = file.readline().rstrip()
    pwd = file.readline().rstrip()
    classnum = int(file.readline().rstrip())
    for i in range(classnum):
        classpart = int(file.readline().rstrip())
        for j in range(classpart):
            coursecode = int(file.readline().rstrip())
            lst.append(coursecode)
    enrolltime = input("Enter the time one minute before your enrollment window opens (use 24-hour time): ")
    schedule.every().day.at(enrolltime).do(job, user, pwd, lst)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
