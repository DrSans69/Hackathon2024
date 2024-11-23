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
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech Innovators Hub</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            line-height: 1.8;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #2d3e50;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 2em;
            letter-spacing: 1px;
        }
        nav {
            background-color: #34495e;
            text-align: center;
            padding: 10px;
        }
        nav a {
            color: white;
            text-decoration: none;
            margin: 0 20px;
            font-weight: bold;
            font-size: 1.1em;
        }
        nav a:hover {
            color: #1abc9c;
        }
        section {
            padding: 40px 20px;
            margin: 20px;
            background-color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h2 {
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 15px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #7f8c8d;
        }
        footer {
            background-color: #2d3e50;
            color: white;
            text-align: center;
            padding: 15px;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
</head>
<body>
    <header>
        <h1>Tech Innovators Hub</h1>
        <p>Shaping the Future of Technology</p>
    </header>
    <nav>
        <a href="#about">About</a>
        <a href="#projects">Our Projects</a>
        <a href="#contact">Get In Touch</a>
    </nav>
    <section id="about">
        <h2>About Us</h2>
        <p>At Tech Innovators Hub, we are dedicated to fostering groundbreaking technology solutions that will revolutionize industries. We bring together the best minds to collaborate on projects that push the limits of what's possible.</p>
    </section>
    <section id="projects">
        <h2>Our Projects</h2>
        <ul>
            <li><strong>AI for Healthcare:</strong> Developing intelligent systems to assist medical professionals in diagnosing and treating diseases.</li>
            <li><strong>Smart Cities:</strong> Implementing IoT technologies to build sustainable and efficient urban environments.</li>
            <li><strong>Blockchain Solutions:</strong> Creating decentralized systems to enhance security and transparency in various industries.</li>
        </ul>
    </section>
    <section id="contact">
        <h2>Contact Us</h2>
        <p>Email: <a href="mailto:info@techinnovatorshub.com">info@techinnovatorshub.com</a></p>
        <p>Phone: +1 (555) 987-6543</p>
    </section>
    <footer>
        <p>&copy; 2024 Tech Innovators Hub. All rights reserved.</p>
    </footer>
</body>
</html>
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
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """You need to determine what the topic is in the given HTML document"""},
        {"role" : "assistant", "content" :  "The topic is an email"},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content

def topics(prompt):
    completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """Determine the overral document structure simmiliar to the given document"""},
        {"role" : "assistant", "content" :  "The "},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content

def analyze(prompt, standart, history : list):
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""You are a helpful assistant who needs to analyze and validate documents given
            documents against this standard: {standart} of user's organisation and general look of documents of such types. You 
            need to recommend autofill suggestions for
            incomplete sections is they are present, and if there is some  historical data: {history}, base it on it. Give the user's document overall score out of 10.
            Print your recommendations, suggest what other things the user may add based on the topic and type of the document."""},
            {"role" : "assistant", "content" :  """The provided document is a ... It's overlall score is: 10/10. Recommendations for Autofill Suggestions: ..."""},
            {"role": "user", "content": prompt}
        ]
    )
    history.append(prompt)
    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content

def human_correction(prompt, answer, text, history):
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""You have to modify the original document {text} 
             based on the points the user wants to modify. All the available 
             points are here: {answer}. Take into account 
             history of prompts and answers: {history}. Print the whole modified document as an answer"""},
            # {"role" : "assistant", "content" :  """<"""},
            {"role": "user", "content": prompt}
        ]
    )
    history.append(prompt)
    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content


# def answer():



if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        document = prompt
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        response = analyze(prompt, standart, history)
        # response = document_type(prompt)
        print("GPT: ", response)
        user_input = input("You: ")
        correction = human_correction(user_input, response, document, history)
        print("GPT: ", correction)
        text, html = get_html_from_str(correction)
        print("HTML: ", html)
        print("TEXT: ", text)
        