from langchain_core.messages import HumanMessage 
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# langchain_core: high level framework that allows us to build AI application
# langgraph: complex framework that allows us to build AI agent
# langchain_openai: allows us to use open AI within LangChain and LangGraph

load_dotenv()
@tool
def calulator(a: float, b: float) -> str:
    """Userful for performing basic arithmeric calulations with numbers"""
    print("Tool had been called.")
    return f"The sum of {a} and {b} is {a + b}"



def main():
    model = ChatOpenAI(temperature=0)

    #Tool is some external service that the agent can call to, and use it
    tools = [calulator]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant.Type 'quit' to exit." )
    print("You can ask me to perform calculations or chat with me." )

    while True:
        user_input = input("\nYou: ").strip()
        if user_input == "quit":
            break
        print("\nAssistant: ", end="")

        #chunks are essentially parts of a response coming from our agent
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
            
            print()

if __name__ == "__main__":
    main()

