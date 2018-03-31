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


# وارد کنید  facebook email 
fb_username = 'mitikomon86@gmail.com'
# وارد کنید facebook password 
fb_password = 'TMS2018'

fb_access_token = fb_auth_token.get_fb_access_token(fb_username, fb_password)
fb_user_id = fb_auth_token.get_fb_id(fb_access_token)

#برای چک کردن اینکه یوزر اکی هست
tinder_api.authverif()

tinder_api.get_updates("2017-11-18T10:28:13.392Z")

%matplotlib auto
#plt.ioff()
#plt.ion()
#inline


def press(event):
    #print('press', event.key)
    sys.stdout.flush()
    #print("you pressed {}".format(event.key))
    #print(type(event.key))
    if event.key in ['right', 'left', 'up']:
        #print('after event.key _id is {}'.format(_id))
        if event.key == 'right':
            # Like a user 
            tinder_api.like(_id)
            print('you liked')
        elif event.key == 'left':
            # Dislike a user 
            tinder_api.dislike(_id)
            print('you disliked')
        else:
            # Superlike a user 
            tinder_api.superlike(_id)
            print('you superliked')
        #plt.show(block=False)
        plt.close()
        
# Get Tinder Recommendations of people around you 
recommendations = tinder_api.get_recommendations()

for index in range(len(recommendations['results'])):
    name = recommendations['results'][index]['name']
    birth_date = features.calculate_age(recommendations['results'][index]['birth_date'])
    ping_time = recommendations['results'][index]['ping_time']
    if name == '5 GUM':
        continue

    _id = testid=recommendations['results'][index]['_id']
    #print('before event.key _id is {}'.format(_id))
    
    print("name is {} and is {} years old and bio is {}".
          format(name, birth_date,
                get_last_activity_date(now, ping_time),
                recommendations['results'][index]['bio']))

    number_of_subplots=len(recommendations['results'][index]['photos'])
    if number_of_subplots < 1:
        continue
    elif number_of_subplots == 1:
        fig, axes = plt.subplots()
    elif number_of_subplots <= 4:
        fig, axes = plt.subplots(1, number_of_subplots)
    elif number_of_subplots > 4:
        fig, axes = plt.subplots(int(number_of_subplots/4) + 1, 4)
    fig.canvas.mpl_connect('key_press_event', press)
    subplots_adjust(hspace=0.000)

    #print(number_of_subplots)
    for i,v in enumerate(range(number_of_subplots)):
        p = recommendations['results'][index]['photos'][i]
        image = io.imread(p['url'])
        #gen_emo = gender_emotion(image)
        if number_of_subplots == 1:
            axes.imshow(image)
        elif number_of_subplots <= 4:
            axes[i].imshow(image)
        else:
            #print(int(i/4), int(i%4))
            axes[int(i/4), int(i%4)].imshow(image)
    #for row in range(int(i/4), int(number_of_subplots/4) + 1):
    #    for column in range(int(i%4), 4):
    #        fig.delaxes(axes[row, column])
    plt.tight_layout()
    
    #plt.imshow(gen_emo)
    
    plt.show(block=True)
    print("################################################################################################")
