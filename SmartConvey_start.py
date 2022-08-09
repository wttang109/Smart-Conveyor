# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:28:45 2019

@author: Sunny
"""
import cv2

# start when input 1 #
def main(j):
    while True:
        vc = cv2.VideoCapture(0)
        try:
            rval , frame = vc.read()
        except:
            rval = False
            print('camera is not open')
            
        rval, frame = vc.read()
        cv2.imwrite('D:/{}_0_start.jpg'.format(j),frame)
        print('picture saved')
        break
        
        '''
#        turn_on = input('Turn on? ')
        if r_start == 1:
            vc = cv2.VideoCapture(1)
            try:
                rval , frame = vc.read()
            except:
                rval = False
                print('camera is not open')
            rval, frame = vc.read()
            cv2.imwrite('D:/{}_0_start.jpg'.format(j),frame)
            print('picture saved')
            break
        elif r_start == 'q':
            break
        else:
            continue
        '''

    '''
    try:
        if vc.isOpened():
            rval , frame = vc.read()
            
        else:
            rval = False
            print('camera is not open')
    except:
        return('nothing')
    # take a picture
    while rval:
        rval, frame = vc.read()
        cap_frame = cap_frame + 1
        if cap_frame == 20:
            cv2.imwrite('0_sc_{}.jpg'.format(j),frame)
            print('picture saved')
            break
    '''
    return frame
    vc.release()
if __name__=='__main__':
    main()
