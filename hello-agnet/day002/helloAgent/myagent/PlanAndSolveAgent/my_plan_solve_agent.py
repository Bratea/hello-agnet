#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 14:58
# @Author  : 小陈
# @File    : my_plan_solve_agent.py
# @Software: PyCharm
"""

# my_plan_solve_agent.py
import ast
import re
from typing import Optional, Dict, List
from hello_agents import PlanAndSolveAgent, HelloAgentsLLM, Config, Message


class MyPlanAndSolveAgent(PlanAndSolveAgent):
    """
    自定义 Plan and Solve Agent - 手动实现"规划 -> 分步执行"的逻辑。
    """

    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
        custom_prompts: Optional[Dict[str, str]] = None
    ):
        # 校验 custom_prompts 是否包含必需的两个 key
        if custom_prompts is not None:
            required_keys = {"planner", "executor"}
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
            custom_prompts=custom_prompts
        )

        # 保存提示词模板：用户自定义优先，否则使用父类默认模板
        self.planner_prompt = custom_prompts.get("planner") if custom_prompts else self.planner.prompt_template
        self.executor_prompt = custom_prompts.get("executor") if custom_prompts else self.executor.prompt_template

        print(f"✅ {name} 初始化完成")

    def run(self, input_text: str, **kwargs) -> str:
        """运行 Plan and Solve Agent：先生成计划，再逐步执行"""
        print(f"\n🤖 {self.name} 开始处理问题: {input_text}")

        # 1. 生成计划
        plan = self._make_plan(input_text, **kwargs)
        if not plan:
            final_answer = "无法生成有效的行动计划，任务终止。"
            print(f"\n--- 任务终止 ---\n{final_answer}")
            self.add_message(Message(input_text, "user"))
            self.add_message(Message(final_answer, "assistant"))
            return final_answer

        print(f"\n✅ 计划已生成: {plan}")

        # 2. 执行计划
        final_answer = self._execute_plan(input_text, plan, **kwargs)

        # 3. 保存对话历史
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_answer, "assistant"))

        print(f"\n--- 最终结果 ---\n{final_answer}")
        return final_answer

    def _make_plan(self, question: str, **kwargs) -> List[str]:
        """调用 LLM 生成步骤计划，并解析为 Python 列表"""
        print("\n--- 正在生成计划 ---")
        prompt = self.planner_prompt.format(question=question)
        response = self._call_llm(prompt, **kwargs)
        print(response)

        try:
            # 先尝试从 ```python ... ``` 代码块中提取
            code_block = re.search(r"```python\s*\n?(.*?)\n?```", response, re.DOTALL)
            if code_block:
                plan_str = code_block.group(1).strip()
            else:
                # 再尝试直接匹配 ["...", "..."] 这种列表
                list_match = re.search(r"\[.*\]", response, re.DOTALL)
                if list_match:
                    plan_str = list_match.group(0).strip()
                else:
                    raise ValueError("未找到 Python 列表")

            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except Exception as e:
            print(f"❌ 解析计划时出错: {e}")
            return []

    def _execute_plan(self, question: str, plan: List[str], **kwargs) -> str:
        """按步骤执行计划，返回最终答案"""
        print("\n--- 正在执行计划 ---")
        history = ""
        final_answer = ""

        for i, step in enumerate(plan, 1):
            print(f"\n-> 正在执行步骤 {i}/{len(plan)}: {step}")

            prompt = self.executor_prompt.format(
                question=question,
                plan=plan,
                history=history if history else "无",
                current_step=step
            )
            response = self._call_llm(prompt, **kwargs)
            final_answer = response

            print(f"✅ 步骤 {i} 完成: {final_answer}")
            history += f"步骤 {i}: {step}\n结果: {final_answer}\n\n"

        return final_answer

    def _call_llm(self, prompt: str, **kwargs) -> str:
        """调用 LLM 获取响应"""
        messages = [{"role": "user", "content": prompt}]
        response = self.llm.invoke(messages, **kwargs)
        return response or ""
