from openai import OpenAI
import re

instruction_search_prompt = """
You are an experienced {role} with 10+ years of experience. Generate a detailed step by step DIY plan for a resident homeowner who is looking to {action} a {product} themselves. Include the all the tools needed. If you understand it, answer "ready". Don't give me any additional information right now, I will ask you for it when needed. 
"""

tool_prompt = "What tools should I prepare for? Give the me the list of tool in a numbered list"

steps_prompt = "I have the tools ready. Show me the detailed step-by-step plan in a numbered list."

client = OpenAI()


number_regex = "\d. "

def call_ai_chat(prompt, model):
    return client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1500
    )

def search_instruction_ai(
    role, product, action, model="gpt-3.5-turbo"
):

    try:
        """
        Args:
            temperature (float): Controls randomness in the output
                - Range: 0.0 to 2.0
                - 0.0: More focused, deterministic, consistent
                - 1.0: More creative, diverse, random
                - Default: 0.7 (balanced)
                
            max_tokens (int): Limits the length of the response
                - Range: 1 to model's context limit
                - Counts both input and output tokens
                - Higher values allow longer responses
                - Default: 1000 (moderate length)
        """

        ready_response = str(call_ai_chat(
            instruction_search_prompt.format(
                role = role, 
                product=product, 
                action=action
            ),
            model
        ).choices[0].message)

        print("ready_response: ", ready_response)

        if ("ready" not in ready_response and "Ready" not in ready_response and "READY" not in ready_response):
            raise Exception("Sorry, unable to fetch instructions for the given product")

        tool_response = str(
            call_ai_chat(tool_prompt, model).choices[0].message.content
        ).replace("\n", " ")

        print("tool_response: ", tool_response)
        # print("type of response.choices[0].message: ", type(response.choices[0].message))

        # tool_list = re.split(r'\d.', tool_response)
        tool_list = re.split(r'\d.', tool_response)[1:]


        print("tool_list.size = ", len(tool_list))

        # content = str(tool_response.choices[0].message).replace("\n", "")
        # print("type after str cast: ", type(content))

        step_response = str(
            call_ai_chat(steps_prompt, model).choices[0].message.content
        ).replace("\n", " ")

        # print("step_response: ", step_response)
        steps = re.split(r'\d.', step_response)[1:]

        print("number of steps: ", len(steps))

        print("steps: ", steps)

        # print(response.choices[0].message)
        
        return {
            "success": True,
            "steps": steps,
            "tools": tool_list,
            "model": model
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model": model
        }


# lego_style_prompt = f"""
# You are an experienced LEGO-style manual designer specializing in step-by-step visual-only guides. Generate a LEGO-like, clipart-style manual for {product_name}, ensuring the following:
# - Each step has its own dedicated visual, with a consistent representation of the product throughout.
# - Absolutely no text in any visual—communication relies solely on clear, structured imagery.
# - The step number appears in the upper left corner of each visual for order clarity.
# - No characters or unnecessary elements—focus entirely on the product and required physical action for each step.
# - Emphasize physical actions using arrows, motion lines, highlights, and intuitive symbols.
# - Maintain a clean, minimalistic style with simple but effective design.

# Follow these steps for the process:
# {steps}
# """
lego_style_prompt = f""

## TODO: try passing all steps vs. passing a single step at a time
def generate_image_from_prompt(
    product, steps,imgCnt=1, imgSize="512x512"
):
    response = client.images.generate(
        prompt=lego_style_prompt.format(product_name=product, steps=steps),
        n=imgCnt,
        size=imgSize
    )

    print(response.data[0].url)
    return response.data[0].url
