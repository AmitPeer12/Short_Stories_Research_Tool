import requests
import json

API = 'https://nakdan-4-0.loadbalancer.dicta.org.il/addnikud'
headers = {'Content-Type': 'text/plain;charset=utf-8'}

def send_request(content):
    packet = {  
        "task": "nakdan",
        "genre": "modern",
        "data": content,
        "addmorph": True,
        "matchpartial": True,
        "keepmetagim": False,
        "keepqq": False
            }
    answer = requests.post(API, headers=headers, json=packet)
    answer.encoding= "UTF-8"
    return answer.json()

def analyse_morph(story, morph_file_path):
    with open(story.story_file_path, 'r', encoding='utf-8')  as story_file:
        with open(morph_file_path, 'a') as analysis_file:
            content = story_file.read()
            while True:
                if len(content) < 30000:
                    json.dump(send_request(content), analysis_file)
                    break
                temp = content[:30000]
                content = content[30000:]
                json.dump(send_request(temp), analysis_file)

def show_analysis(morph_file_path):
    print(morph_file_path)