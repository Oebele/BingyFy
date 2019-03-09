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
    with urlopen(url) as page:
        htmlPage = page.read()
        res = findall(r'g_img={url:\\s*"[\w|\\\|/|.]+"', str(htmlPage))
        if len(res):
            s = res[0]
            s = sub('[\\\|"]', '', s)
            s = s[s.find('/'):]
            return url + s
        else:
            res = findall(r'<link.+id="bgLink".+/>', str(htmlPage))
            if not len(res):
                raise Exception("*** couldn't find picture url in page!")
            s = res[0]
            s = s[s.find('/'):]
            s = s[:s.find('"')]
            return url + s


def getPicture(url):
    with urlopen(url) as picture:
        return picture.read()


def createPictureName(directory, url):
    return directory + os.sep + url.split(os.sep)[-1]


def deleteOldPictures(picture_path):
    current_time = time.time()

    for f in os.listdir(picture_path):
        path = picture_path + '/' + f
        creation_time = os.path.getctime(path)
        extension = os.path.splitext(path)[1]
        if extension != '.py' and (current_time - creation_time) / (24 * 3600) > 7:
            os.unlink(path)
            print('{} removed'.format(f))


def main():
    url = "http://bing.com"
    if platform.linux_distribution()[0] == 'Ubuntu':
        cmd = "gsettings set org.gnome.desktop.background picture-uri 'file:///{}'"
    elif platform.linux_distribution()[0] == 'LinuxMint':
        cmd = "gsettings set org.cinnamon.desktop.background picture-uri 'file:///{}'"
    picture_path = os.environ["HOME"] + os.sep + '/Bing Pictures/'
    picture_url = getPictureUrl(url)
    picture_name = createPictureName(picture_path, picture_url)
    deleteOldPictures(picture_path)
    picture = getPicture(picture_url)
    command = cmd.format(picture_name)

    with open(picture_name, 'wb+') as f:
        f.write(picture)
    os.system(command)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("oops! ==> ", e.args)
