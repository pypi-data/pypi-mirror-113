import os
from tkinter import *
import time
import requests


class Downloader:
    def __init__(self, url,path):
        self.url = url
        self.path = path

    def download(self):
        try:
            download_link = requests.get(self.url)
            master = Tk()
            master.withdraw()
            with open(self.path, 'wb') as f:
                f.write(download_link.content)
            print('Downloaded Successfully!')
            time.sleep(1)
            while True:
                file = input('Do you want to open the downloaded file right now? (Y/N) :')
                if file=='y'.capitalize() or file=='y':
                    os.startfile(self.path)
                    break

                elif file=='n'.capitalize() or file=='n':
                    print('Ok!')
                    break

                else:
                    continue

        except requests.exceptions.ConnectionError:
            raise ConnectionError('Please check your internet connection and try again.')

        except FileNotFoundError:
            pass

        except:
            raise Exception('Oops, an error occurred.')

