import http.client
import datetime
import threading
import time
import os
from bs4 import BeautifulSoup

sum = 0
eof= False
filename = 'file.html'

def display_process():
    global sum,eof
    while eof:
        print(f'Downloaded {sum} bytes, {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')
        time.sleep(1) 

def queryTitle():
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    title_tag = soup.title.string
    if title_tag:
        invalid = ["[","]","<",">",":","\\","?","*","|"]
        title = title_tag
        for x in invalid:
            title = title.replace(x,'')
        title = title.strip()+'.html'
        os.replace(filename,title)
        return title
    else:
        return None


def downloadHandler(url):
    global sum, eof
    sum = 0  
    eof = False
    progress_thread = threading.Thread(target=display_process)
    if url.startswith("http://"):
        conn = http.client.HTTPConnection(url.split("://")[1].split("/")[0])
        path = '/' + '/'.join(url.split("://")[1].split("/")[1:])
    elif url.startswith("https://"):
        conn = http.client.HTTPSConnection(url.split("://")[1].split("/")[0])
        path = '/' + '/'.join(url.split("://")[1].split("/")[1:])
    else:
        print('Incorrect URL format, try again')
        return
    try:
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            with open(filename, 'wb') as file:
                buffer = bytearray(4096)  
                while True:
                    num_bytes_read = response.readinto(buffer)
                    sum += num_bytes_read

                    if (eof==False and sum>0):
                        eof=True
                        print('Watching process')
                        progress_thread.start()  
                    if num_bytes_read == 0:
                        if (eof):
                            eof=False
                            progress_thread.join()
                        break 
                    
                    file.write(buffer[:num_bytes_read])
            checkTitle = queryTitle() 
            title = checkTitle if checkTitle else filename

            print(f'Downloaded {sum} bytes, {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')
            print(f"Saved '{title}' with size {sum} bytes ")
            sum=0
        else:
            print(f"Failed to download file. Status: {response.status} {response.reason}")
        conn.close()
    except:
        print("Can't connect to server, check your URL")
    finally:
        eof=True
        sum=0


if __name__ == "__main__":
    quit = False
    while not quit:
        command = input("Input URL to download | Input 'q' to quit or Ctrl+C/Ctrl+Break\n>>>")
        if command !='q':
            downloadHandler(command)
        if command == 'q':
            quit=True
    print("QUIT")
