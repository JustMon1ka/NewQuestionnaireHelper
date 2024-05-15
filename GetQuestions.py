import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

from QuestionType.Input import Input
from QuestionType.MultipleChoice import MultipleChoice
from QuestionType.SingleChoice import SingleChoice
from QuestionType.Scoring import Scoring
from QuestionType.MultipleScoring import MultipleScoring
from QuestionType.Sorting import Sorting


def get_questions(url: str, edge_driver_path: str):
    Edge_options = Options()
    Edge_options.add_argument('--disable-gpu')  # 禁用GPU加速，某些系统/驱动需要
    Edge_options.add_argument("--log-level=3")
    Edge_options.add_argument("--silent")

    print("开始初始化浏览器引擎......", end="")
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service, options=Edge_options)
    print("Done！")
    print("开始获取网页信息......", end="")

    driver.get(url)
    print("Done！")
    print("开始解析网页......", end="")

    div_question = driver.find_element(By.ID, "divQuestion")
    next_page_button = driver.find_element(By.ID, "divNext").find_element(By.XPATH, "./a")
    question_elements = []
    for i in range(1, 100):
        try:
            question_elements.append(div_question.find_element(By.XPATH, f".//*[@pg='{i}']"))
        except Exception as e:
            print("Done!")
            print(f"共收集到{i - 1}道问题！")
            break
    print("请注意：作者没有几乎没有做任何错误输入处理，任何错误输入都可能导致程序直接崩溃，所以请在输入时自行确保输入正确")
    input("按回车键继续，下面将逐题展示详细信息...")
    os.system('cls')
    print("正在分析题目......")

    question_type = {
        "1": "填空题",
        "3": "单选题",
        "4": "多选题",  # minvalue代表至少选几项
        "5": "单项打分题",
        "6": "多项打分题",
        "11": "排序题",
        # 更多题型待补充
    }

    # style-relation表示如果选了某几个题的某个选项会影响该题的出现
    questions = []
    for question_element in question_elements:
        question_div = question_element.find_element(By.XPATH, "./div")
        q_type = question_div.get_attribute("type")
        q_relation = question_div.get_attribute("relation")
        relations = []
        if q_relation is not None:
            relations = q_relation.split(";")

        in_question_divs = question_div.find_elements(By.XPATH, "./div")
        title_element = in_question_divs[0]
        title = driver.execute_script("return arguments[0].textContent", title_element.find_element(By.XPATH, "./div"))
        if q_type == "1":
            # 填空题处理规则
            input_div = in_question_divs[1]
            input_blank = input_div.find_element(By.XPATH, "./input")

            question = Input(title=title,
                             q_type=question_type.get(q_type),
                             choices=[],
                             relation=relations,
                             elements=input_blank,
                             next_page_element=next_page_button
                             )

            questions.append(question)

        elif q_type == "3":
            # 单选题处理规则
            choices_div = in_question_divs[1]
            choices_elements = choices_div.find_elements(By.XPATH, "./div")
            choices = []
            answers_element = []
            for choices_element in choices_elements:
                choice = driver.execute_script("return arguments[0].textContent",
                                               choices_element.find_element(By.XPATH, "./div"))
                choice_button = choices_element.find_element(By.XPATH, "./span").find_element(By.XPATH, "./a")
                choices.append(choice)
                answers_element.append(choice_button)

            question = SingleChoice(title=title,
                                    q_type=question_type.get(q_type),
                                    choices=choices,
                                    relation=relations,
                                    elements=answers_element,
                                    next_page_element=next_page_button
                                    )

            questions.append(question)

        elif q_type == "4":
            # 多选题处理规则
            choices_div = in_question_divs[1]
            min_select = question_div.get_attribute("minvalue")
            choices_elements = choices_div.find_elements(By.XPATH, "./div")
            choices = []
            answers_element = []
            for choices_element in choices_elements:
                choice = driver.execute_script("return arguments[0].textContent",
                                               choices_element.find_element(By.XPATH, "./div"))
                choice_button = choices_element.find_element(By.XPATH, "./span").find_element(By.XPATH, "./a")
                choices.append(choice)
                answers_element.append(choice_button)

            question = MultipleChoice(title=title,
                                      q_type=question_type.get(q_type),
                                      choices=choices,
                                      relation=relations,
                                      elements=answers_element,
                                      next_page_element=next_page_button
                                      )
            question.set_min_select(min_select)

            questions.append(question)

        elif q_type == "5":
            # 单项打分题处理规则
            score_items_elements = in_question_divs[1].find_element(By.XPATH, "./div/ul").find_elements(By.XPATH, "./li")
            score_items = []
            score_items_button = []
            for score_items_element in score_items_elements:
                score_item_button = score_items_element.find_element(By.XPATH, "./a")
                score_item = score_item_button.get_attribute("title")
                score_items.append(score_item)
                score_items_button.append(score_item_button)

            question = Scoring(title=title,
                               q_type=question_type.get(q_type),
                               choices=score_items,
                               relation=relations,
                               elements=score_items_button,
                               next_page_element=next_page_button
                               )

            questions.append(question)

        elif q_type == "6":
            # 多项打分题处理规则
            scores_items_table = in_question_divs[1].find_element(By.XPATH, "./table")
            scores_items_elements_raw = scores_items_table.find_element(By.XPATH, "./tbody").find_elements(By.XPATH, "./tr")
            row_titles_element = scores_items_elements_raw[0].find_elements(By.XPATH, "./th")
            row_titles = []
            for row_title_element in row_titles_element:
                row_title = driver.execute_script("return arguments[0].textContent", row_title_element)
                row_titles.append(row_title)

            scores_items_elements = []
            for scores_items_element_raw in scores_items_elements_raw:
                if scores_items_element_raw.get_attribute("fid") is not None:
                    scores_items_elements.append(scores_items_element_raw)

            scores_items_titles = []
            scores_items_buttons = []
            for scores_items_element in scores_items_elements:
                td_elements = scores_items_element.find_elements(By.XPATH, "./td")
                scores_item_title = driver.execute_script("return arguments[0].textContent",
                                                          td_elements[0].find_element(By.XPATH, "./div/span"))

                scores_item_buttons = []
                for td_element in td_elements[1:]:
                    scores_item_button = td_element.find_element(By.XPATH, "./a")
                    scores_item_buttons.append(scores_item_button)

                scores_items_titles.append(scores_item_title)
                scores_items_buttons.append(scores_item_buttons)

            question = MultipleScoring(
                title=title,
                q_type=question_type.get(q_type),
                choices=[],
                relation=relations,
                elements=scores_items_buttons,
                row_title=row_titles,
                items_title=scores_items_titles,
                next_page_element=next_page_button
            )
            questions.append(question)

        elif q_type == "11":
            # 排序题处理规则
            sort_items_div = question_div.find_element(By.XPATH, "./ul")
            sort_items_elements = sort_items_div.find_elements(By.XPATH, "./li")
            sort_items_lable = []
            sort_items_button = []
            for sort_items_element in sort_items_elements:
                sort_item_element = sort_items_element.find_elements(By.XPATH, "./div")
                sort_item_lable = driver.execute_script("return arguments[0].textContent",
                                                        sort_item_element[1].find_element(By.XPATH, "./span"))
                sort_item_button = sort_item_element[0].find_element(By.XPATH, "./span")
                sort_items_lable.append(sort_item_lable)
                sort_items_button.append(sort_item_button)

            question = Sorting(title=title,
                               q_type=question_type.get(q_type),
                               choices=sort_items_lable,
                               relation=relations,
                               elements=sort_items_button,
                               next_page_element=next_page_button
                               )

            questions.append(question)

    return questions, question_elements, driver


