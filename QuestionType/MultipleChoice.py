from selenium.webdriver.remote.webelement import WebElement
import itertools
import random
import numpy as np
from scipy.stats import norm

from Question import Question


class MultipleChoice(Question):
    def __init__(self, title: str, q_type: str, choices: list[str], relation: list[str], elements: list[WebElement],
                 next_page_element: WebElement):
        super().__init__(title, q_type, choices, relation, elements, next_page_element)
        self.option_name = {
            "0": "完全随机",
            "1": "标准的正态分布",
            "2": "指定出现概率，其余选项等可能出现"
        }

    def set_min_select(self, min_select):
        self.min_select = min_select

    def __str__(self):
        result = f"题目：{self.title}\n题型：{self.q_type}"
        result += f"，选项共{len(self.choices)}个：\n"
        if self.min_select is not None:
            result += f"注意：本题有最低选择项要求：最少选择{self.min_select}项\n"
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
            self.specified = input("请输入要指定的那几个选项（大写小写均可，不用分隔，如：ACD）：").upper()
            if option == "2":
                self.probability = int(input("你选择了策略 2 ，请指定出现概率（0~100，输入纯数字）："))

    def init_count_answer(self):
        return {}

    def option0(self):
        # 获取所有可能的选取结果
        all_combinations = []
        for r in range(1, len(self.answer_elements) + 1):
            combinations = list(itertools.combinations(self.answer_elements, r))
            all_combinations.extend(combinations)

        # 过滤掉长度低于 min_select 的组合
        if self.min_select is not None:
            all_combinations = [comb for comb in all_combinations if len(comb) >= int(self.min_select)]

        # 随机抽取一个结果
        selected_combination = random.choice(all_combinations)

        # 获取该结果的索引
        indices = [self.answer_elements.index(element) for element in selected_combination]

        return list(selected_combination), indices

    def option1(self):
        # 获取所有可能的选取结果
        all_combinations = []
        for r in range(1, len(self.answer_elements) + 1):
            combinations = list(itertools.combinations(self.answer_elements, r))
            all_combinations.extend(combinations)

        # 过滤掉长度低于 min_select 的组合
        if self.min_select is not None:
            all_combinations = [comb for comb in all_combinations if len(comb) >= int(self.min_select)]

        # 根据指定字符串生成目标组合
        specified_combination = tuple(self.answer_elements[ord(ch) - ord('A')] for ch in self.specified)

        # 获取组合数量
        n = len(all_combinations)

        # 创建选项的位置，使得指定元素位于均值（0）位置
        positions = np.linspace(-3, 3, n)

        # 计算标准正态分布的概率密度
        probabilities = norm.pdf(positions)

        # 将概率归一化，使其和为1
        probabilities /= np.sum(probabilities)

        # 找到指定组合在所有组合中的索引
        specified_index = all_combinations.index(specified_combination)

        # 确保指定元素具有最高的概率
        probabilities[specified_index] = max(probabilities)

        # 重新归一化，使其和为1
        probabilities /= np.sum(probabilities)

        # 根据计算出的概率分布随机选择一个选项
        chosen_index = random.choices(range(n), weights=probabilities, k=1)[0]
        chosen_combination = all_combinations[chosen_index]

        # 获取该结果的索引
        indices = [self.answer_elements.index(element) for element in chosen_combination]

        return list(chosen_combination), indices

    def option2(self):
        # 获取所有可能的选取结果
        all_combinations = []
        for r in range(1, len(self.answer_elements) + 1):
            combinations = list(itertools.combinations(self.answer_elements, r))
            all_combinations.extend(combinations)

        # 过滤掉长度低于 min_select 的组合
        if self.min_select is not None:
            all_combinations = [comb for comb in all_combinations if len(comb) >= int(self.min_select)]

        # 根据指定字符串生成目标组合
        specified_combination = tuple(self.answer_elements[ord(ch) - ord('A')] for ch in self.specified)

        # 找到指定组合在所有组合中的索引
        specified_index = all_combinations.index(specified_combination)

        # 初始化所有组合的概率
        n = len(all_combinations)
        probabilities = np.full(n, (100 - self.probability) / (n - 1))

        # 设置指定组合的概率
        probabilities[specified_index] = self.probability

        # 将概率归一化，使其和为1
        probabilities /= np.sum(probabilities)

        # 根据计算出的概率分布随机选择一个选项
        chosen_index = random.choices(range(n), weights=probabilities, k=1)[0]
        chosen_combination = all_combinations[chosen_index]

        # 获取该结果的索引
        indices = [self.answer_elements.index(element) for element in chosen_combination]

        return list(chosen_combination), indices

    def answer_question(self):
        elements, indexs = None, None
        if self.option == "0":
            elements, indexs = self.option0()
        elif self.option == "1":
            elements, indexs = self.option1()
        elif self.option == "2":
            elements, indexs = self.option2()

        choices = ""
        for index in indexs:
            choices += self.choice_names[index]

        print(f"选择了：{choices}")
        if choices not in self.count_answer:
            self.count_answer[choices] = 1
        else:
            self.count_answer[choices] += 1

        for element in elements:
            element.click()
