from load_legend import legend
from author_stats import collect_author_stories, show_author_stats
from story_stats import show_story_stats
from morph_analysis import analyse_morph, show_analysis
from persistance_layer import repo, Stories, Authors
from pathlib import Path
import requests
import os, sys, atexit

API_KEY = '84668444eaa4feb6ac59b3522a264275f539f9d6d58dec127a48948c1e8b833c'

STORIES_DIR = Path(__file__).parent / "Stories"
PDF_DIR = STORIES_DIR / "pdf"
TXT_DIR = STORIES_DIR / "txt"
HTML_DIR = STORIES_DIR / "html"
MORPH_DIR = STORIES_DIR / "morph"

FILE_TYPES = {1: 'TXT', 2: 'HTML', 3: 'PDF'}
TYPE_FOLDER = {'txt': TXT_DIR, 'html': HTML_DIR, 'pdf': PDF_DIR}
MAIN_MENU = {1: 'Add stories', 2: 'View stats for a single story', 3: 'View stats for all the works of one author', 4: 'View Morphological Analysis for a single story', 5: 'Exit'}

def get_menu_option(menu):
    # Print the menu
    for number, option in menu.items():
        print(f'{number}) {option}')

    # Get user input and validate it
    while True:
        try: 
            if (option := int(input('Choose Action Number -----> '))) in  menu.keys():
                break
        except ValueError as e:
            continue
    
    return option

def find_story_id():
    
    while True:
        name = input('Please enter a story name to load: (or -1 to exit) ')
        if name == '-1':
            return -1
        for story in legend:
            if story[2] == name:
                return int(story[0])
        print('The story name you\'ve enterd doesn\'t exist, Please try a different name.')
        
def get_story(file_type, story_id = None):
    try:

        while True:
            if not story_id:
                story_id = find_story_id()

            if story_id == -1:
                return None
        
            if ret_value := repo.stories.find(id=story_id, type=file_type):
                if os.path.exists(ret_value.story_file_path):
                    print(f'The story with the I.D {story_id} loaded successfully.')
                    return ret_value

            api_url = f'https://staging.benyehuda.org/api/v1/texts/{story_id}?key={API_KEY}&view=metadata&file_format={file_type}'

            if not (response := requests.get(api_url, timeout=6.0)):
                print(f'The story with the I.D {story_id} appears in "Ben Yehuda Project" but cannot be accessed, Please try another story.')
                return None
                
            break

        story_url = response.json().get('download_url')
        story_name = response.json().get('metadata').get('title')
        story_file_path = TYPE_FOLDER.get(file_type) / f"{story_name}.{file_type}"
        
        if os.path.exists(story_file_path):
            print(f'The story with the I.D {story_id} loaded successfully.')
            return repo.stories.find(story_name=story_name)
        
        for author_id, author_name in zip(response.json().get('metadata').get('author_ids'), response.json().get('metadata').get('author_string').split('/')):
            repo.stories.insert(Stories(story_id, story_name, author_id, str(story_file_path), file_type))
            repo.authors.insert(Authors(author_id, author_name))

        story = requests.get(story_url, allow_redirects=True)

        with open(story_file_path, 'wb') as story_file:
            story_file.write(story.content)
        
        ret_value = repo.stories.find(story_name=story_name)
        print(f'The story with the I.D {story_id} loaded successfully.')
        return ret_value

    # Exceptions handling
    except ConnectionError as e:
        print('Connection Error:', e)
        response = 'no response'
    except requests.HTTPError as err:
        if err.code == 404:
            print('page not found')
        else:
            raise
    except requests.ConnectTimeout as e:
        print('Timeout Error:', e)
    except requests.RequestException as e:
        print('Some Ambiguous Exception:', e)

def add_stories():
    while True:
        print('\nAdd a story to your local Database:\n')
        if not get_story(FILE_TYPES[get_menu_option(FILE_TYPES)].lower()):
            return

def story_stats():
    print('\nView the statistics of a single story:\n')
    if not(story := get_story('txt')):
        return
    show_story_stats(story) 

def author_stats():

    while True:
        author_name = input('Please enter author name: (or -1 to exit) ')
        if author_name == '-1':
            return

        author_id = None
        if not(author := repo.authors.find(name=author_name)):
            for story in legend:
                if story[3] == author_name:
                    author_id = int(story[1].split('/')[1][1:])
                    repo.authors.insert(Authors(author_id, author_name))
                    break
        else:
            author_id = author.id
            
        if author_id != None:
            break

    number_of_stories = 0
    for story in legend:
        if int(story[1].split('/')[1][1:]) == author_id:
            if (story_file := get_story('txt', int(story[0]))):
                number_of_stories +=1
                collect_author_stories(story_file)

    show_author_stats(repo.authors.find(id=author_id), number_of_stories)

def morphological_analysis():
    print('\nView the morphological analysis for a single story:\n')
    if not(story := get_story('txt')):
        return
    file_path = MORPH_DIR / f'{story.story_name}.json'
    if not os.path.exists(file_path):
        analyse_morph(story, file_path)

    show_analysis(file_path)

def exit():
    sys.exit()
    
MAIN_MENU_FUNCS = {1: add_stories, 2: story_stats, 3: author_stats, 4: morphological_analysis, 5: exit}

def main():
    if not os.path.exists(STORIES_DIR):
        os.mkdir(STORIES_DIR)
    if not os.path.exists(PDF_DIR):
        os.mkdir(PDF_DIR)    
    if not os.path.exists(TXT_DIR):
        os.mkdir(TXT_DIR)    
    if not os.path.exists(HTML_DIR):
        os.mkdir(HTML_DIR)
    if not os.path.exists(MORPH_DIR):
        os.mkdir(MORPH_DIR)
    
    atexit.register(repo._close)
    while True:
        MAIN_MENU_FUNCS[get_menu_option(MAIN_MENU)]()

if __name__ == '__main__':
    main()