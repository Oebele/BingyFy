'''
Created on Nov 24, 2016

@author: oebele
'''
from urllib.request import urlopen
from re import findall, sub
import os
import time
import platform


def getPictureUrl(url):
    # https://www.bing.com/th?id=OHR.ValGardena_ROW3578236407_1920x1080.jpg&rf=LaDigue_1920x1080.jpg
    with urlopen(url) as page:
        htmlPage = page.read()
        res = findall(r'style="background-image: url\(/th\?id=OHR.\w*.jpg', str(htmlPage))
        if len(res):
            s = res[0]
            s = s.split('url(')[1]
            return f"{url}{s}"
        raise Exception("*** couldn't find picture url in page!")
 

def getPicture(url):
    with urlopen(url) as picture:
        return picture.read()


def createPictureName(directory, url):
    start = url.find('?id=')
    stop = url.find('&amp')
    file_name = url[start + 4: stop]
    return directory + file_name


def deleteOldPictures(picture_path):
    current_time = time.time()

    with os.scandir(picture_path) as sd:
        for f in sd:
            creation_time = os.path.getctime(f.path)
            extension = os.path.splitext(f.path)[1]
            if f.is_file() and extension != '.py' and (current_time - creation_time) / (24 * 3600) > 7:
                os.unlink(f.path)
                print('{} removed'.format(f))


def main():
    url = "https://bing.com"
    cmds = [
        "gsettings set org.gnome.desktop.background picture-uri 'file:///{}'",
        "gsettings set org.gnome.desktop.screensaver picture-uri 'file:///{}'",
        # "set-gdm-wallpaper picture-uri '{}'",
    ]
    picture_path = os.environ["HOME"] + os.sep + '/BingyFy/'
    picture_url = getPictureUrl(url)
    picture_name = createPictureName(picture_path, picture_url)
    deleteOldPictures(picture_path)
    picture = getPicture(picture_url)

    with open(picture_name, 'wb+') as f:
        f.write(picture)
    
    for cmd in cmds:
        command = cmd.format(picture_name)
        os.system(command)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("oops! ==> ", e.args)
