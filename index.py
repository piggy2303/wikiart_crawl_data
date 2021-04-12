import os
from PIL import Image
import requests


def string_on_csv(input):
    input = str(input).replace(",", " ")
    return input


def get_list_image(style_name):
    base_url = "https://www.wikiart.org/en/paintings-by-style/"
    params = {
        "select": "featured",
        "json": 2
    }
    x = requests.get(
        base_url+style_name,
        params=params,
        # timeout=3
    ).json()

    number_image = x["AllPaintingsCount"]
    number_image = int(number_image)
    print(number_image)
    loop_time = int(number_image / 60) + 1
    print(loop_time)

    text_file = open("./data_csv/"+style_name+".csv", "w+")
    text_file.write("id,title,year,artistName,image\n")

    for i in range(loop_time):
        params = {
            "select": "featured",
            "json": 2,
            "page": i+1
        }
        x2 = requests.get(
            base_url+style_name,
            params=params,
            # timeout=3
        ).json()
        x2 = x2["Paintings"]
        print(x2)

        for image_item in x2:
            text_file.write(
                string_on_csv(image_item["id"])+"," + string_on_csv(image_item["title"]) +
                ","+string_on_csv(image_item["year"])+"," +
                string_on_csv(image_item["artistName"]) +
                ","+string_on_csv(image_item["image"])+"\n"
            )

    text_file.close()


def crawl_data():
    f = open("./list_style.txt", "r")
    for i in f:
        i = i.strip().split('"')
        for item in i:
            try:
                if item[:4] == "/en/":
                    item_style = item.split("/")[3].split("?")[0]
                    print(item_style)
                    get_list_image(item_style)
            except:
                pass
    f.close()


# crawl_data()
# get_list_image("abstract-art")


def download_image(list_path):
    f = open(list_path, "r")

    list_downloaded = os.listdir("./data_image/abstract/")

    arr_img = []
    for count, i in enumerate(f):
        file_name = "abstract_"+str(count)+".jpg"

        if file_name not in list_downloaded:
            i = i.strip()
            print(count, i)
            try:
                img = Image.open(requests.get(i, stream=True, timeout=10).raw)
                img = img.convert("RGB")
                img = img.save("./data_image/abstract/"+file_name)
            except:
                print("time out or error")

    f.close()


download_image('./data/abstract-art.txt')
