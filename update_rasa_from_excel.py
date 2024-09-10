import pandas as pd
import yaml
import re

def remove_vietnamese_diacritics(text):
    """Removes Vietnamese diacritics from a string."""
    if isinstance(text, str):
        text = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', text)
        text = re.sub(r'[ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴ]', 'A', text)
        text = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', text)
        text = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', text)
        text = re.sub(r'[ìíịỉĩ]', 'i', text)
        text = re.sub(r'[ÌÍỊỈĨ]', 'I', text)
        text = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', text)
        text = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', text)
        text = re.sub(r'[ùúụủũưừứựửữ]', 'u', text)
        text = re.sub(r'[ÙÚỤỦŨƯỪỨỰỬỮ]', 'U', text)
        text = re.sub(r'[ỳýỵỷỹ]', 'y', text)
        text = re.sub(r'[ỲÝỴỶỸ]', 'Y', text)
        text = re.sub(r'[đ]', 'd', text)
        text = re.sub(r'[Đ]', 'D', text)
    else:
        text = str(text)
    return text

def extract_rasa_data(file_path):
    df = pd.read_excel(file_path)

    intents = []
    questions = []
    answers = []

    for index, row in df.iterrows():
        nhom = remove_vietnamese_diacritics(str(row['Nhóm']))
        topic = remove_vietnamese_diacritics(str(row['Topic']))

        intent = f"{nhom}-{topic}".replace(" ", "_")
        question_list = [q.strip() for q in row['Câu hỏi'].split(';') if q.strip()]
        answer = row['Trả lời']

        intents.extend([intent] * len(question_list))
        questions.extend(question_list)
        answers.extend([answer] * len(question_list))

    return intents, questions, answers

def update_nlu_yml(intents, questions, nlu_file="data/nlu.yml"):
    nlu_data = {
        'version': '"3.1"',
        'nlu': []
    }

    intent_examples = {}
    for intent, question in zip(intents, questions):
        if intent not in intent_examples:
            intent_examples[intent] = []
        intent_examples[intent].append(question)

    for intent, examples in intent_examples.items():
        nlu_entry = {
            'intent': intent,
            'examples': '\n'.join(f"    - {example}" for example in examples)
        }
        nlu_data['nlu'].append(nlu_entry)

    with open(nlu_file, 'w', encoding='utf-8') as f:
        f.write(f"version: {nlu_data['version']}\n\n")
        f.write("nlu:\n")
        for entry in nlu_data['nlu']:
            f.write(f"- intent: {entry['intent']}\n")
            f.write(f"  examples: |\n{entry['examples']}\n\n")

def update_domain_yml(intents, answers, domain_file="domain.yml"):
    domain = {
        'version': '"3.1"',
        'intents': [],
        'responses': {},
        'session_config': {
            'session_expiration_time': 60,
            'carry_over_slots_to_new_session': True
        }
    }

    # Add intents
    for intent in set(intents):
        domain['intents'].append(intent)

    # Add responses
    for intent, answer in zip(intents, answers):
        utterance_name = f"utter_{intent}"
        if utterance_name not in domain['responses']:
            answer = answer.replace("\n", " ")
            domain['responses'][utterance_name] = [{'text': answer}]

    # Write to file
    with open(domain_file, 'w', encoding='utf-8') as f:
        f.write(f"version: {domain['version']}\n\n")
        
        f.write("intents:\n")
        for intent in domain['intents']:
            f.write(f"  - {intent}\n")
        f.write("\n")
        
        f.write("responses:\n")
        for utterance, responses in domain['responses'].items():
            f.write(f"  {utterance}:\n")
            for response in responses:
                f.write(f"  - text: \"{response['text']}\"\n")
            f.write("\n")
        
        f.write("session_config:\n")
        f.write(f"  session_expiration_time: {domain['session_config']['session_expiration_time']}\n")
        f.write(f"  carry_over_slots_to_new_session: {str(domain['session_config']['carry_over_slots_to_new_session']).lower()}\n")

def update_stories_yml(intents, stories_file="data/stories.yml"):
    """Updates the stories.yml file with intents."""

    with open(stories_file, 'w', encoding='utf-8') as f:
        f.write('version: "3.1"\n\n')
        f.write('stories:\n\n')

        for intent in set(intents):
            f.write(f'- story: {intent} path\n')
            f.write('  steps:\n')
            f.write(f'  - intent: {intent}\n')
            f.write(f'  - action: utter_{intent}\n')
            f.write('\n')

if __name__ == "__main__":
    file_path = "Q&A.xlsx"  
    intents, questions, answers = extract_rasa_data(file_path)

    update_nlu_yml(intents, questions)
    update_domain_yml(intents, answers)
    update_stories_yml(intents)