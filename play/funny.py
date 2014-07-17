import os
import re
import Image
import shutil
import urllib
import urllib2


def getHtml(url):
    return urllib.urlopen(url).read()
 
def getImage(html, img_folder):
    img_re = re.compile("""<img.*?src="(.*?)".*?>""")
    img_list = img_re.findall(html)
    
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    for img_url in img_list:
        img_name = img_url.split('/')[-1]
        try:
            urllib.urlretrieve(img_url, os.path.join(img_folder, img_name))
        except:
            continue

def haveFun(img_folder, img_name, minimumSize):
    funny_folder = os.path.join(img_folder, 'funny')
    img_path = os.path.join(img_folder, img_name)
    img = Image.open(img_path).convert('YCbCr')
    width, height = img.size
    if min(width, height) < minimumSize:
        return
    if not os.path.exists(funny_folder):
        os.mkdir(funny_folder)
    img_data = img.getdata()
    
    """
    cnt = 0
    for i, ycbcr in enumerate(img_data):
        y, cb, cr = ycbcr
        if 86 <= cb <= 117 and 140 <= cr <= 168:
            cnt += 1
    if cnt > (0.3 * width * height):
        shutil.move(img_path, funny_folder)
    """
    
    cnt, total = 0, 0
    for i, ycbcr in enumerate(img_data):
        y, cb, cr = ycbcr
        if 66 <= cb <= 137 and 120 <= cr <= 188:
            total += 1
            if 86 <= cb <= 117 and 140 <= cr <= 168:
                cnt += 1
    if (total > (0.3 * width * height)) and (cnt > 0.3 * total):
        shutil.move(img_path, funny_folder)

def findAllFunnyPicOfSepecifiedUrl(url, minimumSize=100):
    img_folder = 'img'
    getImage(getHtml(url), img_folder)
    for img in os.listdir(img_folder):
        haveFun(img_folder, img, minimumSize)

if __name__ == '__main__':
    try:
        findAllFunnyPicOfSepecifiedUrl("http://dongxi.douban.com/doulist/1230768/?r=9&c=1_1", 10)
    except:
        print "Sorry, error occurs!!!"

