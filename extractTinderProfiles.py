import tinder_api
# Seyed Majid Azimi
# 24.03.2018

import tinder_api
import fb_auth_token
from skimage import io
from pylab import *
from datetime import datetime
import features
from matplotlib import pyplot as plt
import warnings
import matplotlib.patheffects as path_effects
import time
import sys

warnings.filterwarnings('ignore')

now = datetime.now().strftime("%Y-%m-%d")
_id = ''
images = []
like = 0
dislike = 0
txt = None
fig = None
def gettoken_id(fb_username, fb_password):

    fb_username = 'mitikomon86@gmail.com'
    fb_password = 'TMS2018'

    global _id
    global fig

    host = 'https://api.gotinder.com'


    fb_access_token = fb_auth_token.get_fb_access_token(fb_username, fb_password)
    fb_user_id = fb_auth_token.get_fb_id(fb_access_token)


    tinder_api.get_auth_token(fb_access_token, fb_user_id, host)
    print("#################################################")

    while (like < 30 or dislike < 30 ):

        try:
            recommendations = tinder_api.get_recommendations()

        except:
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

        print("name is {} and is {} years old  and bio is {}".
              format(name, birth_date, recommendations['results'][index]['bio']))
        
        try:
            if recommendations['results'][index]['bio']:
                fig = plt.figure('Biography', figsize=(6,4))
                t = (recommendations['results'][index]['bio'])
                text = fig.text(0.5, 0.5, t, ha='center', va='center', size=10)
                text.set_path_effects([path_effects.Normal()])
                plt.axis('off')
                plt.tight_layout()
                plt.show(block=False)
        except:
            plt.close()
            pass

        number_of_subplots = len(recommendations['results'][index]['photos'])
        if number_of_subplots < 1:
            continue
        elif number_of_subplots == 1:
            fig, axes = plt.subplots(figsize=(15,15))
        elif number_of_subplots <= 4:
            fig, axes = plt.subplots(1, number_of_subplots,figsize=(15,15))
        elif number_of_subplots > 4:
            fig, axes = plt.subplots(int(number_of_subplots / 4) + 1, 4, figsize=(15,15))
        fig.canvas.mpl_connect('key_press_event', press)
        subplots_adjust(hspace=0.000)

        for i, v in enumerate(range(number_of_subplots)):
            p = recommendations['results'][index]['photos'][i]
            image = io.imread(p['url'])
            images.append(image)
            
            if number_of_subplots == 1:
                axes.axis('off') 
                axes.imshow(image)
                axes.axis('off')
            elif number_of_subplots <= 4:
                axes[i].axis('off')
                axes[i].imshow(image)
                axes[i].axis('off')
            else:
                axes[int(i / 4), int(i % 4)].axis('off')
                axes[int(i / 4), int(i % 4)].imshow(image)
                axes[int(i / 4), int(i % 4)].axis('off')

        if number_of_subplots == 5:
            for j in range(4):
                axes[int(i / 4), int(j)].axis('off')
         
        elif number_of_subplots > 5:
            while i%4 != 0:
                axes[int(i / 4), int(i % 4)].axis('off')
                i += 1


        plt.tight_layout()
        #plt.axis('off')
        plt.show(block=True)

        print("###################################")


    
def press(event):
    global _id
    global images
    global like
    global dislike
    global txt
    global fig
    sys.stdout.flush()
    print('you pressed {}'.format(event.key))
    if event.key == 'e':
        print('exit')
        sys.exit()
        raise SystemExit()

    if event.key in ['right', 'left', 'up']:
        if event.key == 'right':
            # Like a user
            tinder_api.like(_id)
            print('you liked')
            text = 'LIKED'
            count = 0
            for _image in images:
                io.imsave('/home/majid/Ternow-Lovai/data/liked/profile_{}_{}.jpg'.format(_id, count), _image)
                count += 1
                like += 1
                #break
        elif event.key == 'left':
            # Dislike a user
            tinder_api.dislike(_id)
            print('you disliked')
            text = 'DISLIKED'
            count = 0
            for _image in images:
                io.imsave('/home/majid/Ternow-Lovai/data/disliked/profile_{}_{}.jpg'.format(_id, count), _image)
                count += 1
                dislike += 1
                #break
        elif event.key == 'top':
            # Superlike a user
            tinder_api.superlike(_id)
            print('you superliked')
            text = 'SUPERLIKED'
            count = 0
            for _image in images:
                io.imsave('/home/majid/Ternow-Lovai/data/liked/profile_{}_{}.jpg'.format(_id, count), _image)
                count += 1
                like += 1
                #break

        #plt.text(5, 5, text, style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
        if text in ['LIKED', 'SUPERLIKED']:
            txt = plt.text(.5 , .5, text, fontsize=30, style='italic', bbox={'facecolor':'green', 'alpha':0.5, 'pad':1})
        elif text == 'DISLIKED':
            txt = plt.text(.5 , .5, text, fontsize=30, style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':1})

        fig.canvas.draw()
        time.sleep(1) 
        #plt.show(block=False)
        plt.close('all')




