from day001.HelloAgentsLLM import HelloAgentsLLM
from day001.ReAct.ReActAgent import ReActAgent
from day001.ReAct.ToolExecutor import ToolExecutor
from day001.ReAct.search import search


if __name__ == '__main__':
    # 1. 初始化 LLM 客户端
    llm = HelloAgentsLLM()

    # 2. 初始化工具执行器并注册搜索工具
    executor = ToolExecutor()
    executor.registerTool(
        "Search",
        "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。",
        search
    )

    # 3. 初始化 ReAct 智能体
    agent = ReActAgent(llm_client=llm, tool_executor=executor, max_steps=5)

    # 4. 运行智能体
    question = "英伟达最新的GPU型号是什么"
    print(f"问题: {question}\n")
    answer = agent.run(question)

    if answer:
        print(f"\n最终答案: {answer}")
