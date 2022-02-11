from matplotlib import pyplot as plt
from story_stats import extract_stats
import queue

myQueue = queue.Queue()
stats = {}

def collect_author_stories(story):
    if (story == None):
        return
    myQueue.put(extract_stats(story.story_file_path))

def show_author_stats(author, number_of_stories):
    while not myQueue.empty():
        word_stats = myQueue.get()
        word_count = word_stats.pop("all")
        for word in word_stats.keys():
            stats[word] += word_stats[word] / word_count
    
    for word in stats.keys():
        stats[word] /= number_of_stories
    count = min(int(input('How many words would you like to study? (up to 100) ')), 100)

    # x-coordinates of left sides of bars
    left = range(count)
    
    # heights of bars
    height = list(stats.values())[:count]
    
    # font size
    font_size = 14 - round(count / 10)
    # labels for bars
    ticks = []
    for tick in list(stats.keys())[:count]:
        ticks.append(tick[::-1])
    plt.xticks(range(count), ticks, rotation=45, fontsize=font_size)
    
    # plotting a bar chart
    plt.bar(left, height,
            width = 0.8, color = ['red', 'green', 'blue'])
    
    # naming the x-axis
    plt.xlabel('most frequant words in the story')
    # naming the y-axis
    plt.ylabel('word frequancy')
    # plot title
    plt.title(f'Stats for the Author {author.name[::-1]}', {'fontsize':20, 'fontweight': 'bold'})
    # values of bars
    if count <= 50:
        for index, val in enumerate(height):
            plt.text(index - 0.3, val - 1.5, str(val), color='white', fontsize=10, fontweight='bold')
    # additionl stats
    plt.text(count / 5, height[0] - 3,
                f'The story contains {count} words,\nout of them {count} are uniqe words.\nThat is {round(count / count * 100, 2)}%',
                color='black',
                fontsize=font_size)
    # function to show the plot
    plt.show()
