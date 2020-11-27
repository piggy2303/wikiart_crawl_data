import requests


def get_list_image(style_name):
    base_url = "https://www.wikiart.org/en/paintings-by-style/"
    params = {
        "select": "featured",
        "json": 2
    }
    x = requests.get(
        base_url+style_name,
        params=params,
        timeout=3
    ).json()

    number_image = x["AllPaintingsCount"]
    number_image = int(number_image)
    print(number_image)
    loop_time = int(number_image / 60) + 1
    print(loop_time)

    text_file = open("./data/"+style_name+".txt", "w+")

    for i in range(loop_time):
        params = {
            "select": "featured",
            "json": 1,
            "page": i+1
        }
        x2 = requests.get(
            base_url+style_name,
            params=params,
            timeout=3
        ).json()
        print(x2)

        for image_item in x2:
            text_file.write(image_item["image"]+"\n")

    text_file.close()


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
