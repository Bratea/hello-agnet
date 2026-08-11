from day001.HelloAgentsLLM import HelloAgentsLLM
from day001.PlanAndSolve.PlanAndSolveAgent import PlanAndSolveAgent


if __name__ == '__main__':
    # 1. 初始化 LLM 客户端
    llm = HelloAgentsLLM()

    # 2. 初始化 Plan-and-Solve 智能体
    agent = PlanAndSolveAgent(llm_client=llm)

    # 3. 运行智能体
    question = "如何从零开始搭建一个基于Python的个人博客网站？"
    print(f"问题: {question}\n")
    agent.run(question)
