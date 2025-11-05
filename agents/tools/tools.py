from matplotlib.style import available
from .web_scraper_llm import web_search

# The tools the bank account agent can use.

# Dummy search tool
def dummy_search_tool(search_term:str) -> str:
    return f"Natwest: 3.5% fixed, Monzo: 5% fixed, Suffolk Building Society: 5% variable"

# Proper search tool
def account_finder_tool(search=""):
    # We will extract plain text from this webpage
    urls = ['https://www.natwest.com/savings.html', 'https://www.hsbc.co.uk/savings/products/']
    # Get HTML source code of the webpage
    response = web_search(urls, search)

    return response

# Tool to calculate return on investment
def interest_calc(rate, investment, time):
    return investment*(1+rate)**time


# Overall regex to match the functions
match_num = r'[+-]?(?:\d*\.\d+|\d+)'

available_tools = {
    "dummy_search_tool":r'(dummy_search_tool\(".*"\))',
    "account_finder_tool": r'(account_finder_tool\((search=)*((".*")|(\'.*\'))\))',
    "interest_calc": fr'(interest_calc\((rate=)*{match_num}\,( )*(investment=)*{match_num}\,( )*(time=)*{match_num}(/{match_num})*\))'
}
