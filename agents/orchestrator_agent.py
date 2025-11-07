import re
from agents.generic_agent import GenericAgent
from agents.savings_agent import *
from agents.triage_agent import *
# The triage agent will ask questions until it understands the ask, it will then generate a prompt for the other agent

ORCHESTRATOR_PROMPT = """You are an orchestrator agent that's is to find out what the user is enquiring about and then hand over to the relevant agent. You will ask the user a series of questions to understand their needs. Once you have enough information, you will return python code that runs the correct agent. Make sure that your first message explains what you can do and asks the user what they need help with. You do not need to go into any more depth once you understand what agent you need to hand off to.

You have access to the following agents:
1. savings_triage: Finds the best savings account for the user. Run with savings_triage
1. credit_triage: Finds the best credit card account for the user. Run with credit_triage

When calling an agent, use exactly the following format:
HANDOFF: <agent_name>()

For example, to call the savings agent, you would write:
HANDOFF: SavingsTriageAgent()


The information you have so far is:
"""


class Orchestrator(GenericAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        super().__init__(model_name=model_name, main_prompt=ORCHESTRATOR_PROMPT, tools=[])

        self.current_agent = self.run_agent

        self.triage_agents_to_handoff = ['savings_triage', 'credit_triage']

        # Agents
        self.savings_triage = SavingsTriageAgent()
        self.savings_search = SavingsAgent()
        self.credit_triage = CreditTriageAgent()

    def run_agent(self):
        while True:
            # Generate the response
            response = self.get_response(self.prompt)

            if response != None:
                #TODO: Change Regex
                next_question=re.search(r"(savings_triage)|(credit_triage)", response)

                # No tool is called then the agent has sufficient info so it has produced the final prompt to be used by the savings agent
                if next_question != None:
                    self.prompt = self.prompt_builder()

                    # Move to next agent
                    if next_question.group() in self.triage_agents_to_handoff:
                        print("Next agent: " + next_question.group())
                        self.current_agent = lambda : self.run_triage_agent(eval("self." + next_question.group()))
                        return
                print(response)
                answer = input("ANSWER: ")

                # Append the answer to the prompt for the next iteration
                self.prompt += f"\n{response}: ANSWER: {answer}"
            else:
                return "ERROR: LLM failed to produce answer"

    def run_triage_agent(self, agent:TriageAgent):
        response = agent.run_agent()

        if response != agent.llm_error:
            self.current_agent = lambda : self.run_search_agent(response, self.savings_search)

    def run_search_agent(self, task, agent:SearchAgent):
        output = agent.run_agent(task, True)
        self.current_agent = self.run_agent
