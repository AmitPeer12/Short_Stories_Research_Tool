import matplotlib.pyplot as plt
import random as rd

def extract_stats(file_path):
    with open(file_path, 'r', encoding='utf-8')  as story_file:
        word_list = {}
        content = story_file.read()
        chars_to_remove = ['\n', '\r', '\t', '\'', '\"', '?', '<', '>', '!', '.', ',', '–', '-', '`']
        for char in chars_to_remove:
            content = content.replace(char, '')
        content = content.split()
        for word in content:
            word_list[word] = 1 if word not in word_list else word_list[word] + 1
        
        word_list["all"] = len(content)
        return dict(sorted(word_list.items(), key=lambda item: item[1], reverse=True))
        

def show_story_stats(story):

    word_stats = extract_stats(story.story_file_path)
    word_count = word_stats.pop("all")
    uniqe_words = len(word_stats)
    
    count = min(int(input('How many words would you like to study? (up to 100) ')), 100)

    # x-coordinates of left sides of bars
    left = range(count)
    
    # heights of bars
    height = list(word_stats.values())[:count]
    
    # font size
    font_size = 14 - round(count / 20)
    # labels for bars
    ticks = []
    for tick in list(word_stats.keys())[:count]:
        ticks.append(tick[::-1])
    plt.xticks(range(count), ticks, rotation=45, fontsize=font_size)
    
    # plotting a bar chart
    plt.bar(left, height,
            width = 0.8, color = generate_colors(count))
    
    # naming the x-axis
    plt.xlabel('most frequant words in the story')
    # naming the y-axis
    plt.ylabel('word frequancy')
    # plot title
    plt.title(f'Stats for the story {story.story_name[::-1]}', {'fontsize':20, 'fontweight': 'bold'})
    # values of bars
    if count <= 50:
        for index, val in enumerate(height):
            plt.text(index - 0.3, val - 1.5, str(val), color='white', fontsize=10, fontweight='bold')
    # additionl stats
    plt.text(count / 5, height[0] - 3,
                f'The story contains {word_count} words,\nout of them {uniqe_words} are uniqe words.\nThat is {round(uniqe_words / word_count * 100, 2)}%',
                color='black',
                fontsize=font_size)
    # function to show the plot
    plt.show()

def generate_colors(number_of_colors):
    color = ["#" + ''.join([rd.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
    return color