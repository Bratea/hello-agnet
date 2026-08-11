#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 10:41
# @Author  : 小陈
# @File    : main.py
# @Software: PyCharm
AI科普电子书
为了理解 CAMEL 框架的角色扮演能力，我们将构建一个具有实际价值的协作案例：
让一位 AI 心理学家与一位 AI 作者合作，共同创作一本关于"拖延症心理学"的短篇电子书。
这个案例体现了 CAMEL 的核心优势，让两个智能体在各自专业领域发挥所长，协作完成单个智能体难以胜任的复杂创作任务。
"""

from colorama import Fore
from day002.CAMEL.RolePlaying import role_play_session
from camel.utils import print_text_animated

def main():
    # 开始协作对话
    chat_turn_limit, n = 30, 0
    # 调用 init_chat() 来获得由 AI 生成的初始对话消息
    input_msg = role_play_session.init_chat()

    while n < chat_turn_limit:
        n += 1
        # step() 方法驱动一轮完整的对话，AI 用户和 AI 助理各发言一次
        assistant_response, user_response = role_play_session.step(input_msg)

        # 检查是否有消息返回，防止对话提前终止
        if assistant_response.msg is None or user_response.msg is None:
            break

        print_text_animated(Fore.BLUE + f"作家 (AI User):\n\n{user_response.msg.content}\n")
        print_text_animated(Fore.GREEN + f"心理学家 (AI Assistant):\n\n{assistant_response.msg.content}\n")

        # 检查任务完成标志
        if "<CAMEL_TASK_DONE>" in user_response.msg.content or "<CAMEL_TASK_DONE>" in assistant_response.msg.content:
            print(Fore.MAGENTA + "✅ 电子书创作完成！")
            break

        # 将助理的回复作为下一轮对话的输入
        input_msg = assistant_response.msg

    print(Fore.YELLOW + f"总共进行了 {n} 轮协作对话")


if __name__ == "__main__":
    main()
