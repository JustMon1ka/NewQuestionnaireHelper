from selenium.webdriver.remote.webelement import WebElement

from Question import Question


class MultipleScoring(Question):
    def __init__(self, title: str, q_type: str, choices: list[str], relation: list[str], elements: list[list[WebElement]],
                 next_page_element: WebElement, row_title: list[str], items_title: list[str]):
        super().__init__(title, q_type, choices, relation, elements, next_page_element)
        self.row_title = row_title
        self.items_title = items_title
        self.count_answer = self.init_count_answer()
        self.specified = []
        self.probability = []
        self.option_name = {
            "0": "完全随机",
            "1": "标准的正态分布",
            "2": "指定出现概率，其余选项等可能出现"
        }

    def __str__(self):
        result = f"题目：{self.title}\n题型：{self.q_type}\n\n"
        max_len = []
        for items_title in self.items_title:
            max_len.append(len(items_title))
        for index, row_title in enumerate(self.row_title):
            result += f"{'':<{max(max_len)+2}}"
            result += f"{self.choice_names[index]}. {row_title:<{len(row_title)+2}}"
        result += "\n"
        for items_title in self.items_title:
            result += f"{items_title}\n"
        result += f"\n题目关联：{self.relation}"
        result += "\n"
        result += "请输入此题的答题策略（0：完全随机 | 1：标准的正态分布 | 2：指定出现概率，其余选项等可能出现）：\n"
        return result

    def set_option(self, option):
        self.option = option
        if option == "":
            self.option = "0"
        elif option != "0":
            for i in range(len(self.items_title)):
                self.specified.append(input(f"请输入 第{i}题 要指定的那个打分项（大写小写均可）：").upper())
                if option == "2":
                    self.probability.append(int(input("你选择了策略 2 ，请指定出现概率（0~100，输入纯数字）：")))

    def init_count_answer(self):
        result = {}
        for answer_elements, i in zip(self.answer_elements, range(len(self.items_title))):
            result[i] = {}
            for index, answer_element in enumerate(answer_elements):
                result[i][self.choice_names[index]] = 0

        return result

    def answer_question(self):
        if not self.specified:
            self.specified = self.items_title
        for item_title,  answer_elements, specified, i in zip(self.items_title, self.answer_elements, self.specified, range(len(self.items_title))):
            element, index = None, None
            if self.option == "0":
                element, index = self.single_choice_like_option0(answer_elements)
            elif self.option == "1":
                element, index = self.single_choice_like_option1(answer_elements, specified)
            elif self.option == "2":
                element, index = self.single_choice_like_option2(answer_elements, specified)

            choice = self.choice_names[index]
            print(f"{i},{item_title}：{choice}", end="  ")
            self.count_answer[i][choice] += 1
            element.click()

