import agents
from teams.agents import Message


def main():
    sales = agents.Agent(
        agent_id="1",
        agent_name="Sales",
        system="You are Agent 1, you are a helpful assistant for all your sales needs. Our company sales dog food, cat food, and bird food.",
    )

    customer = agents.Agent(
        agent_id="2",
        agent_name="Customer",
        system="You are Agent 2, you are a customer looking to buy pet food. You are speaking with Agent 1 about the products they sell."
    )

    message = None
    # for i in range(10):
    #     message = customer.completion(message)
    #     print("Customer:", message.content)
    #     message.role = "user"
    #     message = sales.completion(message)
    #     print("Sales:", message.content)
    # pass

    message = sales.completion()



if __name__ == "__main__":
    main()