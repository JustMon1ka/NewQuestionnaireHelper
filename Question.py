import random
from typing import Union, Tuple, List, Any

import numpy as np
from selenium.webdriver.remote.webelement import WebElement


def standard_normal_pdf(x, mu=0, sigma=1):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


class Question:
    def __init__(self, title: str, q_type: str, choices: list[str], relation: list[str],
                 elements: any,
                 next_page_element: WebElement):
        self.title = title
        self.q_type = q_type
        self.choices = choices  # 如果是填空题，则没有选项
        self.relation = relation
        self.min_select = None  # 只有多选类型的题目才有这个属性
        self.answer_elements = elements
        self.next_page_element = next_page_element
        self.choice_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.option = None
        self.option_name = None
        self.specified = None
        self.probability = None
        try:
            self.count_answer = self.init_count_answer()  # 根据题目类型不同而不同
        except:
            ...

    def init_count_answer(self):
        return {}

    def __str__(self):
        ...

    def set_option(self, option):
        self.option = option

    def answer_question(self):
        ...

    def single_choice_like_option0(self, answer_elements) -> tuple[WebElement, int]:
        n = len(answer_elements)
        if n == 0:
            raise ValueError("没有可用的选项元素。")

        # 纯随机选择一个元素的索引
        chosen_index = random.randint(0, n - 1)
        chosen_element = answer_elements[chosen_index]

        return chosen_element, chosen_index

    def single_choice_like_option1(self, answer_elements, specified) -> tuple[WebElement, int]:
        n = len(answer_elements)
        if n == 0:
            raise ValueError("生成选择时失败：没有找到选项按钮.")

        # 创建选项的位置，使得指定元素位于均值（0）位置
        positions = np.linspace(-3, 3, n)
        probabilities = standard_normal_pdf(positions)

        # 将概率归一化，使其和为1
        probabilities /= np.sum(probabilities)

        # 确保指定元素具有最高的概率
        specified_index = int(ord(specified) - ord('A'))
        specified_probability = max(probabilities)
        probabilities[specified_index] = specified_probability
        probabilities /= np.sum(probabilities)  # 重新归一化，使其和为1

        # 根据计算出的概率分布随机选择一个选项
        chosen_index = random.choices(range(n), weights=probabilities, k=1)[0]
        chosen_element = answer_elements[chosen_index]

        return chosen_element, chosen_index

    def single_choice_like_option2(self, answer_elements, specified) -> tuple[WebElement, int]:
        """
        根据指定的概率选出一个元素和它的索引
        """
        n = len(answer_elements)
        if n == 0:
            raise ValueError("没有可用的选项元素。")
        if not (0 <= self.probability <= 100):
            raise ValueError("概率必须在0到100之间。")

        # 计算指定选项和其他选项的概率
        specified_index = int(ord(specified) - ord('A'))
        specified_prob = self.probability / 100.0
        other_prob = (1 - specified_prob) / (n - 1) if n > 1 else 0

        # 构建概率分布列表
        probabilities = [other_prob] * n
        probabilities[specified_index] = specified_prob

        # 根据计算出的概率分布随机选择一个选项
        chosen_index = random.choices(range(n), weights=probabilities, k=1)[0]
        chosen_element = answer_elements[chosen_index]

        return chosen_element, chosen_index

    def generate_answer(self):
        ...

    def reset_elements(self, answer_elements, next_button):
        self.answer_elements = answer_elements
        self.next_page_element = next_button
