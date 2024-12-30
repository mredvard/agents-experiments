from openai import OpenAI

class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class Chat:
    def __init__(self, messages: list[Message]):
        self.messages = messages

    def to_dict(self):
        return [message.to_dict() for message in self.messages]

    def add_message(self, message: Message):
        self.messages.append(message)


class Agent:
    def __init__(self, agent_id, agent_name, system, agents:list=None, chat=None):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.client = OpenAI()
        self.system = system
        self.agents = {}
        if agents:
            for agent in agents:
                self.agents[agent.agent_id] = agent

        if chat is None:
            self.chat = Chat([])
        else:
            self.chat = chat

    def to_dict(self):
        return {"agent_id": self.agent_id, "agent_name": self.agent_name}

    def completion(self, prompt: Message = None) -> Message:
        if prompt:
            self.chat.add_message(prompt)
        messages = [{"role": "system", "content": self.system}]
        messages.extend(self.chat.to_dict())
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.9
        )
        message = completion.choices[0].message.to_dict()
        self.chat.add_message(Message(message["role"], message["content"]))
        return Message(message["role"], message["content"])

    def invoke_agent(self, agent_id, prompt):
        agent = self.agents[agent_id]
        return agent.completion(prompt)



class Conversation:
    def __init__(self, agents, max_iterations=10):
        self.agents = agents
        self.chat = Chat([])
        self.max_iterations = max_iterations

    def to_dict(self):
        return {"agents": [agent.to_dict() for agent in self.agents], "chat": self.chat.to_dict()}

    def add_message(self, agent, content):
        self.chat.messages.append(Message(agent.agent_name, content))

    def run(self):
        iterations = 0
        while True:
            for agent in self.agents:
                self.add_message(agent, agent.completion(self.chat, agent.agent_name))
                print(self.chat.messages[-1].content)
            if self.chat.messages[-1].content == "Goodbye":
                break
            elif iterations > self.max_iterations:
                break
            iterations += 1