from day001.HelloAgentsLLM import HelloAgentsLLM
from day001.Reflection.ReflectionAgent import ReflectionAgent


if __name__ == '__main__':
    # 1. 初始化 LLM 客户端
    llm = HelloAgentsLLM()

    # 2. 初始化 Reflection 智能体
    agent = ReflectionAgent(llm_client=llm, max_iterations=3)

    # 3. 运行智能体
    task = "编写一个函数，判断一个正整数是否为素数"
    print(f"任务: {task}\n")
    final_code = agent.run(task)

    if final_code:
        print(f"\n最终代码:\n{final_code}")
