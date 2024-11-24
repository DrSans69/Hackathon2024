import os
import openai
from dotenv import load_dotenv
from pathlib import Path
import re 
load_dotenv(Path("key.env"))
OPENAI_API_KEY = os.getenv("API_KEY")


openai.api_key = OPENAI_API_KEY


standart = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Green Earth Organization</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f9f9f9;
        }
        header {
            background-color: #4caf50;
            color: white;
            padding: 10px 20px;
            text-align: center;
        }
        nav {
            margin: 20px 0;
        }
        nav a {
            margin-right: 15px;
            text-decoration: none;
            color: #4caf50;
        }
        section {
            margin-bottom: 20px;
        }
        footer {
            background-color: #4caf50;
            color: white;
            text-align: center;
            padding: 10px 20px;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
</head>
<body>
    <header>
        <h1>Green Earth Organization</h1>
        <p>Working Together for a Sustainable Future</p>
    </header>
    <nav>
        <a href="#about">About Us</a>
        <a href="#projects">Our Projects</a>
        <a href="#contact">Contact</a>
    </nav>
    <section id="about">
        <h2>About Us</h2>
        <p>Green Earth Organization is dedicated to promoting environmental sustainability through education, community involvement, and innovative projects. Our mission is to inspire and empower individuals to take action for a healthier planet.</p>
    </section>
    <section id="projects">
        <h2>Our Projects</h2>
        <ul>
            <li><strong>Tree Plantation Drive:</strong> Organizing community tree-planting events in urban and rural areas.</li>
            <li><strong>Clean Water Initiative:</strong> Ensuring access to clean and safe drinking water in underprivileged communities.</li>
            <li><strong>Recycling Awareness Campaign:</strong> Educating people about waste management and recycling best practices.</li>
        </ul>
    </section>
    <section id="contact">
        <h2>Contact Us</h2>
        <p>Email: <a href="mailto:info@greenearth.org">info@greenearth.org</a></p>
        <p>Phone: +1 (555) 123-4567</p>
    </section>
    <footer>
        <p>&copy; 2024 Green Earth Organization. All rights reserved.</p>
    </footer>
</body>
</html>
"""
prompt = """
<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta http-equiv="Content-Style-Type" content="text/css" /><title></title></head><body style="line-height:116%; font-family:Aptos; font-size:12pt"><div><div style="-aw-headerfooter-type:header-primary; clear:both"><p style="margin-top:0pt; margin-bottom:8pt"><span style="height:0pt; display:block; position:absolute; z-index:-65537"><img src="Output.001.png" width="624" height="340" alt="" style="margin-top:230.87pt; -aw-left-pos:0pt; -aw-rel-hpos:margin; -aw-rel-vpos:margin; -aw-top-pos:0pt; -aw-wrap-type:none; position:absolute" /></span><span style="-aw-import:ignore">&#xa0;</span></p></div><p style="margin-top:0pt; margin-bottom:8pt"><span>Test1</span></p><p style="margin-top:0pt; margin-bottom:8pt"><span style="font-family:'Amasis MT Pro Black'">Test2</span></p><p style="margin-top:0pt; margin-bottom:8pt"><span style="font-family:'Arial Black'; color:#45b0e1">Test3</span></p><p style="margin-top:0pt; margin-bottom:8pt"><span style="font-family:'Arial Black'; text-decoration:underline; color:#4c94d8">Test4</span></p><p style="margin-top:0pt; margin-bottom:8pt; text-align:right"><span style="font-family:'Arial Nova Cond'; font-weight:bold; text-decoration:underline">Multiple words line test </span></p></div></body></html>
"""
history = []
completion = openai.chat

def get_html_from_str(string : str):
    pattern = r"<!DOCTYPE html>.*?</html>"
    match = re.search(pattern, string, re.DOTALL)
    modified_string = re.sub(pattern, "", string, flags=re.DOTALL)
    html_document = match.group(0)
    return (modified_string, html_document)
    


def document_type(prompt):
    completion = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": """You need to determine what the topic is in the given HTML document"""},
        {"role" : "assistant", "content" :  "The topic is an email"},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content

def topics(prompt):
    completion = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": """Determine the overral document structure simmiliar to the given document"""},
        {"role" : "assistant", "content" :  "The "},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content

def analyze(prompt, standart, history : list, origin):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""You are a helpful assistant who needs to analyze and validate given document which was a {origin} format, converted to html. 
            In you should give recommendations assuming this is still a file of {origin} format. Compare the
            document against this standard: {standart} of user's organisation and general look of documents of such types. You 
            need to recommend autofill suggestions for
            incomplete sections is they are present, and if there is some  historical data: {history}, base it on it. Give the user's document overall score out of 10.
            Print your recommendations, suggest what other things the user may add based on the topic and type of the document. Account for formatting too. Fistly you type what the provided document is, meaning it's orignal format {origin}. 
            Do not specify that it has been converted. Then the overall score which should be just 
            some number out of 10, then 
            by points recommendations for Autofill Suggestions, small conclusion. Do not use hashtags before topic names"""},
            {"role" : "assistant", "content" :  """The provided document is a ... Overall score: 10/10. Recommendations for Autofill Suggestions: ... Conclusion: ..."""},
            {"role": "user", "content": prompt}
        ]
    )
    history.append(prompt)
    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content

def human_correction(prompt, answer, text, history):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""You have to modify the original document {text} 
             based on the points the user wants to modify. All the available 
             points are here: {answer}. Take into account 
             history of prompts and answers: {history}. Print the whole modified document as an answer. 
             It always should start with <!DOCTYPE html>"""},
            # {"role" : "assistant", "content" :  """<"""},
            {"role": "user", "content": prompt}
        ]
    )
    history.append(prompt)
    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content


def parse_check(prompt, standard, history, origin):
    response = analyze(prompt, standard, history, origin)

    # Clean up and print each section
    sections = re.split(
        r'(?i)(?=\b(The provided document is|Overall score|Recommendations for Autofill Suggestions|Conclusion):?)', response
    )

    # Combine headers with their respective content
    parsed_sections = []
    current_section = ""

    for part in sections:
        if re.match(r'(?i)\b(The provided document is|Overall score|Recommendations for Autofill Suggestions|Conclusion):?', part):
            if current_section:  # Save the previous section
                parsed_sections.append(current_section.strip())
            current_section = part  # Start a new section
        else:
            current_section += part  # Append content to the current section

    if current_section:  # Add the last section
        parsed_sections.append(current_section.strip())

    # Output each section
    # for i, section in enumerate(parsed_sections):
    #     print(f"Section {i}:\n{section}\n")

    # Check if sections match the expected ones
    if (
        len(parsed_sections) < 7 or  # Ensure we have at least 7 sections
        parsed_sections[0] != "The provided document is" or
        parsed_sections[2] != "Overall score" or
        parsed_sections[4] != "Recommendations for Autofill Suggestions" or
        parsed_sections[6] != "Conclusion"
    ):
        # If not matching, recursively call the function again
        return parse_check(prompt, standard, history, origin)
    else:
        # Return parsed sections if everything matches
        return parsed_sections
    


if __name__ == "__main__":
    while True:
        origin = "docx"
        user_input = input("You: ")
        document = prompt
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        response = parse_check(prompt, standart, history, origin)
        # response = document_type(prompt)
        # print("GPT: ", response)
        for i in range(1, len(response), 2):
            print(response[i], "\n")
        user_input = input("You: ")
        correction = human_correction(user_input, response, document, history)
        print("GPT: ", correction)
        text, html = get_html_from_str(correction)
        print("HTML: ", html)
        print("TEXT: ", text)
        