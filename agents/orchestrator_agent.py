import re
from agents.generic_agent import GenericAgent
from agents.search_agent import *
from agents.triage_agent import *
# The triage agent will ask questions until it understands the ask, it will then generate a prompt for the other agent

ORCHESTRATOR_PROMPT = """You are an orchestrator agent that's is to find out what the user is enquiring about and then hand over to the relevant agent. Open the chat with an introduction and explain what you can help with.
Once you know the broad area the user is equiring about, hand off to the relevant agent using the instructions below. DO NOT ATTEMPT TO GAIN ANY FURTHER INFORMATION.

You have access to the following agents:
1. savings_triage: Finds the best savings account for the user. Run with savings_triage
2. credit_triage: Finds the best credit card account for the user. Run with credit_triage

When calling an agent, use exactly the following format:
HANDOFF: <agent_name>()

For example, to call the savings agent, you would write:
HANDOFF: savings_triage

For example, to call the savings agent, you would write:
HANDOFF: credit_triage

If the user decides to end the chat write exactly the following: ENDCHAT
The information you have so far is:
"""


class Orchestrator(GenericAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash-lite"):
        super().__init__(model_name=model_name, main_prompt=ORCHESTRATOR_PROMPT, tools=[])

        # Current agent - this function changes over time depending on the agent currently being used
        self.current_agent = self.run_agent

        self.triage_agents_to_handoff = ['savings_triage', 'credit_triage']

        # Create regex for these:
        self.triage_agents_to_handoff_regex = '('+ ')|('.join(map(str, self.triage_agents_to_handoff))+')'

        # Agents
        self.savings_triage = SavingsTriageAgent()
        self.credit_triage = CreditTriageAgent()

    def run_agent(self, user_input: str | None = None, debug=False):
        """Run the orchestrator agent. It's goal is to determine which agent the user needs to be handed off to.
        Once it knows which agent the user needs, it changes the function that self.current_agent calls to self.run_triage_agent

        Args:
            user_input (str | None, optional): The users input, answer to the question it asks. Defaults to None.

        Returns:
            str: The orchestrators response
        """
        # Add user input to response
        if user_input != None:
            self.prompt += f"User: {user_input}\n"
        # Generate the response
        response = self.get_response(self.prompt)

        if response != None:
            #TODO: Change Regex
            next_question=re.search(self.triage_agents_to_handoff_regex, response)

            # No tool is called then the agent has sufficient info so it has produced the final prompt to be used by the savings agent
            if next_question != None:
                self.prompt = self.prompt_builder()

                # Move to next agent
                if next_question.group() in self.triage_agents_to_handoff:
                    if debug:
                        print("Moving to next agent: " + next_question.group())
                    self.current_agent = lambda x, d : self.run_triage_agent(eval("self." + next_question.group()), x, d)

                    response = self.current_agent(None, debug)

                    return response

            # Append the answer to the prompt for the next iteration
            self.prompt += f"\n Agent: {response}"

            return response
        else:
            return "ERROR: LLM failed to produce answer"

    def run_triage_agent(self, agent:TriageAgent, user_input: str, debug=False):
        """Run the triage agent to ask questions to send to the savings/credit card agents

        Args:
            agent (TriageAgent): _description_
            user_input (str): _description_

        Returns:
            _type_: _description_
        """
        response, next_question = agent.run_agent(user_input, debug)

        # If no next question we move on to next agent
        if next_question == None:
            # Agent has finished asking questions and has found answer. Reset to orchestrator
            self.current_agent = self.run_agent

            # Run agent to see what the user wants to do next
            response += "COMPLETE"

        return response
