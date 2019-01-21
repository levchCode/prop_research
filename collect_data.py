#
# x0 (date)
# x1 (number_of_sun spots today)
# x2 (something else)
# y (volume of a station 7405 kHz, in db)
#

import requests
import datetime
import pandas as pd
from PIL import Image, ImageStat


def get_volume(day):

    image_url = "http://websdr.ewi.utwente.nl:8901/fullday/day" + \
        str(day) + ".png"
    img = Image.open(requests.get(image_url, stream=True).raw)
    img.save("waterfall_pictures/full/FULL " + str(day) + ".png")
    cropped_img = img.crop((4157, 958, 4163, 1000))
    cropped_img.save("waterfall_pictures/freq/7405 " + str(day) + ".png")
    stat = ImageStat.Stat(cropped_img.convert('L'))
    return stat.mean[0]


def get_date_from_day(day):
    # 16514 is March 20th 2015
    start = 16514
    startdate = datetime.datetime.strptime("03/20/15", "%m/%d/%y")
    return startdate + datetime.timedelta(days=(day-start))


if __name__ == "__main__":
    r = requests.get("https://services.swpc.noaa.gov/json/predicted_monthly_sunspot_number.json").json()
    
    data = []
    #range(17863, 17916)
    for i in range(17863, 17864):
        d = get_date_from_day(i)
        for k in r:
            if datetime.date.fromisoformat(k["date"]).month == d.month and datetime.date.fromisoformat(k["date"]).year == d.year:
                num_spots = k["ssn_predicted"]
                flux = k["flux_predicted"]
        vol = get_volume(i)
        data.append(({"date": d, "num_spots": num_spots, "flux": flux, "volume": vol}))

    df = pd.DataFrame(data)
    df.to_csv("sw.csv", index=False)
