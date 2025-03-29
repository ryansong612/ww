from openai import OpenAI


class Model:
    def __init__(self, name="user"):
        self.api_key = "sk-39e64084ea4742948630df69faef0104"
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        self.messages = []
        self.model = "deepseek-chat"
        self.max_tokens=2000
        self.user_name = name
    
    def chat(self, message_body: str):
        self.messages.append({
            "role": "user",
            "content": message_body,
            "name": self.user_name
        })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
        )
        top_choice = response.choices[0].message
        self.messages.append(top_choice)
        return top_choice.content

if __name__ == "__main__":
    model = Model()
    model.chat("你好,请记住数字一，后面回答只能说一")
    model.chat("1+1等于几")
    print(model.messages)

