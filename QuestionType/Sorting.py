from selenium.webdriver.remote.webelement import WebElement
import itertools
import random
import numpy as np
from scipy.stats import norm

from Question import Question


class Sorting(Question):
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
        result += f"，排序项共{len(self.choices)}个：\n"
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
            self.specified = input("请输入要指定的排序序列（大写小写均可，不用分隔，如：BACD）：").upper()
            if option == "2":
                self.probability = int(input("你选择了策略 2 ，请指定出现概率（0~100，输入纯数字）："))

    def init_count_answer(self):
        return {}

    def option0(self):
        # 获取所有元素的排列方式
        all_permutations = list(itertools.permutations(self.answer_elements))

        # 随机抽取一个排列
        selected_permutation = random.choice(all_permutations)

        # 获取该排列的索引
        indices = [self.answer_elements.index(element) for element in selected_permutation]

        return list(selected_permutation), indices

    def option1(self):
        # 获取所有元素的排列方式
        all_permutations = list(itertools.permutations(self.answer_elements))

        # 根据指定字符串生成目标排列
        if self.specified:
            specified_permutation = tuple(self.answer_elements[ord(ch) - ord('A')] for ch in self.specified)
        else:
            specified_permutation = all_permutations[0]  # 如果未指定，默认第一个排列

        # 获取排列数量
        n = len(all_permutations)

        # 创建选项的位置，使得指定元素位于均值（0）位置
        positions = np.linspace(-3, 3, n)

        # 计算标准正态分布的概率密度
        probabilities = norm.pdf(positions)

        # 将概率归一化，使其和为1
        probabilities /= np.sum(probabilities)

        # 找到指定排列在所有排列中的索引
        specified_index = all_permutations.index(specified_permutation)

        # 确保指定元素具有最高的概率
        probabilities[specified_index] = max(probabilities)

        # 重新归一化，使其和为1
        probabilities /= np.sum(probabilities)

        # 根据计算出的概率分布随机选择一个排列
        chosen_index = random.choices(range(n), weights=probabilities, k=1)[0]
        chosen_permutation = all_permutations[chosen_index]

        # 获取该排列的索引
        indices = [self.answer_elements.index(element) for element in chosen_permutation]

        return list(chosen_permutation), indices

    def option2(self):
        # 获取所有元素的排列方式
        all_permutations = list(itertools.permutations(self.answer_elements))

        # 根据指定字符串生成目标排列
        if self.specified:
            specified_permutation = tuple(self.answer_elements[ord(ch) - ord('A')] for ch in self.specified)
        else:
            specified_permutation = all_permutations[0]  # 如果未指定，默认第一个排列

        # 找到指定排列在所有排列中的索引
        specified_index = all_permutations.index(specified_permutation)

        # 初始化所有排列的概率
        n = len(all_permutations)
        probabilities = np.full(n, (100 - self.probability) / (n - 1))

        # 设置指定排列的概率
        probabilities[specified_index] = self.probability

        # 将概率归一化，使其和为1
        probabilities /= np.sum(probabilities)

        # 根据计算出的概率分布随机选择一个排列
        chosen_index = random.choices(range(n), weights=probabilities, k=1)[0]
        chosen_permutation = all_permutations[chosen_index]

        # 获取该排列的索引
        indices = [self.answer_elements.index(element) for element in chosen_permutation]

        return list(chosen_permutation), indices

    def option_fix(self):
        indices = [self.answer_elements.index(element) for element in self.answer_elements]
        return self.answer_elements, indices

    def answer_question(self):
        # elements, indexs = None, None
        # if self.option == "0":
        #     elements, indexs = self.option0()
        # elif self.option == "1":
        #     elements, indexs = self.option1()
        # elif self.option == "2":
        #     elements, indexs = self.option2()
        elements, indexs = self.option_fix()

        choices = ""
        for index in indexs:
            choices += self.choice_names[index]

        print(f"选择的排序顺序是：{choices}(由于排序题点击选项时选项会发生位移，所以暂时用完全正序替代)")
        if choices not in self.count_answer:
            self.count_answer[choices] = 1
        else:
            self.count_answer[choices] += 1

        for element in elements:
            element.click()
