import PyPDF2
import requests
import json

def load_pdf_text(pdf_file):
    with open(pdf_file, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def extract_information_from_pdf(pdf_file):


    # Prompt the LLM to extract the requested information
    # prompt = f"Extract the effective date, governing law, and parties from the following contract:\n\n{text}"
    # prompt = f"You are a legal expert. Read the following document and answer the questions following it:\n\n{text}\n Question: What is the effective date? Do not provide any other information."
    prompt = f"Read the text of input-docs/contract.pdf"
    # prompt = f"what is the effective date, governing law, and parties from the following contract"

    tools = [
    {
      "type": "function",
      "function": {
        "name": "load_pdf_text",
        "description": "Get the text from the supplied pdf file path",
        "parameters": {
          "type": "object",
          "properties": {
            "pdf_name": {
              "type": "string",
              "description": "The path to the pdf file"
            }
          },
          "required": ["pdf_name"]
        }
      }
    }
  ]

    url = "http://192.168.137.2:11434/api/chat"
    data = {
        "model": "llama3.1",
        "messages": [
            {
                "role": "user",
                "content": "What is effective date of the contract in input-docs/contract.pdf?"
            }
        ],
        "stream": False,
        "tools": tools
        }

    headers = {
        'Content-Type': 'application/json'
    }

    print(f"\nprompt being sent: {prompt}\n")

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)["message"]["tool_calls"][0]["function"]["arguments"]["pdf_name"]
        # return response
    else:
        return f"Error: {response.status_code}, {response.text}"


    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the information from the LLM's response
    information = {}
    information["effective_date"] = response.choices[0].text.split("\n")[0]
    information["governing_law"] = response.choices[0].text.split("\n")[1]
    information["parties"] = response.choices[0].text.split("\n")[2]

    return information

# Example usage
pdf_file = "input-docs/contract.pdf"
information = extract_information_from_pdf(pdf_file)
print(information)