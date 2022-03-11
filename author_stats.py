import matplotlib.pyplot as plt
from story_stats import extract_stats, generate_colors

stories = []

def collect_author_stories(story):
    if (story == None):
        return
    stories.append(extract_stats(story.story_file_path))

def show_author_stats(author, number_of_stories):
    stats = {}
    for word_stats in stories:
        word_count = word_stats.pop("all")
        for word in word_stats.keys():
            if word in stats:
                stats[word] += word_stats[word] / word_count
            else: stats[word] = word_stats[word] / word_count
    
    for word in author.name.split(' '):
        if word in stats:
            stats.pop(word)
    
    for word in stats.keys():
        stats[word] /= number_of_stories
    
    count = min(int(input('How many words would you like to study? (up to 100) ')), 100)
    stats = dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))

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
            width = 0.8, color = generate_colors(count))
    
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