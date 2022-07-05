import os
from dotenv import load_dotenv
import requests as req
import random as rnd
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from instabot import Bot

load_dotenv()


def url_to_img(url):
    """
    change the url into a numpy image

    :param url:
    :return:
    """
    r = req.get(url, stream=True)
    img = np.array(Image.open(r.raw))
    return img


def show_image(img):
    """
    showing images
    :param img:
    """
    plt.imshow(img)
    plt.show()


def get_random_query():
    query_list = ['landscapes', 'mountain', 'sea', 'beach', 'sky', 'aurora']

    return query_list[int(rnd.uniform(0, 1) * len(query_list))]


def get_random_result(photo_links):
    print(f"Getting Photos from : {photo_links}")
    data = req.get(photo_links)
    results = data.json()['results']
    return results[int(rnd.uniform(0, 1) * len(results))]['urls']['regular']


def get_random_quotes():
    url = "https://free-quotes-api.herokuapp.com/"

    res = req.get(url)

    quotes = res.json()['quote']
    creator = res.json()['author']

    if creator == "":
        creator = "Anonymous"

    return [quotes, creator]


def add_rectangle(img, text, font_scale, font, thickness):
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (img.shape[0] + text_size[1]) // 2

    overlay = img.copy()
    cv2.rectangle(overlay,
                  pt1=(0, text_y - text_size[1] - 20),
                  pt2=(img.shape[1], text_y + text_size[1]),
                  color=(255, 255, 255),
                  thickness=-1)
    alpha = 0.6
    new_img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    return [text_x, text_y, new_img]


def put_text_in_image(text, img):
    # add text in image centered and in the middle of the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    thickness = 2

    [text_x, text_y, new_img] = add_rectangle(img, text,
                                              font_scale, font,
                                              thickness)

    edited_img = cv2.putText(
        new_img,
        text,
        org=(text_x, text_y),
        fontFace=font,
        fontScale=font_scale,
        color=(0, 0, 0),
        thickness=thickness
    )

    show_image(edited_img)

    save = Image.fromarray(edited_img)
    save.save('xd.jpg')


def get_quotes(img):
    [quotes, creator] = get_random_quotes()
    put_text_in_image(f"Quotes from {creator}", img)
    post_to_ig(quotes)


def post_to_ig(quotes):
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    print(username, password)
    bot = Bot()
    bot.reset_cache()

    bot.login(username=username, password=password)
    bot.upload_photo("xd.jpg", caption=f"'{quotes}'"
                                       f"Tags : "
                                       f"#quotes #landscape #sea #beach #sky #aurora #tourist #spots #touristplaces "
                                       f"#nature #outdoor #skyporn #skyline #travel #travelphotography "
                                       f"#naturephotography #nature_sultans #travelingram #traveling")


def get_photo():
    """
    getting the photos and showing the image
    """
    photo_links = f"https://api.unsplash.com/search/photos/?" \
                  f"client_id={os.getenv('UNSPLASH_KEY')}" \
                  f"&query={get_random_query()}" \
                  f"&orientation=squarish"
    photo_url = get_random_result(photo_links)
    img = url_to_img(photo_url)
    show_image(img)
    get_quotes(img)


# get_random_quotes()
get_photo()
