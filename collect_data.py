#
# x0 (date)
# x2 (k-index)
# x3 (solar flux)
# y (volume of a station 7405 kHz, in db)
#

import requests
import datetime
import pandas as pd
from PIL import Image, ImageStat


def maprange(a, b, s):
	(a1, a2), (b1, b2) = a, b
	return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def get_volume(day):

    image_url = "http://websdr.ewi.utwente.nl:8901/fullday/day" + str(day) + ".png"

    img = Image.open(requests.get(image_url, stream=True).raw)

    cropped_img = img.crop((4157, 958, 4163, 1000))
    cropped_img.save("waterfall_pictures/freq/7405 " + str(day) + ".png")
    stat = ImageStat.Stat(cropped_img.convert('L'))

    return stat.mean[0]/4


def get_date_from_day(day):
    # 16514 is March 20th 2015
    start = 16514
    startdate = datetime.datetime.strptime("20/03/15", "%d/%m/%y")
    return startdate + datetime.timedelta(days=(day-start))

def get_day_from_date(d):
    start = 16514
    startdate = datetime.datetime.strptime("20/03/15", "%d/%m/%y")
    current = datetime.datetime.strptime(d, "%d/%m/%y")
    return start + abs((current - startdate).days)



if __name__ == "__main__":
    #17897 - 1 января 2019 года
    #17986 - 31 марта 2019 года

    SNRs = []
    dates = []
    days = []
    ais = []
    ks = [] 
    f = open("indexes.txt", "r").readlines()

    for i in range(17897, 17986):
        d = get_date_from_day(i)

        vol = get_volume(i)
        print("Processed day {0} : vol: {1}".format(i-17897, vol))
        dates.append(d)
        days.append(i)
        SNRs.append(vol)
                
        ks.append(int(f[i-17897][74]))
        ais.append(int(f[i-17897][60:62]))
        
    df = pd.DataFrame({"day":days, "a":ais, "k":ks, "volume":SNRs})
    #df = pd.DataFrame({"a":ais, "k":ks})
    df.to_csv("data.csv", index=False)