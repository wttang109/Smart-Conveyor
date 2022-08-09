# -*- coding: utf-8 -*-
"""
Created on Thu May  9 13:18:23 2019

@author: Sunny
"""
import time
#import SmartConvey_start
import SmartConvey_OD
#import SmartConvey_focal
#from SmartConvey_find import find_marker, distance_to_camera

#import modbus_tk
import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import modbus_tk.defines as cst
#master = mt.TcpMaster('***', 502)  # modbus
import cv2
cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)
rob_x = 320
rob_y = 240
spotA_x = -79
spotA_y = 1004
spotB_x = -669
spotB_y = 953
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    j=time.strftime("%y%m%d_%H%M%S" , time.localtime())
    
#    start = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS,starting_address=0, quantity_of_x=14)# modbus
#    r_start = start[0]# modbus
    r_start =1


    if r_start ==1: # pick up
        time.sleep(1)
        rat_x = 405/454.4  # mm / px  big: 405/454.4   small: 345/329.6
        rat_y = 415/458.4  # mm / px  big: 415/458.4   small: 375/356.4
        print('###### Pick Up ######')
        start =  time.time()
        cv2.imwrite('D:/SC/{}_0_start.jpg'.format(j),frame)
        print('start done')
        pic_point, x_p, y_p = SmartConvey_OD.main(frame, j, det=123)
        print('OD done')
        
        #### calculate xy
        x_mm=round((x_p - rob_x) * rat_x,1)
        y_mm=round((y_p - rob_y) * rat_y,1)
        cv2.putText(pic_point, "( {} , {} , {} )mm".format(x_mm, -y_mm, 310),#, z=inches*2.54),
                (pic_point.shape[1] - 500, pic_point.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2) # 660mm
        print('x_mm= ',x_mm+spotA_x,', y_mm= ',-y_mm + 100 + spotA_y)
        cv2.imwrite('D:/SC/{}_3_point.jpg'.format(j), pic_point)
        end =  time.time()
        print("Execution Time(sec): ", end - start)
        
        # modbus
#        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS,  starting_address=0,
#                   output_value=[0,1,0,0,0,0,0,0,0,0,
#                                 int(round(x_mm-65.8,0)),
#                                 int(round(-y_mm + 100 + 812.92,0)) ,310])
        print('send pick up xy to robot')
        continue
    
    elif r_start ==2: # put down
        time.sleep(1)
        rat_x = 345/329.6  # mm / px  big: 405/454.4   small: 345/329.6
        rat_y = 375/356.4  # mm / px  big: 415/458.4   small: 375/356.4
        print('###### Put Down ######')
        start =  time.time()
        cv2.imwrite('D:/SC/{}_0_start.jpg'.format(j),frame)
        print('start done')
        pic_point, x_p, y_p = SmartConvey_OD.main(frame, j, det=45)   # box
        print('OD done')
        
        #### calculate xy
        x_mm=round((x_p - rob_x) * rat_x,1)
        y_mm=round((y_p - rob_y) * rat_y,1)
        cv2.putText(pic_point, "( {} , {} , {} )mm".format(x_mm, -y_mm, 213),#, z=inches*2.54),
                (pic_point.shape[1] - 500, pic_point.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2) # 660mm
        print('x_mm= ',x_mm+spotB_x,', y_mm= ',-y_mm + 100 + spotB_y)
        cv2.imwrite('D:/SC/{}_3_point.jpg'.format(j), pic_point)
        end =  time.time()
        print("Execution Time(sec): ", end - start)
        
        # modbus
#        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS,  starting_address=0,
#                   output_value=[0,1,0,0,0,0,0,0,0,0,
#                                 int(round(x_mm-628.21,0)),
#                                 int(round(-y_mm + 100 + 672.33,0)) ,213])
        print('send put down xy to robot')
        continue

    elif r_start ==3:   # box
        print('###### Put Down ######')
        start =  time.time()
        cv2.imwrite('D:/SC/{}_0_start.jpg'.format(j),frame)
        pic_point, x_p, y_p = SmartConvey_OD.main(frame, j, det=45)
        r_start=1
        # modbus
#        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS,  starting_address=0,
#                   output_value=[0,1,0,0,0,0,0,0,0,0,
#                                 xxx,
#                                 yyy ,213])
        end =  time.time()
        print("Execution Time(sec): ", end - start)
        continue
    
    elif key==27:
        break
    else:
        # big
        cv2.rectangle(frame, (int(rob_x*0.3), int(rob_y*0.03)), (int(rob_x*1.72), int(rob_y*1.94)), (0, 255, 0), 2)
#        # small
        cv2.rectangle(frame, (int(rob_x*0.48), int(rob_y*0.245)), (int(rob_x*1.51), int(rob_y*1.73)), (0, 255, 0), 2)
        cv2.circle(frame,(320, 240), 10, (0, 0, 255), 2)
        cv2.circle(frame,(320, 350), 10, (0, 150, 255), 2)
#        print('Stand by')
        continue
 
vc.release()
cv2.destroyWindow("preview")
    # R0 robot to ai
    # R1 ai to robot
    # 
    #R10=x
    #R11=y
    
    
#    time.sleep(1)
    #        frame = cv2.imread('D:/SC/{}_2_cut.jpg'.format(j))
#        w,h,focalLength = SmartConvey_focal.main(dis=36, w=6, h=6, image='D:/SC/box_brown_b.jpg', fix=0.1)
    
#      marker = find_marker(frame)
#     inches = distance_to_camera(w, focalLength, marker[1][1])
    
       # save result
#       cv2.putText(pic_point, "( {x} , {y} , {z} )cm".format(x=int((x_p-66)*0.89664), y=int((y_p-44)*0.89664), z=520),#, z=inches*2.54),
#                (pic_point.shape[1] - 500, pic_point.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX,
#                1, (0, 255, 0), 2) # 520mm
    
    #     cv2.imshow('object_detection', pic_point)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    #        r_start = 'q'
#    master.set_timeout(5.0)
    #        r_start = 'q'
#    master.set_timeout(5.0)
    
