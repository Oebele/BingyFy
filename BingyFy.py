'''
Created on May 11, 2016

@author: x
'''
from urllib.request import urlopen
from re import findall, sub
import os


def getPictureUrl(url):
    with urlopen(url) as page:
        htmlPage = page.read()
        res = findall('g_img={url:\\s*"[\w|\\\|/|.]+"', str(htmlPage))
        if len(res) > 0:
            s = res[0]
            s = sub('[\\\|"]', '', s)
            s = s[s.find('/'):]
            return url + s
        else:
            raise


def getPicture(url):
    with urlopen(url) as picture:
        return picture.read()


def createPictureName(directory, url):
    return directory + os.sep + url.split(os.sep)[-1]


def main():
    url = "http://bing.com"
    cmd = "gsettings set org.gnome.desktop.background picture-uri 'file:///{}'"
    picture_path = os.environ["HOME"] + os.sep + '/Bing Pictures/'
    picture_url = getPictureUrl(url)
    picture_name = createPictureName(picture_path, picture_url)
    picture = getPicture(picture_url)
    command = cmd.format(picture_name)

    with open(picture_name, 'wb+') as f:
        f.write(picture)
    os.system(command)

if __name__ == "__main__":
    try:
        main()
    except:
        print("oops!")
