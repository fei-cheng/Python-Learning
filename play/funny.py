import os
import re
import Image
import urllib
import urllib2


def getHtml(url):
    return urllib.urlopen(url).read()
 
def getImage(html):
    img_re = re.compile("""<img.*?src="(.*?)".*?>""")
    img_list = img_re.findall(html)
    img_folder = ('img')
    
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    for img_url in img_list:
        img_name = img_url.split('/')[-1]
        try:
            urllib.urlretrieve(img_url, os.path.join(img_folder, img_name))
        except:
            continue

def isFunny(img_path):
    img = Image.open(img_path).convert('YCbCr')
    width, height = img.size
    img_data = img.getdata()

    cnt = 0
    for i, ycbcr in enumerate(data):
        y, cb, cr = ycbcr
        if 86 <= cb <= 117 and 140 <= cr <= 168:
            cnt += 1
    return cnt > (0.3 * width * height)

if __name__ == '__main__':
    getImage(getHtml("http://www.ifeng.com"))

