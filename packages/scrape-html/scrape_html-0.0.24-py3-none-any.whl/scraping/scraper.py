import os
import csv
from .proxy import Proxy
from pydantic import HttpUrl
from typing import List, Dict
from selenium import webdriver

class PageSources(Proxy):
    def __init__(self, url: HttpUrl = None, headless: bool = True, proxy: str = None) -> None:
        super().__init__(headless, proxy) # add chrome options and proxy
        self.__chrome = webdriver.Chrome(chrome_options=self.options)
        self.__url = url
        self.__error = 40


    def get_current_html(self) -> str:
        """
        It will take a while.
        """
        try:
            print('Loading html...\n')
            self.__chrome.get(self.__url) # open url
            if len(self.__chrome.page_source) < self.__error:
                raise Exception('Page not found')    
            return self.__chrome.page_source.encode("utf-8") # html in string
        except:
            raise Exception('schema http or https, TLD required, max length 2083')
    

    def get_host_page_name(self) -> str:
        return self.__url[self.__url.find('//')+2:self.__url.find('.')] # Host 'https://google.com' get 'google'


    def close_browser(self) -> bool: # Quit browser
        self.__chrome.close()
        return True


    def save(self, directory: str='web_data') -> None:
        # root save directory
        path = os.getcwd()
        path_dir = f'{path}/{directory}'
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)
        with open(f"{path_dir}/{self.get_host_page_name()}_{len(os.listdir(path_dir))+1}.html", "w", encoding='utf-8') as code:
            code.write(f'{self.__chrome.page_source}') # Save data in directory web_data
            code.close()
    

    @classmethod
    def get_multiple_html(cls, links: List[str]) -> None: # Iteration with multiple link
        for count, link in enumerate(links):
            print(f'Link # {count}')
            new_instance = cls(link)
            new_instance.get_current_html()
            new_instance.save()
        print('Finished ...')


    def get_csv_columns(self, dict_data: Dict[str, str]) -> List[str]:
        return [column for column in dict_data[-1].keys()] # {'column':'value'} get every columns


    def save_csv(self, dict_data: Dict[str, str], outfile: str = 'output.csv', open_file: str = 'w') -> None:
        """
        dict_data = [
            {'example': 'lorem'},
            {'example': 'lorem'},
            ...
        ]
        """
        try:
            with open(outfile, open_file, newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=self.get_csv_columns(dict_data))
                writer.writeheader() # Write column name
                for data in dict_data:
                    writer.writerow(data) # Write values
        except ValueError as e:
            print(f'Fix it, and run again: {e}')
        print('\nFinished...')