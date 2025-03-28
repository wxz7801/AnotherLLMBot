from src.k_llm.tools import extract_reasoning
from src.k_llm.models import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """判断用户消息的主题，如果没有明显主题请回复"无主题"，要求：
            1. 主题通常2-4个字，必须简短，要求精准概括，不要太具体。
            2. 建议给出多个主题，之间用英文逗号分割。只输出主题本身就好，不要有前后缀。"""),
        ("user", "{input}")
    ]
)


class TopicIdentifier():
    def __init__(self):
        self._output_parser = StrOutputParser()
        self._chain = _prompt | chat_model | self._output_parser
    
    def identify_topic(self, user_input):
        response = self._chain.invoke(user_input)
        topic, _ = extract_reasoning(response)

        # 解析主题字符串为列表
        topic_list = [t.strip() for t in topic.split(",") if t.strip()]
        
        return topic_list
    
    def reply(self, user_input):
        response = self._chain.invoke(user_input)
        
        content, _ = extract_reasoning(response)
        return content

    
topic_identifier = TopicIdentifier()