from selenium.webdriver.remote.webelement import WebElement
import random
from openai import OpenAI

from Question import Question


class Input(Question):
    def __init__(self, title: str, q_type: str, choices: list[str], relation: list[str], elements: WebElement,
                 next_page_element: WebElement):
        super().__init__(title, q_type, choices, relation, elements, next_page_element)
        self.option_name = {
            "0": "随机回答预设的选项",
            "1": "使用GPT-3.5模型帮助回答",
        }
        api_key = ""
        self.client = OpenAI(api_key=api_key)

    def __str__(self):
        result = f"题目：{self.title}\n题型：{self.q_type}\n"
        result += "\n"
        result += f"题目关联：{self.relation}"
        result += "\n"
        result += "请输入此题的答题策略（0：随机回答预设的选项（均代表'无'的意思） | 1：使用GPT-3.5模型帮助回答（响应会比较慢而且不太稳定））：\n"
        return result

    def set_option(self, option):
        self.option = option
        if option == "":
            self.option = "0"

    def option0(self):
        # 存放表示“无”，“没想法”之类的短语
        phrases = [
            "无", "没想法", "不知道", "暂无意见", "暂时没有想法", "无可奉告",
            "目前没有想法", "还没有想法", "无意见", "无异议", "尚未考虑",
            "没有特别意见", "暂无看法", "暂时没有意见", "无法回答", "无特别意见",
            "未能答复", "没有什么要说的", "不确定", "没有答案", "未做决定",
            "暂时无法回答", "没有明确的意见", "未能提供意见", "尚无定论",
            "无法给出答案", "无明确看法", "不清楚", "没有什么想法", "未能确定",
            "没有什么可说的", "目前无看法", "没有什么可补充的", "暂时不便回答",
            "尚未决定", "未考虑清楚", "没有特别的看法", "目前无法给出意见",
            "无法提供答案", "没有具体意见", "无具体意见", "暂无特别看法",
            "无特别看法", "不便回答", "暂时没有任何意见", "目前没有任何想法",
            "无法给出明确答案", "未能给出明确答复"
        ]

        # 随机抽取一个短语
        selected_phrase = random.choice(phrases)

        return selected_phrase

    def option1(self):
        question = self.title + "，请用中文回答我"
        # 调用 OpenAI 的 API 来使用 GPT 模型回答问题
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个问卷填写员，请根据问卷的题目做出相应回答."},
                    {"role": "user", "content": question}
                ],
                max_tokens=512,
                temperature=1
            )
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            return f"Error: {str(e)}"

    def answer_question(self):
        result = ""
        if self.option == "0":
            result = self.option0()
        if self.option == "1":
            result = self.option1()
        print(f"回答了：{result}")
        self.answer_elements.send_keys(result)


