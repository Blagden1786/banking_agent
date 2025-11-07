# The tools the agents can use.

# Dummy search tool
def dummy_search_tool(search_term:str) -> str:
    return f"Natwest: 3.5% fixed, Monzo: 5% fixed, Suffolk Building Society: 5% variable"

# Tool to calculate return on investment
def interest_calc(rate, investment, time):
    return investment*(1+rate)**time


# Overall regex to match the functions
match_num = r'[+-]?(?:\d*\.\d+|\d+)'

# Regexes for each tool
available_tools_regex = {
    "dummy_search_tool":r'(dummy_search_tool\(".*"\))',
    "search_tool" : r'(self.search_tool\((search=)*((".*")|(\'.*\'))\))',
    "interest_calc": fr'(interest_calc\((rate=)*{match_num}\,( )*(investment=)*{match_num}\,( )*(time=)*{match_num}(/{match_num})*\))'
}



## Prompting
TOOL_PROMPT_START = """Complete the task given as best as you can. You have access to the following tools:\n"""

TOOL_PROMPT_END = """The way you use the tools is by specifying python code.
Specifically, this python code should be a single function call to the tool that you wish to use.
Example uses :

self.search_tool("Variable rate instant access ISA"),

interest_calc(0.04, 1000, 1)

-----------\n"""

# Descriptions of the tools available
available_tools_desc = {
    "dummy_search_tool" : """dummy_search_tool: A search tool to find info about select accounts
    Input
        - search_term: A google search term to use""",
    "search_tool" : """self.search_tool: Get information about different savings account
Input
    - search: A prompt explain what account you are trying to find. ONLY GIVE DETAILS OF THE ACCOUNT, NOT THAT YOU WANT THE BEST ONE
Unlike others, call this tool with exactly: self.search_tool(<search term>:str)""",
    "interest_calc": """interest_calc: Calculate the growth of an investment over a few years.
    Input
        - rate (float): the interest rate as a number (eg 5%=0.05)
        - investment (float): the initial investment
        - time (float): the number of years to leave the investment for"""
}
