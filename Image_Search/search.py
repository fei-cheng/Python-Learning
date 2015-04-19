import os
import glob
from math import sqrt
from PIL import Image

suffixes = ['jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG']

def calculate_color_histogram(image):
    width = image.size[0]
    height = image.size[1]
    colorHistogram = [0] * 64

    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
            index = (r / 64) * 1 + (g / 64) * 4 + (b / 64) * 16
            colorHistogram[index] += 1
            
    return colorHistogram

def calculate_pearson_similarity(p1, p2):
    """
        Returns the Pearson correlation coefficient for p1 and p2.
        See: http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
    """
    length = len(p1)
    if length != len(p2):
        raise
    
    # Sums
    sum1 = sum(p1)
    sum2 = sum(p2)

    # Sums of the squares
    sum1Sq = sum([pow(item, 2) for item in p1])
    sum2Sq = sum([pow(item, 2) for item in p2])

    # Sum of the products
    pSum = 0
    for index in range(length):
        pSum += p1[index] * p2[index]
        
    # Calculate r (Pearson score)
    num = length * pSum - sum1 * sum2
    den = sqrt((length * sum1Sq - pow(sum1, 2)) * (length * sum2Sq - pow(sum2, 2)))
    if den == 0:
        return 0
    return num / den

def calculate_cosine_similarity(p1, p2):
    length = len(p1)
    if length != len(p2):
        raise

    # Sums of the squares
    sum1Sq = sum([pow(item, 2) for item in p1])
    sum2Sq = sum([pow(item, 2) for item in p2])

    # Sum of the products
    pSum = 0
    for index in range(length):
        pSum += p1[index] * p2[index]
        
    # Calculate similarity
    den = sqrt(sum1Sq * sum2Sq)
    if den == 0:
        return 0
    return pSum / den
    
def is_image(filePath):
    return filePath.split(".")[-1] in suffixes

def load_image(imagePath):
    return Image.open(imagePath)

def search_image(src, tgtDir):
    """
        src: the path of source image
        tgtDir: the directory of target image
    """
    if (not os.path.isfile(src)) or (not os.path.isdir(tgtDir)):
        return
    
    if not is_image(src):
        return
    srcColorHistogram = calculate_color_histogram(load_image(src))

    targetPath = None
    maxSimilarity = -1
    for item in os.listdir(tgtDir):
        filePath = os.path.join(tgtDir, item)
        if not is_image(filePath):
            continue
        imageColorHistogram = calculate_color_histogram(load_image(filePath))
        # similarity = calculate_cosine_similarity(srcColorHistogram, imageColorHistogram)
        similarity = calculate_pearson_similarity(srcColorHistogram, imageColorHistogram)
        print 'similarity: ', str(similarity) + ', comparing with ' + filePath + '......'
        if similarity >= maxSimilarity:
            targetPath = filePath
            maxSimilarity = similarity

    return maxSimilarity, targetPath


if __name__ == "__main__":
    print search_image("2009.jpg", "target")

