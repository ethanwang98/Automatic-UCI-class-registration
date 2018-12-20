from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import schedule, time


def job(user: str, pwd: str, to_enroll: [int], to_waitlist: [int], order: [str]) -> None:
    """Opens up Chrome Driver, waits 57 seconds and automatically enters the user in their classes or waitlists"""
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
    for i in order:
        if i == 'enroll':
            elem = driver.find_element_by_xpath("//input[@value='Enrollment Menu']")
            elem.click()
            for x in range(len(to_enroll)):
                while True:
                    elem = driver.find_element_by_xpath("//input[@value='add']")
                    elem.click()
                    elem = driver.find_element_by_name("courseCode")
                    elem.send_keys(to_enroll[x])
                    elem.send_keys(Keys.RETURN)
                    try:
                        driver.find_element_by_class_name("WebRegErrorMsg")
                    except NoSuchElementException:
                        print("Class successfully added.")
                        break
                    except KeyboardInterrupt:
                        print("Aborted adding of class")
                        break
        else:
            elem = driver.find_element_by_xpath("//input[@value='Wait list Menu']")
            elem.click()
            for x in range(len(to_waitlist)):
                while True:
                    elem = driver.find_element_by_xpath("//input[@value='add']")
                    elem.click()
                    elem = driver.find_element_by_name("courseCode")
                    elem.send_keys(to_waitlist[x])
                    elem.send_keys(Keys.RETURN)
                    try:
                        driver.find_element_by_class_name("WebRegErrorMsg")
                    except NoSuchElementException:
                        print("Class successfully added to the waitlist.")
                        break
                    except KeyboardInterrupt:
                        print("Aborted adding class to waitlist.")
                        break


def get_info(choice: str) -> tuple:
    """Takes information about user, such as username, password, and course codes, and returns a tuple
    containing all of that information"""
    to_enroll = []
    to_waitlist = []
    if choice == 'manual':
        while True:
            priority = input("Type 'waitlist' for entering classes to waitlist or 'enroll' for entering classes to "
                             "enroll, or both words separated by comma for both")
            if priority in ['waitlist', 'enroll', 'waitlist,enroll', 'enroll,waitlist']:
                break
            print("Invalid input.")
        order = priority.split(',')
        user = input("Enter your UCI username: ")
        pwd = input("Enter your UCI password: ")
        for i in order:
            if i == 'enroll':
                to_enroll = enroll(choice)
            else:
                to_waitlist = waitlist(choice)
    else:
        file = open('info.txt', 'r')
        user = file.readline().rstrip()
        pwd = file.readline().rstrip()
        order = file.readline().rstrip().split(',')
        for i in order:
            if i == 'enroll':
                to_enroll = enroll(choice, file)
            else:
                to_waitlist = waitlist(choice, file)
    return user, pwd, to_enroll, to_waitlist, order


def enroll(choice: str, file = None) -> list:
    """Takes course codes of classes that the user wants to enroll in and returns a list
    with all of those course codes"""
    lst = []
    if choice == 'manual':
        class_num = int(input("How many classes are you signing up for? "))
        for i in range(class_num):
            class_part = int(input("How many parts do you need to sign up for to enter this class? "))
            for j in range(class_part):
                course_code = int(input("Enter the course code: "))
                lst.append(course_code)
    else:
        class_num = int(file.readline().rstrip())
        for i in range(class_num):
            class_part = int(file.readline().rstrip())
            for j in range(class_part):
                course_code = int(file.readline().rstrip())
                lst.append(course_code)
    return lst


def waitlist(choice: str, file = None) -> list:
    """Takes course codes of classes that the user wants to waitlist and returns a list
    with all of those course codes"""
    lst = []
    if choice == 'manual':
        class_num = int(input("How many classes are you trying to waitlist? "))
        for i in range(class_num):
            class_part = int(input("How many parts do you need to sign up for to enter this class? "))
            for j in range(class_part):
                course_code = int(input("Enter the course code: "))
                lst.append(course_code)
    else:
        class_num = int(file.readline().rstrip())
        for i in range(class_num):
            class_part = int(file.readline().rstrip())
            for j in range(class_part):
                course_code = int(file.readline().rstrip())
                lst.append(course_code)
    return lst


def main():
    """User can choose to input information manually or from a file, and they must enter a time
     one minute before their desired time to ensure that the program enters the information at
     the exact desired time."""
    while True:
        choice = input("Type 'manual' to enter information manually or 'auto' to read information from a file: ")
        if choice != 'manual' or choice != 'auto':
            print("Invalid input.")
        else:
            break
    info = get_info(choice)
    enroll_time = input("Enter the time one minute before your enrollment window opens (use 24-hour time): ")
    schedule.every().day.at(enroll_time).do(job, info[0], info[1], info[2], info[3], info[4])
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
