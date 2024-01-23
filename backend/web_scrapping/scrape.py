import requests 
from bs4 import BeautifulSoup
from collections import defaultdict
import uuid
import os

class Scrape: #
    def __init__(self, url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0(windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Accept-Language': 'en-GB,en;q=0.5',  # English
            'Referer': 'https://google.com',
            'DNT': '1'  # 1-> True do not track
        }
        self.url = url
        self.session = requests.Session()
        self.response = self.session.get(url, headers=self.headers)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.cookie = defaultdict(list)

    def savepage(self, 
                 folder_loc: str =None, # specify the folder where u want to save if not 
                 html_file_name:str=None # 
                 ):
        """Saves the HTML content of the page to a file.
        
        Args:
            page_name (str): The name of the file to save the page to. Defaults to 'index'.
        
        Writes the HTML content of the page response to an HTML file with the given 
        page_name. Prettifies the HTML before writing.
        """
        status = self.response.status_code
        try :
            if folder_loc is None:
                folder_loc = f'HTML File-{uuid.uuid4().hex}'
                os.makedirs(folder_loc)
            html_file_name = f'{uuid.uuid4().hex}.html'
            saved_path = os.path.join(folder_loc,html_file_name)

            with open(saved_path, 'w', encoding='utf-8') as f:
                content = self.response.text
                soup = BeautifulSoup(content, 'html.parser')
                prettified_html = soup.prettify()
                f.write(prettified_html)
        except Exception as e:
            print(e,f'status code {status}')
            

    def get_file_fromBinary(self,binary_data:bytes):
        """Gets the image format from the binary data.
        
        This function checks the binary data against known file signatures 
        to determine the image format. It returns the image format string 
        if a match is found, otherwise False.
        
        The file_signatures dictionary contains binary signatures as keys 
        and the corresponding image format strings as values. The binary 
        data is checked against each signature in order until a match is found.
        
        This allows detecting common image formats like JPEG, PNG, GIF from 
        binary data. Additional formats can be added to the dictionary as needed.
        """
        try: 
            file_signatures = {
                b'\xFF\xD8\xFF': 'JPEG',
                b'\x89PNG\r\n\x1A\n': 'PNG',
                b'\x47\x49\x46\x38\x37\x61': 'GIF',
                b'\x42\x4D': 'BMP',
                b'\x00\x00\x01\x00': 'ICO',
                b'\x52\x49\x46\x46': 'WEBP',
                b'\x42\x50\x47\xFB': 'BPG',  # BPG (Better Portable Graphics)
                b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'PNG',
                b'\x25\x50\x44\x46': 'PDF',
                b'\x49\x49\x2A\x00': 'TIFF',
                b'\x4D\x4D\x00\x2A': 'TIFF',
                b'\x00\x00\x00\x0C\x6A\x50\x20\x20': 'JP2',  # JPEG 2000
                b'\x46\x4F\x52\x4D': 'IFF',  # IFF (Interchange File Format)
                b'\x00\x00\x02\x00': 'ICO',  # Icon file
                b'\x00\x00\x01\x00': 'ICO',  # Icon file
                b'<svg': 'SVG',  # SVG detection based on the presence of <svg tag
                b'%PDF': 'PDF',  # PDF detection
                # Add more as needed
                }
            for signature, image_format in file_signatures.items():
                if binary_data.startswith(signature):
                    return image_format
            return False
        except Exception as e:
            print(e)
            

    def pullImages(self, 
                   folder_loc=None,
                   Src:str='src'):
        """Pulls all images from the HTML content and saves them to a folder.
        
        This method finds all <img> tags in the HTML content, gets the image 
        binary data using the src URL, determines the file format from the 
        binary signature, generates a unique filename, and saves the image 
        to the provided folder location.
        
        A default folder with a unique name will be created if no folder is specified.
        Any exceptions are printed but execution continues.
        """
        images = self.soup.find_all('img')
        # Generate a unique folder if folder_loc is not provided
        if folder_loc is None:
            folder_loc = f'images_{uuid.uuid4().hex}'
            os.makedirs(folder_loc)
        # from what i have observed many websites have either stored in src or data-srcset or 
        for src in images:
            try:
                source = src[Src]
                binary_data = requests.get(source).content
                file_format = self.get_file_fromBinary(binary_data)
                unique_filename = f'{uuid.uuid4().hex}.{file_format.lower()}'
                save_path = os.path.join(folder_loc, unique_filename)

                with open(save_path, 'wb') as f:
                    f.write(binary_data)

                print(f'Image saved as: {save_path}')
            except Exception as e:
                print(e)
            
        
if __name__ == '__main__':
    # if you want to experiment you can uncomment the code below to check if this is working or not 
    # splash = 'https://unsplash.com/'
    # page = Scrape(splash)
    # save_page = page.savepage()
    # s = page.pullImages()
    # print('hurray its working..!!')
    pass
