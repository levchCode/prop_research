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

    image_url = "http://websdr.ewi.utwente.nl:8901/fullday/day" + \
        str(day) + ".png"
    img = Image.open(requests.get(image_url, stream=True).raw)
    img.save("waterfall_pictures/full/FULL " + str(day) + ".png")
    cropped_img = img.crop((4157, 958, 4163, 1000))
    cropped_img.save("waterfall_pictures/freq/7405 " + str(day) + ".png")
    stat = ImageStat.Stat(cropped_img.convert('L'))

    return maprange((0,255), (0, 200), stat.mean[0])


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
    # 17863 - 28 ноября 2018 года
    # 17917 - 21 января 2018 года

    # data = []

    # for i in range(17863, 17916):
    #     print(i)

    #     d = get_date_from_day(i)

    #     vol = get_volume(i)
    #     data.append(({"date": d, "day":i, "volume": vol}))
                
    # df = pd.DataFrame(data)
    # df.to_csv("sw.csv", index=False)

    # v = pd.read_csv('sw.csv')
    # i = pd.read_csv('a-k-flux.csv')

    # df = pd.DataFrame({"day":v["day"], "a":i["a"], "k":i["k"], "solar_flux":i["solar_flux"], "volume":v["volume"]})

    # df.to_csv("combined.csv", index=False)

    f = open("kp2019.wdc", "r").readlines()

    for i in f:
        y = i[0:2]
        m = i[2:4]
        d = i[4:6]

        date = datetime.date(2000 + int(y), int(m), int(d))


        kp = i[23:25]
        ap = i[47:49]

        print(date, kp, ap)