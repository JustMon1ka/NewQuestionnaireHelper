# -*- coding: gbk -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import os

from GetQuestions import get_questions, reset_questions_elements

url = "https://www.wjx.cn/vm/PFwcaAl.aspx"
edge_driver_path = "./driver/msedgedriver.exe"

# ʹ��requests��ȡ��ҳ����

# ������ͷģʽ
Edge_options = Options()
# Edge_options.add_argument("--headless")  # �����ͷ����
Edge_options.add_argument('--disable-gpu')  # ����GPU���٣�ĳЩϵͳ/������Ҫ

if __name__ == "__main__":
    # ��ʼ��WebDriver
    os.system('cls')
    questions, question_elements, driver = get_questions(url, edge_driver_path)

    os.system('cls')
    for question, i in zip(questions, range(len(questions))):
        print("�ڿ�ʼ�Զ��ش�����֮ǰ����Ϊÿһ������ָ���������")
        print("_______________________________________________________")
        print()
        print(f"��{i + 1}�⣺")
        print(question)
        question.set_option(input("��������ԣ�"))
        os.system('cls')

    print("�����Ƕ��ƵĴ������������")
    for question, i in zip(questions, range(len(questions))):
        print(f"��{i+1}�⣨{question.q_type}����{question.option}. {question.option_name[question.option]}")

    input("���ȷ������,���س���ʼִ�е�һ�δ��⣨�Դ𣩣����ע�ű�����ҳ�Ĳ����Ƿ����Ԥ��")
    os.system('cls')
    for question_element, question, i in zip(question_elements, questions, range(len(questions))):
        try:
            print(f"��{i+1}�⣨{question.q_type}����", end='')
            if question_element.get_attribute("style") == "display: none;":
                print("��Ŀ������")
                continue
            question.answer_question()
            input()
            question.next_page_element.click()
        except Exception as e:
            print(e)
            break

    submit_button = driver.find_element(By.ID, "divSubmit").find_element(By.XPATH, "./div/div/div")
    submit_button.click()
    input("��һ�δ�����������ȷ�Ͻű����������밴�س���ʼˢ�ʾ����")
    driver.close()
    os.system('cls')

    num = int(input("������Ҫˢ�ķ�����"))
    os.system('cls')
    for i in range(num):
        print(f"������д��{i+1}���ʾ�����Ҫ��д{num}��")
        print("_______________________________________________________")
        questions1, question_elements1, driver1 = reset_questions_elements(questions, url, edge_driver_path)
        for question_element, question, j in zip(question_elements1, questions1, range(len(questions))):
            print(f"��{j+1}�⣨{question.q_type}����", end='')
            if question_element.get_attribute("style") == "display: none;":
                print("��Ŀ������")
                continue
            question.answer_question()
            try:
                question.next_page_element.click()
            except:
                continue

        submit_button = driver1.find_element(By.ID, "divSubmit").find_element(By.XPATH, "./div/div/div")
        submit_button.click()
        os.system('cls')
        driver1.close()

    print(f"�ű�ִ����ɣ�һ���ش���{num+1}���ʾ��ʼ���Ǵ�Ҳ�㣩������������ͳ�ƽ����")
    print("_______________________________________________________")
    for question, i in zip(questions, range(len(questions))):
        print(f"��{i+1}�⣨{question.q_type}����{question.count_answer}")