def reset_questions_elements(questions: list, url: str, edge_driver_path: str):
    Edge_options = Options()
    Edge_options.add_argument("--headless")  # 添加无头参数
    Edge_options.add_argument('--disable-gpu')  # 禁用GPU加速，某些系统/驱动需要
    Edge_options.add_argument("--log-level=3")
    Edge_options.add_argument("--silent")

    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service, options=Edge_options)

    driver.get(url)

    div_question = driver.find_element(By.ID, "divQuestion")
    next_page_button = driver.find_element(By.ID, "divNext").find_element(By.XPATH, "./a")

    question_elements = []
    for i in range(1, 100):
        try:
            question_elements.append(div_question.find_element(By.XPATH, f".//*[@pg='{i}']"))
        except Exception as e:
            break

    questions1 = []
    for question, question_element in zip(questions, question_elements):
        question_div = question_element.find_element(By.XPATH, "./div")
        in_question_divs = question_div.find_elements(By.XPATH, "./div")
        q_type = question_div.get_attribute("type")
        if q_type == "1":
            # 填空题处理规则
            input_div = in_question_divs[1]
            input_blank = input_div.find_element(By.XPATH, "./input")

            question.reset_elements(answer_elements=input_blank, next_button=next_page_button)
            questions1.append(question)

        elif q_type == "3":
            # 单选题处理规则
            choices_div = in_question_divs[1]
            choices_elements = choices_div.find_elements(By.XPATH, "./div")
            answers_element = []
            for choices_element in choices_elements:
                choice_button = choices_element.find_element(By.XPATH, "./span").find_element(By.XPATH, "./a")
                answers_element.append(choice_button)

            question.reset_elements(answer_elements=answers_element, next_button=next_page_button)
            questions1.append(question)

        elif q_type == "4":
            # 多选题处理规则
            choices_div = in_question_divs[1]
            choices_elements = choices_div.find_elements(By.XPATH, "./div")
            answers_element = []
            for choices_element in choices_elements:
                choice_button = choices_element.find_element(By.XPATH, "./span").find_element(By.XPATH, "./a")
                answers_element.append(choice_button)

            question.reset_elements(answer_elements=answers_element, next_button=next_page_button)
            questions1.append(question)

        elif q_type == "5":
            # 单项打分题处理规则
            score_items_elements = in_question_divs[1].find_element(By.XPATH, "./div/ul").find_elements(By.XPATH, "./li")
            score_items_button = []
            for score_items_element in score_items_elements:
                score_item_button = score_items_element.find_element(By.XPATH, "./a")
                score_items_button.append(score_item_button)

            question.reset_elements(answer_elements=score_items_button, next_button=next_page_button)
            questions1.append(question)

        elif q_type == "6":
            # 多项打分题处理规则
            scores_items_table = in_question_divs[1].find_element(By.XPATH, "./table")
            scores_items_elements_raw = scores_items_table.find_element(By.XPATH, "./tbody").find_elements(By.XPATH, "./tr")

            scores_items_elements = []
            for scores_items_element_raw in scores_items_elements_raw:
                if scores_items_element_raw.get_attribute("fid") is not None:
                    scores_items_elements.append(scores_items_element_raw)

            scores_items_buttons = []
            for scores_items_element in scores_items_elements:
                td_elements = scores_items_element.find_elements(By.XPATH, "./td")

                scores_item_buttons = []
                for td_element in td_elements[1:]:
                    scores_item_button = td_element.find_element(By.XPATH, "./a")
                    scores_item_buttons.append(scores_item_button)

                scores_items_buttons.append(scores_item_buttons)

            question.reset_elements(answer_elements=scores_items_buttons, next_button=next_page_button)
            questions1.append(question)

        elif q_type == "11":
            # 排序题处理规则
            sort_items_div = question_div.find_element(By.XPATH, "./ul")
            sort_items_elements = sort_items_div.find_elements(By.XPATH, "./li")
            sort_items_button = []
            for sort_items_element in sort_items_elements:
                sort_item_element = sort_items_element.find_elements(By.XPATH, "./div")
                sort_item_button = sort_item_element[0].find_element(By.XPATH, "./span")
                sort_items_button.append(sort_item_button)

            question.reset_elements(answer_elements=sort_items_button, next_button=next_page_button)
            questions1.append(question)

    return questions1, question_elements, driver
