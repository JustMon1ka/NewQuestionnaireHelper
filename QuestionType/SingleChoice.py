from selenium.webdriver.remote.webelement import WebElement

from Question import Question


class SingleChoice(Question):
    def __init__(self, title: str, q_type: str, choices: list[str], relation: list[str], elements: list[WebElement],
                 next_page_element: WebElement):
        super().__init__(title, q_type, choices, relation, elements, next_page_element)
        self.option_name = {
            "0": "完全随机",
            "1": "标准的正态分布",
            "2": "指定出现概率，其余选项等可能出现"
        }

    def __str__(self):
        result = f"题目：{self.title}\n题型：{self.q_type}"
        result += f"，选项共{len(self.choices)}个：\n"
        result += "\n"
        for index, choice in enumerate(self.choices):
            # 使用索引获取选项名
            option_name = self.choice_names[index]
            result += f"{option_name}. {choice}\n"
        result += "\n"
        result += f"题目关联：{self.relation}"
        result += "\n"
        result += "请输入此题的答题策略（0：完全随机 | 1：标准的正态分布 | 2：指定出现概率，其余选项等可能出现）：\n"
        return result

    def set_option(self, option):
        self.option = option
        if option == "":
            self.option = "0"
        elif option != "0":
            self.specified = input("请输入要指定的那个选项（大写小写均可）：").upper()
            if option == "2":
                self.probability = int(input("你选择了策略 2 ，请指定出现概率（0~100，输入纯数字）："))

    def init_count_answer(self):
        result = {}
        for index, choice in enumerate(self.choices):
            result[self.choice_names[index]] = 0

        return result

    def answer_question(self):
        element, index = None, None
        if self.option == "0":
            element, index = self.single_choice_like_option0(self.answer_elements)
        elif self.option == "1":
            element, index = self.single_choice_like_option1(self.answer_elements, self.specified)
        elif self.option == "2":
            element, index = self.single_choice_like_option2(self.answer_elements, self.specified)

        choice = self.choice_names[index]
        print(f"选择了：{choice}")
        self.count_answer[choice] += 1
        element.click()
