import tinder_api
import fb_auth_token


# Seyed Majid Azimi
# 24.03.2018

import sys
sys.path.insert(0, '/home/majid/Ternow/gender_emotion')


from skimage import io
from pylab import *
import numpy as np
from datetime import datetime


import features

from matplotlib import pyplot as plt


now = datetime.now().strftime("%Y-%m-%d")


host = 'https://api.gotinder.com' #به خاطر این خط دیگه نیازی به  نیست import config.py or tinder_config_ex.py
_id = ''
images = []
def gettoken_id(fb_username, fb_password):
    global _id
    # وارد کنید  facebook email
    #fb_username = '@gmail.com'
    #  وارد کنید facebook password
    #fb_password = ''

    fb_access_token = fb_auth_token.get_fb_access_token(fb_username, fb_password)
    fb_user_id = fb_auth_token.get_fb_id(fb_access_token)

    #برای چک کردن اینکه یوزر اکی هست
    tinder_api.authverif()

    tinder_api.get_updates("2017-11-18T10:28:13.392Z")

    # Get Tinder Recommendations of people around you
    recommendations = tinder_api.get_recommendations()

    for index in range(len(recommendations['results'])):
        global images
        images = []

        name = recommendations['results'][index]['name']
        birth_date = features.calculate_age(recommendations['results'][index]['birth_date'])
        ping_time = recommendations['results'][index]['ping_time']
        if name == '5 GUM':
            continue

        _id = recommendations['results'][index]['_id']
        # print('before event.key _id is {}'.format(_id))

        print("name is {} and is {} years old  and bio is {}".
              format(name, birth_date, recommendations['results'][index]['bio']))

        number_of_subplots = len(recommendations['results'][index]['photos'])
        if number_of_subplots < 1:
            continue
        elif number_of_subplots == 1:
            fig, axes = plt.subplots()
        elif number_of_subplots <= 4:
            fig, axes = plt.subplots(1, number_of_subplots)
        elif number_of_subplots > 4:
            fig, axes = plt.subplots(int(number_of_subplots / 4) + 1, 4)
        fig.canvas.mpl_connect('key_press_event', press)
        subplots_adjust(hspace=0.000)

        # print(number_of_subplots)
        for i, v in enumerate(range(number_of_subplots)):
            p = recommendations['results'][index]['photos'][i]
            image = io.imread(p['url'])
            images.append(image)
            if number_of_subplots == 1:
                axes.imshow(image)
            elif number_of_subplots <= 4:
                axes[i].imshow(image)
            else:
                # print(int(i/4), int(i%4))
                axes[int(i / 4), int(i % 4)].imshow(image)
        plt.show(block=True)
        print("################################################################################################")


def press(event):
    global _id
    global images
    #print('press', event.key)
    sys.stdout.flush()
    #print("you pressed {}".format(event.key))
    #print(type(event.key))
    #while(event.key not in ['right', 'left', 'up']):
    #    print("you pressed {}".format(event.key))
    if event.key in ['right', 'left', 'up']:
        #print('after event.key _id is {}'.format(_id))

        if event.key == 'right':
            # Like a user
            tinder_api.like(_id)
            print('you liked')
            likecount = 0
            for _image in images:
                io.imsave('input_dataset/liked/profile_{}_{}.jpg'.format(_id, likecount), _image)
                likecount += 1
        elif event.key == 'left':
            # Dislike a user
            tinder_api.dislike(_id)
            print('you disliked')
            dislikecount = 0
            for _image in images:
                io.imsave('input_dataset/disliked/profile_{}_{}.jpg'.format(_id, dislikecount), _image)
                dislikecount += 1
        else:
            # Superlike a user
            tinder_api.superlike(_id)
            print('you superliked')
            likecount = 0
            for _image in images:
                io.imsave('input_dataset/liked/profile_{}_{}.jpg'.format(_id, likecount), _image)
                likecount += 1
        #plt.show(block=False)
        plt.close()
        


