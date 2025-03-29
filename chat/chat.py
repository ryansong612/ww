# This is the API interface for the chat component of the robot product
import jieba.analyse
from model import Model
from recog import RecognizerAdaptor

class ChatAPI:
    def __init__(self):
        self.model = Model()
        self.recognizer = RecognizerAdaptor()

    def extract_keyword(self, s: str) -> str:
        keywords = jieba.analyse.extract_tags(s, topK=5, withWeight=True)
        return keywords
    
    def stream_chat(self):
        user_input = self.recognizer.recognize_from_mic(language="zh-CN")
        print(f"User: {user_input}")
        response = self.model.chat(user_input)
        print(f"Bot: {response}")

    
    
if __name__ == "__main__":
    chat = ChatAPI()
    # print(chat.extract_keyword("人善被狗欺"))
    chat.stream_chat()
    