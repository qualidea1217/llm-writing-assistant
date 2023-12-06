import openai
from flask import Flask, request, jsonify
from flask_cors import CORS


"""Usage Instruction:
1. Before actual usage, you need to install flask, flask-cors, and openai to make the backend work properly.
Install them through "pip install flask", "pip install flask-cors", "pip install openai".
2. Once all the required dependencies are installed, initialize the backend by run the writing_assistant.py.
Make sure to fill in the api_key for the openai api in the writing_assistant.py since this backend program use openai
chatgpt as the service provider for AI writing assistant.
3. Open writing_assistant.html as the frontend (website) and start using."""


DEFAULT_MODEL = "gpt-4-1106-preview"  # openai model name
DEFAULT_API_KEY = "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"  # REMOVE THIS BEFORE PUSH TO GITHUB!!!

app = Flask(__name__)
CORS(app)


def openai_chat(role: str, prompt: str, api_key: str, model) -> str:
    """
    Wrapper for one chat.
    :param role: prompt for system role.
    :param prompt: actual input for this chat.
    :param api_key: openai api key
    :param model: model name
    :return: output from chatgpt
    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]
    )
    output_str = response["choices"][0]["message"]["content"]
    return output_str


def get_simplification(text: str, api_key: str, model: str) -> str:
    """
    openai API for text simplification
    :param text: text for simplification
    :param api_key: openai api key
    :param model: model name
    :return: output from chatgpt
    """
    role = """You are a skilled editor, known for your ability to simplify complex text while preserving its meaning. 
    You have a strong understanding of readability principles and how to apply them to improve text comprehension."""
    prompt = f"""Given the text from an essay, write an appropriate simplified version of the text to improve its 
    readability, ensuring its core meaning remains intact. Return only the simplified version of the selected segment. 
    Return <UNABLE> if you are unable to fulfill the request.\n\ntext: {text}"""
    output_str = openai_chat(role, prompt, api_key, model)
    if "<UNABLE>" in output_str:
        return "Sorry, I am unable to fulfill your requirement."
    return output_str


def get_translation(text: str, target_language: str, api_key: str, model: str) -> str:
    """
    openai API for text translation
    :param text: text for translation
    :param target_language: output text langauge
    :param api_key: openai api key
    :param model: model name
    :return: output from chatgpt
    """
    role = """You are a skilled translator, known for your ability to translate complex text while preserving its 
    meaning. You have a strong understanding of different languages"""
    prompt = f"""Translate the following text to {target_language}. Ensure the translated version maintains the 
    original meaning, style, and coherence. Please pay attention to cultural nuances and idiomatic expressions, 
    striving for a natural and fluent translation. The essay should be translated with precision and accuracy while 
    considering the target audience's linguistic and cultural context. Return only the translated content. 
    Return <UNABLE> if you are unable to fulfill the request.\n\ntext: {text}"""
    output_str = openai_chat(role, prompt, api_key, model)
    if "<UNABLE>" in output_str:
        return "Sorry, I am unable to fulfill your requirement."
    return output_str


def grammar_check(text: str, api_key: str, model: str):
    """
    openai API for grammar check
    :param text: text for grammar check
    :param api_key: openai api key
    :param model: model name
    :return: output from chatgpt, text after fixing grammar
    """
    role = """You are a skilled and helpful writing assistant who has abundant knowledge about grammar."""
    prompt = f"""Proofread the following text for grammar and language accuracy. Correct any grammatical errors, 
    punctuation mistakes, and ensure that the language flows smoothly. Pay attention to proper sentence structure, 
    verb agreement, tense consistency, and clarity of expression. Additionally, check for spelling errors and ensure 
    that the overall writing adheres to the conventions of formal or informal language, as specified. 
    Provide only the corrected result. Return <UNABLE> if you are unable to fulfill the request.\n\ntext: {text}"""
    output_str = openai_chat(role, prompt, api_key, model)
    if "<UNABLE>" in output_str:
        return "Sorry, I am unable to fulfill your requirement."
    return output_str


@app.route('/grammar_check', methods=['POST'])
def grammar_check_api():
    data = request.json
    text = data['text']
    # Call your Python function here with the text
    result = grammar_check(text, DEFAULT_API_KEY, DEFAULT_MODEL)
    response = jsonify(result)
    return response

@app.route('/text_simplification', methods=['POST'])
def text_simplification_api():
    data = request.json
    text = data['text']
    # Call your Python function here with the text
    result = get_simplification(text, DEFAULT_API_KEY, DEFAULT_MODEL)
    response = jsonify(result)
    return response


@app.route('/text_translation', methods=['POST'])
def text_translation_api():
    data = request.json
    text = data['text']
    target_langauge = data["target_language"]
    # Call your Python function here with the text
    result = get_translation(text, target_langauge, DEFAULT_API_KEY, DEFAULT_MODEL)
    response = jsonify(result)
    return response


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)  # run this to start backend