import requests

API = 'https://nakdan-4-0.loadbalancer.dicta.org.il/addnikud'
headers = {'Content-Type': 'text/plain;charset=utf-8'}


def morph_analysis(story):
    with open(story.story_file_path, 'r', encoding='utf-8')  as story_file:
        final_return = ""
        content = story_file.read()
        while len(content) > 30000:
            temp = content[:30000]
            content = content[30000:]
            packet = {  "task": "nakdan",
                        "genre": "modern",
                        "data": temp,
                        "addmorph": True,
                        "matchpartial": True,
                        "keepmetagim": False,
                        "keepqq": False
                     }
            answer = requests.post(API, headers=headers, json=packet)
            answer.encoding= "UTF-8"
            final_return += answer.text
        print(final_return)
