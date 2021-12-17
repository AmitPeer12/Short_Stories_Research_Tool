import requests
import requests.exceptions
import os.path

api_key = '84668444eaa4feb6ac59b3522a264275f539f9d6d58dec127a48948c1e8b833c'
directory_for_stories = "C:\Python39\storiesProject"
files_types = {1: '.pdf', 2: '.txt', 3: '.xml', 4: '.html'}

def main():
    while True:
        try:
            story_serial_number = input("Please write the story serial number: ")
            api_url = f'https://staging.benyehuda.org/api/v1/texts/{story_serial_number}?key={api_key}&view=metadata&file_format=html'
            response = requests.get(api_url, timeout=6.0)
            if not response:
                print("There is not such a story, please try again")
                continue
            url = response.json().get('download_url')
            story_name = response.json().get('metadata').get('title')
            file_type = int(input("1)pdf\n2)txt\n3)xml\n4)html\nEnter file type:"))
            while file_type < 1 or file_type > len(files_types):
                print("Not a valid number, please pick a number from the following options.")
                file_type = int(input("1)pdf\n2)txt\n3)xml\n4)html\nEnter file type:"))
            story_download(url, story_name, files_types[file_type])
        # Exceptions handling
        except ConnectionError as e:
            print("Connection Error:", e)
            response = "no response"
        except requests.HTTPError as err:
            if err.code == 404:
                print("page not found")
            else:
                raise
        except requests.RequestException as e:
            print("Some Ambiguous Exception:", e)
        except requests.ConnectTimeout as e:
            print("Timeout Error:", e)


def story_download(url, story_name, file_type):
    story = requests.get(url, allow_redirects=True)
    story_directory = os.path.join(directory_for_stories, story_name + file_type)
    open(story_directory, 'wb').write(story.content)
    story.close()


if __name__ == '__main__':
    main()
