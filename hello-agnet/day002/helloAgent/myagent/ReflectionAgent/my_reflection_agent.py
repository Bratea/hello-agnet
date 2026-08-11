#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 14:45
# @Author  : 小陈
# @File    : my_reflection_agent.py
# @Software: PyCharm
"""

# my_reflection_agent.py
from typing import Optional, Dict, List
from hello_agents import ReflectionAgent, HelloAgentsLLM, Config, Message


class MyReflectionAgent(ReflectionAgent):
    """
    自定义 Reflection Agent - 手动实现"生成 -> 反思 -> 优化"的迭代循环。
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        max_iterations: int = 3,
        custom_prompts: Optional[Dict[str, str]] = None
    ):
        # 校验 custom_prompts 是否包含必需的三个 key
        if custom_prompts is not None:
            required_keys = {"initial", "reflect", "refine"}
            missing = required_keys - set(custom_prompts.keys())
            if missing:
                raise ValueError(
                    f"custom_prompts 缺少必需的 key: {missing}。"
                    f"必须包含 {required_keys}"
                )

        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt,
            config=config,
            max_iterations=max_iterations,
            custom_prompts=custom_prompts
        )
        self.max_iterations = max_iterations
        self.attempts: List[str] = []
        self.feedbacks: List[str] = []
        print(f"✅ {name} 初始化完成，最大迭代次数: {max_iterations}")

    def run(self, input_text: str, **kwargs) -> str:
        """运行 Reflection Agent：生成 -> 反思 -> 优化"""
        print(f"\n🤖 {self.name} 开始处理任务: {input_text}")

        # 1. 初始生成
        print("\n--- 初始尝试 ---")
        initial_prompt = self.prompts["initial"].format(task=input_text)
        current_result = self._call_llm(initial_prompt, **kwargs)
        print(current_result)

        # 2. 反思与优化循环
        for i in range(self.max_iterations):
            print(f"\n--- 第 {i + 1}/{self.max_iterations} 轮反思 ---")

            # 2a. 反思
            reflect_prompt = self.prompts["reflect"].format(
                task=input_text,
                content=current_result
            )
            feedback = self._call_llm(reflect_prompt, **kwargs)
            print(f"\n🤔 反思反馈:\n{feedback}")
            self.feedbacks.append(feedback)

            # 2b. 检查是否需要停止
            if "无需改进" in feedback or "no need for improvement" in feedback.lower():
                print("\n✅ 反馈认为结果已无需改进，结束迭代。")
                break

            # 2c. 优化
            refine_prompt = self.prompts["refine"].format(
                task=input_text,
                last_attempt=current_result,
                feedback=feedback
            )
            current_result = self._call_llm(refine_prompt, **kwargs)
            self.attempts.append(current_result)
            print(f"\n✨ 优化后结果:\n{current_result}")

        # 3. 保存对话历史
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(current_result, "assistant"))

        print(f"\n--- 最终结果 ---\n{current_result}")
        return current_result

    def _call_llm(self, prompt: str, **kwargs) -> str:
        """调用 LLM 获取响应"""
        messages = [{"role": "user", "content": prompt}]
        response = self.llm.invoke(messages, **kwargs)
        return response or ""

    def show_trajectory(self):
        """打印所有反思反馈和优化记录"""
        print("\n--- 反思轨迹 ---")
        for idx, feedback in enumerate(self.feedbacks, 1):
            print(f"\n第 {idx} 轮反馈:\n{feedback}")
        if self.attempts:
            print("\n--- 优化记录 ---")
            for idx, attempt in enumerate(self.attempts, 1):
                print(f"\n第 {idx} 轮优化结果:\n{attempt}")
