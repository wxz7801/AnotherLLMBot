from src.config_loader import k_config  # 导入 config对象
from src.k_llm.models import chat_model
from src.k_llm.prompt_templates import rag_cat_girl, cat_girl

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


# Define the function that calls the model
def call_chat_model(state: MessagesState):
    use_rag = k_config["use_rag"]
    if use_rag:
        from src.k_llm.rag import retriever, format_docs

        prompt_template = rag_cat_girl
        # prompt_template = hub.pull("rlm/rag-prompt")
        
        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template 
            | chat_model 
        )

        # 将 state["messages"] 转换为字符串
        messages_text = "\n".join([msg.content for msg in state["messages"]])
        response = chain.invoke(messages_text)
    else:
        prompt_template = cat_girl
        chain = prompt_template | chat_model
        response = chain.invoke(state["messages"])

    # Update message history with response:
    return {"messages": response}


class ChatBot():
    def __init__(self):
        self.name = "ChatBot"
        self.output_parser = StrOutputParser()
        
        # Define a new graph
        self.workflow = StateGraph(state_schema=MessagesState)

        # Define the (single) node in the graph
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", call_chat_model)

        # Add memory
        memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=memory)

        self.app_config = {"configurable": {"thread_id": "1"}}
        
    
    def reply(self, user_input):
        # 调用 invoke 方法生成响应
        try:
            output = self.app.invoke({"messages": user_input}, self.app_config)
            print("output:", output)
            print("==============================\n")
            invoke_response = output["messages"][-1].content
            print("invoke_response:", invoke_response)
            message = invoke_response.split("</think>")[-1].split('\n')[-1]
            return message
        except Exception as e:
            return "发生错误:", e

chat_bot = ChatBot()