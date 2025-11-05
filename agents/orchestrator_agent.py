import re
from agents.generic_agent import GenericAgent
# The triage agent will ask questions until it understands the ask, it will then generate a prompt for the other agent

ORCHESTRATOR_PROMPT = """You are an orchestrator agent that's is to find out what the user is enquiring about and then hand over to the relevant agent. You will ask the user a series of questions to understand their needs. Once you have enough information, you will return python code that runs the correct agent. Make sure that your first message explains what you can do and asks the user what they need help with.

You have access to the following agents:
1. Savings Agent: Finds the best savings account for the user. Run with savings_agent()
2. Credit Agent: Finds the best credit card for the user. Run with credit_agent()

When calling an agent, use exactly the following format:
HANDOFF: <agent_name>()

For example, to call the savings agent, you would write:
HANDOFF: savings_agent()


The information you have so far is:
"""


class Orchestrator(GenericAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        super().__init__(model_name=model_name, main_prompt=ORCHESTRATOR_PROMPT, tools=[])

    def run_agent(self):
        while True:
            # Generate the response
            response = self.get_response(self.main_prompt)

            if response != None:
                next_question=re.search(r"(savings_agent\(\))|(credit_agent\(\))", response)

                # No tool is called then the agent has sufficient info so it has produced the final prompt to be used by the savings agent
                if next_question != None:
                    self.main_prompt = self.prompt_builder()
                    return next_question.group()

                print(response)
                answer = input("ANSWER: ")

                # Append the answer to the prompt for the next iteration
                self.main_prompt += f"\n{response}: ANSWER: {answer}"
            else:
                return "ERROR: LLM failed to produce answer"
