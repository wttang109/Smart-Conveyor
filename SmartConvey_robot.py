# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:00:30 2019

@author: Sunny
"""

import time
import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import modbus_tk.defines as cst
master = mt.TcpMaster('***', 502)  # modbus
import cv2

def ready_cmd(s,re):
    while True:
        start = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS,
                               starting_address=0, quantity_of_x=14)# modbus
        stop = start[0]
        if stop ==s:
            return re
    
def main(pic_point, x_p, y_p, d_egg, j, r_start, bbstep, mode, empty_num):
    root = 'D:/SC'
    rat_x = 367/329 # Atop box mm/px     367/329
    rat_y = 330/288 # Atop box mm/px     330/288
    cam_x = 320 # px
    cam_y = 240 # px
    
    h_B = int(129.7)# mm
    h_F = int(132)# mm
    cam_disx = 55 # mm
    cam_disy = 0
    
    robB_x = int(round(-1047,0)) # mm   #
    robB_y = int(round(-35.3,0))            #
    robF_x = int(round(1084.7,0)) # 12/3
    robF_y = int(round(-64,0))  # 12/3
    
    fxfix = -24 # mm  # 12/3
    fyfix = 0        # 12/3
    bxfix = 24
    byfix = -4
    def sendxy(robx, roby, R2, x, y, cdx, cdy, xfix, yfix, h):
        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS,  starting_address=0,
                                    output_value=[0,1,R2,0,0,0,0,0,0,0,
                                    int(round(robx + y + cdx + xfix, 0)),
                                    int(round(roby + x + cdy + yfix, 0)), h])

    def calxymm(x_p, y_p, pic, j):
        x_mm=round((x_p - cam_x) * rat_x,1)
        y_mm=round((y_p - cam_y) * rat_y,1)
        cv2.putText(pic, "( {} , {} , {} )mm".format(x_mm, -y_mm, h_F),#, z=inches*2.54),
                (pic.shape[1] - 500, pic.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2) # 660mm
    #                print('1x_mm= ', x_mm, ', 1y_mm= ', y_mm, '+', cam_disx)
        print('x_p= ', x_p, ', y_p= ', y_p)
        cv2.imwrite(root + '/{}_3_point.jpg'.format(j), pic)
        return x_mm, y_mm
    
#    while True:
#        start = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS,
#                               starting_address=0, quantity_of_x=14)# modbus
#        r_start = start[0]
        
        
        
    if r_start ==1:# pick up (robF)
        if pic_point == 'box':
            print('1 F only box')
            return 1
        elif d_egg !=0:
            #### calculate xy
            x_mm, y_mm = calxymm(x_p, y_p, pic_point, j)
                
            # modbus  xy reverse
            sendxy(robx=robF_x, roby=robF_y, R2=0, x=-x_mm, y=-y_mm, cdx=cam_disx, cdy=-cam_disy,
                       xfix=fxfix, yfix=fyfix, h=h_F)
            
            ready_cmd(2,33)
#                return 1
#                
        
    elif r_start ==2: # put down (robB)
        if pic_point == 'box':
            print('2 B only box')
            return 1
        elif mode==1:  # still have defect egg, robot back to F
            print('F  mode==1')
            print('F  mode==1')
            print('F  mode==1')
            print('F  mode==1')
            x_mm, y_mm = calxymm(x_p, y_p, pic_point, j)
            if empty_num ==2:
                sendxy(robx=robB_x, roby=robB_y, R2=0, x=x_mm, y=y_mm, cdx=-cam_disx, cdy=cam_disy,
                       xfix=bxfix, yfix=byfix, h=h_B)
                return 0
            elif empty_num !=1:
                print('F to B put down')
                # modbus  xy reverse
                sendxy(robx=robB_x, roby=robB_y, R2=1, x=x_mm, y=y_mm, cdx=-cam_disx, cdy=cam_disy,
                       xfix=bxfix, yfix=byfix, h=h_B)
                ready_cmd(1,33)
#                    return 1
        elif bbstep=='BgoF':  # B stand by and robot go F
            print('2 B stand by and robot go F')
            # modbus  xy reverse
            master.execute(1, cst.WRITE_MULTIPLE_REGISTERS,  starting_address=0,
                           output_value=[0,1,0,0,0,0,0,0,0,0])
            return 3
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
