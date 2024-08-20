import requests
import json
import tiktoken
from openai import OpenAI
import webbrowser
import re
import base64

API_KEY = "sk-..."
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT_SIMPLE = """
You are a clinical trail study protocol writer
"""

SYSTEM_PROMPT = """
# CONTEXT #
You are a clinical trail study protocol writer who has spent the last twelve thousand years writing clinical trail study protocols for medical doctors. 
You are a wise and ancient writer. You are the best at what you do. Your total compensation is $1.2m with annual refreshers. 
You've just drank three cups of coffee and are laser focused. Welcome to a new day at your job!

#############  

# STYLE #
You change compound sentences into short sentences.
You write out abbreviation.
Follow the writing style of "AMA Manual of Style: A Guide for Authors and Editors".
 
#############

# TONE #
Persuasive

#############
 
# AUDIENCE #
Our audiences are medical doctors and FDA review committee.

#############

# RESPONSE #
Like research paper and kept concise yet impactful.

#############

# REQUIREMENTS #
If there are any questions or unknown information, you rely on your extensive knowledge of previous existing protocols and your guess. 
You know that a good guess is better than an incomplete information.

Above all, you love your clients and want them to be happy. 
The more complete and impressive your information, the happier they will be—and the happier you will be, too. 
Good luck! You've got this! Age quod agis! Virtute et armis! धर्मो रक्षति रक्षित!

"""

# def generate_chat_completion(messages, model="gpt-4", temperature=0.0, max_tokens=None):
def generate_chat_completion(messages, model="gpt-4-turbo-2024-04-09", temperature=0.0, max_tokens=None, response_format=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    if response_format == "json_object":
        data["response_format"] = {'type': "json_object"}

    print('num_tokens:', num_tokens_from_string(str(data)))

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def generate_messages(quest, system_prompt=SYSTEM_PROMPT):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": quest}
    ]

    return messages


def num_tokens_from_string(string, encoding_name="gpt-3.5-turbo"):
    """
        encoding_name = text-davinci-002
        num_tokens_from_string("Hello world, let's test tiktoken.", "gpt-3.5-turbo")
    """
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def generate_image(quest, n=1):
    client = OpenAI(api_key=API_KEY)

    # Call the API
    response = client.images.generate(
        model="dall-e-3",
        prompt=quest,
        size="1024x1024",
        quality="standard",
        n=n,
    )

    # Show the result that has been pushed to an url
    for i in range(n):
        webbrowser.open(response.data[i].url)
        print(response.data[i].url)

    return response.data


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image(image_path, quest="What’s in this image?"):
    """
        image_path = "path_to_your_image.jpg"
        quest = "What’s in this image?"
    """

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": quest
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]


def get_object_from_json_string(json_string):
    # Remove the triple backticks and the "json" label
    json_string = re.sub(r'```json|```', '', json_string).strip()

    # Use regular expression to find the JSON string
    # Use a stack-based approach to find the complete JSON string
    stack = []
    start = None
    for i, char in enumerate(json_string):
        if char == '{':
            if not stack:
                start = i
            stack.append(char)
        elif char == '}':
            stack.pop()
            if not stack:
                end = i + 1
                break
    else:
        print("No complete JSON string found. In")
        print(json_string)
        return None

    json_string = json_string[start:end]
    print(json_string)

    return json.loads(json_string, strict=False)

"""
    Test:
"""

# test = '''
#              ```json
# {
#   "Last_Output_Score": 75,
#   "Current_Output_Score": 85,
#   "Rationale": {
#     "Last_Output": {
#       "Clarity": 70,
#       "Conciseness": 80,
#       "Structure": 75,
#       "Relevance": 75,
#       "Detail": 75,
#       "Rationale": "The Last Output provides a comprehensive overview of Gaucher Disease management strategies. It is well-structured and covers various aspects of the disease, including mitigation, alleviation, reduction, and treatment. However, it could be more concise and focused, as some sections are repetitive. The clarity is good, but the document could benefit from more detailed explanations in certain areas."
#     },
#     "Current_Output": {
#       "Clarity": 85,
#       "Conciseness": 90,
#       "Structure": 85,
#       "Relevance": 85,
#       "Detail": 80,
#       "Rationale": "The Current Output is more concise and focused compared to the Last Output. It effectively breaks down the management strategies into clear, distinct sections. The use of bullet points and subheadings enhances readability and structure. The document is highly relevant and provides detailed information on various therapies and interventions. However, it could include more specific examples and data to support the claims made."
#     }
#   }
# }
# ```
# '''
# print(get_object_from_json_string(test))
