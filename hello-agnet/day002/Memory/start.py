#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2026/8/8 15:53
# @Author  : 小陈
# @File    : start.py
# @Software: PyCharm
"""

import json
import os
# 配置好同级文件夹下.env中的大模型API
from dotenv import load_dotenv
from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
from hello_agents.core.message import Message
from hello_agents.tools import MemoryTool, RAGTool

load_dotenv(override=True)


# 创建LLM实例
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7
)


# 创建工具注册表
tool_registry = ToolRegistry()

# 添加记忆工具（只启用 working 记忆，不需要 Embedding 依赖）
memory_tool = MemoryTool(
    user_id="user123",
    memory_types=["working"]
)
tool_registry.register_tool(memory_tool)

# RAG工具需要 Qdrant 向量数据库和 Embedding 模型依赖，这里暂不启用
# rag_tool = RAGTool(knowledge_base_path="./knowledge_base")
# tool_registry.register_tool(rag_tool)


class NativeToolAgent(SimpleAgent):
    """
    使用 OpenAI 原生 function calling 的 Agent。
    比框架默认的字符串 '[TOOL_CALL:...]' 解析更稳定，
    能可靠地触发 memory 等工具。
    """

    def _tools_to_openai_format(self):
        """把注册表里的工具转成 OpenAI functions/tools 格式。"""
        openai_tools = []
        for tool in self.tool_registry.get_all_tools():
            properties = {}
            required = []
            for p in tool.get_parameters():
                json_type = p.type if p.type in ("string", "integer", "number", "boolean") else "string"
                properties[p.name] = {"type": json_type, "description": p.description}
                if p.required:
                    required.append(p.name)

            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
            })
        return openai_tools

    def _execute_tool_call(self, tool_call):
        """执行单个 tool_call。"""
        tool_name = tool_call.function.name
        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            return f"❌ 未找到工具 '{tool_name}'"

        try:
            args = json.loads(tool_call.function.arguments)
            return tool.run(args)
        except Exception as e:
            return f"❌ 工具 '{tool_name}' 执行失败: {e}"

    def run(self, input_text: str, max_tool_iterations: int = 3, **kwargs):
        """运行 Agent，支持原生 function calling。"""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        for msg in self._history:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": input_text})

        # 没启用工具时直接走 LLM
        if not self.enable_tool_calling:
            response_text = self.llm.invoke(messages, **kwargs)
            self.add_message(Message(input_text, "user"))
            self.add_message(Message(response_text, "assistant"))
            return response_text

        tools = self._tools_to_openai_format()
        final_response = ""

        for _ in range(max_tool_iterations):
            # 直接调底层 OpenAI 客户端，保留完整 message（含 tool_calls）
            response = self.llm._client.chat.completions.create(
                model=self.llm.model,
                messages=messages,
                tools=tools,
                temperature=kwargs.get("temperature", self.llm.temperature),
                max_tokens=kwargs.get("max_tokens", self.llm.max_tokens),
            )
            message = response.choices[0].message

            if not message.tool_calls:
                final_response = message.content or ""
                break

            # 记录 assistant 的 tool_calls
            messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            # 执行每个工具调用并把结果回传
            for tc in message.tool_calls:
                result = self._execute_tool_call(tc)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result)
                })

        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_response, "assistant"))
        return final_response


# 创建Agent（必须在构造时传入 tool_registry，否则不会启用工具调用）
agent = NativeToolAgent(
    name="智能助手",
    llm=llm,
    system_prompt=(
        "你是一个有记忆能力的AI助手。请严格遵守以下规则：\n"
        "1. 当用户要求你记住某些信息时，你必须先调用 memory 工具存储下来。\n"
        "2. 当用户询问之前的信息时，你必须先调用 memory 工具检索。\n"
        "3. 不要口头说你记住了或你记得，除非你已经完成了工具调用并看到了结果。\n"
    ),
    tool_registry=tool_registry
)

# 第一轮：让 Agent 记住用户信息
print("===== 第一轮 =====")
response1 = agent.run("你好！请记住我叫张三，我是一名Python开发者", temperature=0.0)
print(response1)

# 兜底：如果 LLM 没有真正调用工具存储，手动存一次
search_result = memory_tool.run({
    "action": "search",
    "query": "张三 Python开发者",
    "memory_type": "working"
})
if "未找到" in search_result:
    print("\n[系统兜底] 检测到记忆未存入，手动补存...")
    memory_tool.run({
        "action": "add",
        "content": "用户叫张三，是一名Python开发者",
        "memory_type": "working",
        "importance": 0.8
    })

# 第二轮：测试是否记住了
print("\n===== 第二轮 =====")
response2 = agent.run("你还记得我是谁吗？", temperature=0.0)
print(response2)
