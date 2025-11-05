from .generic_agent import GenericAgent
from .tools.tools import *



# The savings account agent finds the savings which match the query

SAVINGS_PROMPT = """Answer the following question as best you can. You have access to the following tools:

account_finder_tool: Get information about different savings account
    Input
        - search: A prompt explain what account you are trying to find. ONLY GIVE DETAILS OF THE ACCOUNT, NOT THAT YOU WANT THE BEST ONE

interest_calc: Calculate the growth of an investment over a few years.
    Input
        - rate (float): the interest rate as a number (eg 5%=0.05)
        - investment (float): the initial investment
        - time (float): the number of years to leave the investment for

The way you use the tools is by specifying python code.
Specifically, this python code should be a single function call to the tool that you wish to use.

The only values that should be in the "action" field are:
account_finder_tool: Run a search for the given term, args: {"search": {type: str}}
interest_calc: Calculate the growth of an investment over a few years, args: {"rate": {type: float}, "investment": {type: float}, "time": {type: float}}
example uses :

account_finder_tool("Variable rate instant access ISA"),

interest_calc(0.04, 1000, 1)


ALWAYS use the following exact format:

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:$Python Function Call

Now begin, remember to use the EXACT format as above.
Once you have sufficient information to provide an answer give a natural answer to the question.

Task: """

class SavingsAgent(GenericAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        super().__init__(model_name=model_name, main_prompt=SAVINGS_PROMPT, tools=["account_finder_tool", "interest_calc"])
    # Additional methods specific to SavingsAgent can be added here

    def run_agent(self, task:str, trace: bool = False) -> str:
        prompt = self.prompt_builder() + task

        while True:
            # Get response from the model
            response = self.get_response(prompt)
            if response is None:
                return "Error: No response from model."
            if trace:
                print(f"Agent response: {response}")


            tool_call = self.is_tool_used(response)
            if tool_call != "":
                # Execute the tool call
                try:
                    tool_result = str(eval(tool_call))
                except Exception as e:
                    tool_result = f"Error executing tool: {e}"

                if trace:
                    print(f"Tool call: {tool_call}")
                    print(f"Tool result: {tool_result}")

                # Append the tool result to the prompt for the next iteration
                prompt += f"\nAgent response: {response}\nThe outcome of the usage of the tool use was {tool_result}"
            else:
                # No tool used, return the final answer
                return response
