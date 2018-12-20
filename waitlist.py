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
    elem = driver.find_element_by_xpath("//input[@value='Wait list Menu']")
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
            print("Class successfully added to the waitlist.")


def main():
    lst = []
    user = input("Enter your UCI username: ")
    pwd = input("Enter your UCI password: ")
    enrolltime = input("Enter the time one minute before the waitlist opens (use 24-hour time): ")
    classnum = int(input("How many classes are you trying to waitlist? "))
    for i in range(classnum):
        classpart = int(input("How many parts do you need to sign up for to enter this class? "))
        for j in range(classpart):
            coursecode = int(input("Enter the course code: "))
            lst.append(coursecode)
    schedule.every().day.at(enrolltime).do(job, user, pwd, lst)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
