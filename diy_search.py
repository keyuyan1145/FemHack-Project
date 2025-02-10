from googlesearch import search
from bs4 import BeautifulSoup
import requests

def get_diy_instructions(query, search_platform="google", target_site="wikihow"):
    """
    Search for DIY instructions and parse the content.
    
    Args:
        query (str): Search query (e.g., "how to build a shelf")
        search_platform (str): Search engine to use (default: "google")
        target_site (str): Target website to extract from (default: "wikihow")
    
    Returns:
        dict: Parsed information including steps, tools, and warnings
    """
    try:
        # Construct search query
        search_query = f"site:{target_site}.com {query}"
        
        # Get first result
        if search_platform.lower() == "google":
            search_results = list(search(search_query, num_results=1))
            if not search_results:
                return {"error": "No results found"}
            target_url = search_results[0]
        else:
            return {"error": f"Search platform {search_platform} not supported"}

        # Fetch webpage content
        response = requests.get(target_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Parse WikiHow content
        result = {
            "title": "",
            "tools": [],
            "steps": [],
            "warnings": [],
            "url": target_url
        }

        # Get title
        title = soup.find('h1')
        if title:
            result["title"] = title.text.strip()

        # Get tools/things you'll need
        things_needed = soup.find('div', {'class': 'things-you-ll-need'})
        if things_needed:
            tools_list = things_needed.find_all('li')
            result["tools"] = [tool.text.strip() for tool in tools_list]

        # Get steps
        method_steps = soup.find_all('div', {'class': 'step'})
        for step in method_steps:
            step_text = step.find('div', {'class': 'step-content'})
            if step_text:
                result["steps"].append(step_text.text.strip())

        # Get warnings
        warnings = soup.find_all('div', {'class': 'warning'})
        result["warnings"] = [warning.text.strip() for warning in warnings]

        return result

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"} 