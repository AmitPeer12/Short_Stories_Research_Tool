from operator import concat
from decode_morph import tostring1
import requests, json, openpyxl

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

def add_top_to_sheet(sheet):
    sheet["A1"] = "Word"
    sheet["B1"] = "Is Seperator"
    sheet["C1"] = "Vocalized"
    sheet["D1"] = "Lex"
    sheet["E1"] = "Prefix"
    sheet["F1"] = "Pos"
    sheet["G1"] = "Gender"
    sheet["H1"] = "Number"
    sheet["I1"] = "Person"

def parse_morph(morph_tag):
    return []

def reorganize_row(row):
    new_row = []
    new_row.append(row["word"])
    new_row.append(row["sep"])
    options = row["options"]
    if len(options) > 0:
        y = {}
        for inner in options:
            y['morph'] = '0x{0:{1}X}'.format(int(inner["morph"]), 16)
        print(y)
        #options = options[0]
        #new_row.append(options["w"])
        #new_row.append(options["lex"])
        #print()
        #return concat(new_row, parse_morph(int(options["morph"])))
    return new_row

def add_data_to_sheet(data, sheet):
    for index, row in enumerate(data, start=2):
        for i, value in enumerate(reorganize_row(row)):
            sheet[f'{chr(ord("A") + i)}{index}'] = value

def analyse_morph(story, json_file_path):
    with open(story.story_file_path, 'r', encoding='utf-8')  as story_file:
        with open(json_file_path, 'a', encoding='utf-8') as analysis_file:
            content = story_file.read()
            while True:
                if len(content) < 30000:
                    json.dump(send_request(content), analysis_file)
                    break
                temp = content[:30000]
                content = content[30000:]
                json.dump(send_request(temp), analysis_file)

def show_analysis(story_name, json_file_path, morph_file_path):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = story_name
    add_top_to_sheet(sheet)
    with open(json_file_path, 'r') as data:
        add_data_to_sheet(json.loads(data.read()), sheet)
    workbook.save(morph_file_path)