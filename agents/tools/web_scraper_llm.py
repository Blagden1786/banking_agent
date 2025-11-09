import requests
from bs4 import BeautifulSoup
from google import genai


#LLM web scraper. It takes in the text from a number of websites and summarises it to pick out the relevant info on savings accounts


def sumamrise(text:str, details:str)-> str | None:
    """Use an llm to summarise the text/html code of a website and pull out the savings in a machine readable format

    Args:
        text (str): The website
        details (str): The type of account the agent needs to find

    Returns:
        str: The machie readable text
    """

    PROMPT = """You are a helpful bot that summarises the input websites.

    You will be given a collection of websites that contain information about accounts, such as savings or credit cards. Your goal is to extract the useful information about each account. You should also find the link to each account.
Only select the accounts that comply with this prompt and ignore any ask for the best one if applicable: (""" + details + """)
After finding this information, place it into a format that is easily machine readable (eg JSON).

For example:
Input site: HSBC: account1 5% variable instant access, account2 10% fixed rate ISA no access
Output: {{Bank: HSBC, Name: account1, Rate: 5%, Withdrawals: Instant access, Type: Savings, Rate Change: Variable}, {Bank: HSBC, Name: account2, Rate: 10%, Withdrawals: None, Type: ISA, Rate Change: Fixed}}

The input you will receive will either be plain text or html code for a collection of websites. Now go and find all of the relevant accounts!\n""" + text

    client = genai.Client()
    response = client.models.generate_content(
            model="gemini-2.5-flash", contents=PROMPT
        )

    return response.text

def web_search(urls:list[str], details:str) -> str | None:
    """Web search a collection of webpages to get savings info

    Args:
        urls (list[str]): urls of savings websites to scraper
        details (str): The type of account the scraper needs to find

    Returns:
        str: Output of LLM for the url search
    """
    text = ""

    for url in urls:
        # Get HTML source code of the webpage
        response = requests.get(url)

        # Parse the source code using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        text += soup.get_text() + "\n--------\n"

    return sumamrise(text, details)
