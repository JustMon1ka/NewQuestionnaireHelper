# -*- coding: gbk -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import os

from GetQuestions import get_questions, reset_questions_elements

url = "https://www.wjx.cn/vm/PFwcaAl.aspx"
edge_driver_path = "./driver/msedgedriver.exe"

# 使用requests获取网页内容

# 设置无头模式
Edge_options = Options()
# Edge_options.add_argument("--headless")  # 添加无头参数
Edge_options.add_argument('--disable-gpu')  # 禁用GPU加速，某些系统/驱动需要

if __name__ == "__main__":
    # 初始化WebDriver
    os.system('cls')
    questions, question_elements, driver = get_questions(url, edge_driver_path)

    os.system('cls')
    for question, i in zip(questions, range(len(questions))):
        print("在开始自动回答问题之前，请为每一道问题指定答题策略")
        print("_______________________________________________________")
        print()
        print(f"第{i + 1}题：")
        print(question)
        question.set_option(input("请输入策略："))
        os.system('cls')

    print("以下是定制的答题策略总览：")
    for question, i in zip(questions, range(len(questions))):
        print(f"第{i+1}题（{question.q_type}）：{question.option}. {question.option_name[question.option]}")

    input("如果确认无误,按回车开始执行第一次答题（试答），请关注脚本对网页的操作是否符合预期")
    os.system('cls')
    for question_element, question, i in zip(question_elements, questions, range(len(questions))):
        try:
            print(f"第{i+1}题（{question.q_type}），", end='')
            if question_element.get_attribute("style") == "display: none;":
                print("题目被跳过")
                continue
            question.answer_question()
            input()
            question.next_page_element.click()
        except Exception as e:
            print(e)
            break

    submit_button = driver.find_element(By.ID, "divSubmit").find_element(By.XPATH, "./div/div/div")
    submit_button.click()
    input("第一次答题结束，如果确认脚本运行无误，请按回车开始刷问卷次数")
    driver.close()
    os.system('cls')

    num = int(input("请输入要刷的份数："))
    os.system('cls')
    for i in range(num):
        print(f"正在填写第{i+1}份问卷，共需要填写{num}份")
        print("_______________________________________________________")
        questions1, question_elements1, driver1 = reset_questions_elements(questions, url, edge_driver_path)
        for question_element, question, j in zip(question_elements1, questions1, range(len(questions))):
            print(f"第{j+1}题（{question.q_type}），", end='')
            if question_element.get_attribute("style") == "display: none;":
                print("题目被跳过")
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

    print(f"脚本执行完成！一共回答了{num+1}次问卷（最开始的那次也算），以下是运行统计结果：")
    print("_______________________________________________________")
    for question, i in zip(questions, range(len(questions))):
        print(f"第{i+1}题（{question.q_type}）：{question.count_answer}")
