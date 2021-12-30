from persistance_layer import repo, Stories, Authors
import random, ast, matplotlib.pyplot as plt
import requests, requests.exceptions
import pathlib, os, sys


API_KEY = '84668444eaa4feb6ac59b3522a264275f539f9d6d58dec127a48948c1e8b833c'

STORIES_DIR = fr'{pathlib.Path(__file__).parent.resolve()}\Stories'
PDF_DIR = fr'{pathlib.Path(__file__).parent.resolve()}\Stories\PDF'
TXT_DIR = fr'{pathlib.Path(__file__).parent.resolve()}\Stories\TXT'
HTML_DIR = fr'{pathlib.Path(__file__).parent.resolve()}\Stories\HTML'

LEGEND = 'https://raw.githubusercontent.com/projectbenyehuda/public_domain_dump/master/pseudocatalogue.csv'

FILE_TYPES = {1: 'TXT', 2: 'HTML', 3: 'PDF'}
TYPE_FOLDER = {'txt': TXT_DIR, 'html': HTML_DIR, 'pdf': PDF_DIR}
MAIN_MENU = {1: 'Add stories', 2: 'View stats for a single story', 3: 'View stats for all the works of one author', 4: 'Exit'}

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

def download_story(file_type):
    try:

        while True:
            serial_number = do_something()
            if not serial_number:
                print('There is not such a story, please try again')
                continue

            if serial_number == -1:
                return None

            api_url = f'https://staging.benyehuda.org/api/v1/texts/{serial_number}?key={API_KEY}&view=metadata&file_format={file_type}'

            if not (response := requests.get(api_url, timeout=6.0)):
                print('There is not such a story, please try again')
                continue
                
            break

        story_url = response.json().get('download_url')
        story_id = response.json().get('id')
        story_name = response.json().get('metadata').get('title')
        #story name can include chars that are invalid for path like "
        story_file_path = fr'{TYPE_FOLDER.get(file_type)}\{story_name}.{file_type}'
        
        if os.path.exists(story_file_path):
            return repo.stories.find(story_name = story_name)
        
        for author_id, author_name in zip(response.json().get('metadata').get('author_ids'), response.json().get('metadata').get('author_string').split('/')):
            repo.stories.insert(Stories(story_id, story_name, author_id, 0, ''))
            repo.authors.insert(Authors(author_id, author_name))

        story = requests.get(story_url, allow_redirects=True)

        with open(story_file_path, 'wb') as story_file:
            story_file.write(story.content)
            
        with open(story_file_path, 'r', encoding='utf-8')  as story_file:
            word_list = {}
            content = story_file.read().replace('\n', '').replace('\r', '').split()
            for word in content:
                word_list[word] = 1 if word not in word_list else word_list[word] + 1
                
            repo.stories.update('word_count', len(content), story_id)
        
        return repo.stories.find(story_name = story_name)

    # Exceptions handling
    except ConnectionError as e:
        print('Connection Error:', e)
        response = 'no response'
    except requests.HTTPError as err:
        if err.code == 404:
            print('page not found')
        else:
            raise
    except requests.RequestException as e:
        print('Some Ambiguous Exception:', e)
    except requests.ConnectTimeout as e:
        print('Timeout Error:', e)

def add_stories():
    while True:
        if not download_story(FILE_TYPES[get_menu_option(FILE_TYPES)].lower()):
            return
        
def story_stats():
    if not(story := download_story('txt')):
        return
 
    count = input('How many words would you like to study? ')
    word_stats = sorted(ast.literal_eval(story.word_stats).items(), key=lambda item: item[1], reverse=True)
    word_count = story.word_count
    uniqe_words = len(word_stats)
    
    # x-coordinates of left sides of bars
    left = range(count)
    
    # heights of bars
    height = word_stats.values()[:count]
    
    # labels for bars
    tick_label = word_stats.keys()[:count]
    
    # randomly generated list of colors
    colors = []
    for i in range(count):
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))
    
    # plotting a bar chart
    plt.bar(left, height, tick_label = tick_label,
            width = 0.8, color = colors)
    
    # naming the x-axis
    plt.xlabel('most frequant words in the story')
    # naming the y-axis
    plt.ylabel('word frequancy')
    # plot title
    plt.title(f'Stats for the story {story.story_name}')
    # additionl stats
    plt.text(0, 0,
                f'The story contains {word_count} words, {uniqe_words} of which are uniqe words. That is {uniqe_words / word_count * 100}%',
                verticalalignment='bottom',
                horizontalalignment='center',
                fontsize=15)
    # function to show the plot
    plt.show()
        
def author_stats():
    return

def exit():
    sys.exit()
    
MAIN_MENU_FUNCS = {1: add_stories, 2: story_stats, 3: author_stats, 4: exit}

def main():
    if not os.path.exists(STORIES_DIR):
        os.mkdir(STORIES_DIR)
    if not os.path.exists(PDF_DIR):
        os.mkdir(PDF_DIR)    
    if not os.path.exists(TXT_DIR):
        os.mkdir(TXT_DIR)    
    if not os.path.exists(HTML_DIR):
        os.mkdir(HTML_DIR)
    
    while True:
        MAIN_MENU_FUNCS[get_menu_option(MAIN_MENU)]()

if __name__ == '__main__':
    main()
