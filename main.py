from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def try_find_sumbmit():
    a = try_find_element(
        '//input[@type="submit" and @name="commit" and @value="Submit response"]',
        FindType=By.XPATH,
    )
    return bool(a)


def try_find_element(class_name, FindType=By.CLASS_NAME):
    try:
        object = driver.find_element(FindType, class_name)
        is_visible = object.is_displayed()
        is_interactable = object.is_enabled()
        if is_visible and is_interactable:
            return object
        else:
            return None
    except Exception as e:
        return None


def wait_for_class_join():
    while True:
        join_button = try_find_element(
            "join_class_session_link", FindType=By.CLASS_NAME
        )
        if bool(join_button):
            join_button.click()
            break
        driver.refresh()
        sleep(2)


def input_login():
    username, passsword = open("creds.secrets", "r").read().splitlines()
    element = driver.find_element(By.ID, "username")
    element.send_keys(username)
    element = driver.find_element(By.ID, "password")
    element.send_keys(passsword)
    driver.find_element(By.ID, "mainButton").click()


def find_question_on_page():
    question_type_element = try_find_element("item_type_header", By.ID)
    question_text_element = try_find_element("item_prompt", By.ID)
    question_type = question_type_element.text if question_type_element else "Not Found"
    question_text = (
        question_text_element.text.strip() if question_text_element else "Not Found"
    )
    text_input = try_find_element("response", By.ID)
    submit_button = try_find_element("commit", By.NAME)

    result = {
        "type": question_type,
        "Question": question_text,
        "input": text_input,
        "send_button": submit_button,
    }

    match result["type"]:
        case "numerical question":
            pass
        case "many choice question":
            result["input"] = extract_answer_choices_multi()
        case _:
            print(f"Unknown question type: {question_type}")

    return result


def extract_answer_choices_multi():
    ul_element = try_find_element("responses", By.ID)
    if ul_element:
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        choices = []
        for li in li_elements:
            choice_text = (li.text, li)
            choices.append(choice_text)
        return choices
    else:
        return None


def answer_question(result):
    match result["type"]:
        case "numerical question":
            print("Handling numerical question")

            result["input"].send_keys("0")
            result["send_button"].click()
        case "many choice question":
            print("MultiSelect")
        case _:
            print(f"Unknown question type: {result['type']}")
            # Insert your code for handling unknown question types here


def is_submitted():
    element = try_find_element(
        "//*[contains(text(), 'You responded to this question')]", By.XPATH
    )

    if element:
        return True
    else:
        return False


def wait_for_submit_button():
    while not try_find_sumbmit():
        sleep(1)


def try_find_sumbmit() -> bool:
    a = try_find_element(
        '//input[@type="submit" and @name="commit" and @value="Submit response"]',
        FindType=By.XPATH,
    )
    return bool(a)


def check_session_has_ended():
    header_container = try_find_element("header_container", By.ID)

    if header_container:
        header_text = header_container.text
        return "has ended" in header_text.lower()
    else:
        return False


GeckoDriverManager().install()
driver = webdriver.Firefox()
initLink = "https://learningcatalytics.com/sign_in/?login=true"
driver.get(initLink)
input_login()
sleep(10)
wait_for_class_join()

while not try_find_sumbmit():
    driver.find_element(By.ID, "refresh").click()
    sleep(1)

wait_for_submit_button()


while True:
    if check_session_has_ended():
        break

    question = find_question_on_page()
    answer_question(question)
    question["send_button"].click()
    while not is_submitted():
        sleep(1)


driver.quit()
