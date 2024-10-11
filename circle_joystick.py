# written by vikash singh thakur
# u are freeee...    to use it whatever way u want it to
# date 11/10/24

# I LOVE ROBOTICS..........

# NOTE : written in hindi and english formate  

import cv2                                            #yaha sare libraries included hai
import math
from cvzone.HandTrackingModule import HandDetector
from pyfirmata import Arduino

 
detector = HandDetector(detectionCon=0.8, maxHands=2)  ## maine yaha thresold apne according set kiya hai aap apne accoding change kr sakte ho

 
video = cv2.VideoCapture(2)  # camera acces ke liye aap ise change kr sakte ho 0 1 or 2 me se kisi ek me app try kr ke dekh sakte ho

 
board = Arduino('/dev/ttyACM0')   # ye port system ke according vari kr sakta hai to pleses check kr le ki aapka arduino kis com port se connected hai

 
left_thumb_x_pin = board.get_pin('d:9:s')    # ye pins hai jinse arduino cnneted hai apke servo motors se  9 10 11 and 12 wale
left_thumb_y_pin = board.get_pin('d:10:s')   
right_thumb_x_pin = board.get_pin('d:11:s')  
right_thumb_y_pin = board.get_pin('d:12:s')  

 
square_size = 200                     # ye bhi aapke camera ke accordding vary kr sakta hai to plase check kr ke aap apne according use kr lewe
left_square_top_left = (350, 200)
right_square_top_left = (100, 200)

while True:
    ret, frame = video.read()    # yaha aaap frame set kr sakte ho
    frame = cv2.flip(frame, 1)

    
    cv2.rectangle(frame, left_square_top_left, 
                  (left_square_top_left[0] + square_size, left_square_top_left[1] + square_size), 
                  (0, 255, 0), 2)
    
    cv2.rectangle(frame, right_square_top_left, 
                  (right_square_top_left[0] + square_size, right_square_top_left[1] + square_size), 
                  (0, 255, 0), 2)

   
    left_servo_x_angle = 90  # initial angles ke liye maine 90 as a defoult angle se t kiya hai isme 
    left_servo_y_angle = 90
    right_servo_x_angle = 90
    right_servo_y_angle = 90

     
    hands, img = detector.findHands(frame)

    if hands:
        for hand in hands:
            lmList = hand['lmList']  # ye land mark ka list hai 
            thumb_tip_pos = lmList[4][:2]  # yaha se hume thumb ka position milta hai screen ke according in x and y

            print(f'Thumb Tip Position: {thumb_tip_pos}')  # Debugging ke liye maine ise add kiya hai 

            # yaha hum left hand ki availibility check karenge 
            if hand['type'] == "Left":
                # yaha gar jo hamara tip hai thumb ka wo agar square ke under aa rha hai to ye response krega 
                if (left_square_top_left[0] <= thumb_tip_pos[0] <= left_square_top_left[0] + square_size and
                        left_square_top_left[1] <= thumb_tip_pos[1] <= left_square_top_left[1] + square_size):
                    
                    # isme hum left thumb ka coordinate calculate 
                    x = thumb_tip_pos[0] - left_square_top_left[0]
                    y = thumb_tip_pos[1] - left_square_top_left[1]

                    # Debugging 
                    print(f'Left Thumb X: {x}, Y: {y}') 

                    # Map coordinates to servo angles
                    left_servo_x_angle = int((x / square_size) * 180)  # Map X to 0-180
                    left_servo_y_angle = int((y / square_size) * 180)  # Map Y to 0-180

                    # Control left thumb servos
                    left_thumb_x_pin.write(left_servo_x_angle)
                    left_thumb_y_pin.write(left_servo_y_angle)

            # Check karega agr right hand hoga to yaha se 
            elif hand['type'] == "Right":
                # yaha dekhenge ki jo right hand ka thumb ander hai ya nahi 
                if (right_square_top_left[0] <= thumb_tip_pos[0] <= right_square_top_left[0] + square_size and
                        right_square_top_left[1] <= thumb_tip_pos[1] <= right_square_top_left[1] + square_size):

                    # relative coordinate calcute krenge taki hum servo ke liye mapping value find kr sake
                    x = thumb_tip_pos[0] - right_square_top_left[0]
                    y = thumb_tip_pos[1] - right_square_top_left[1]

                    
                    print(f'Right Thumb X: {x}, Y: {y}') 

                    # Map karenge coordinates of thumb for the servo angle motion 
                    right_servo_x_angle = int((x / square_size) * 180)  # Map X to 0-180
                    right_servo_y_angle = int((y / square_size) * 180)  # Map Y to 0-180

                    # Control krna hai right thumb servo ko 
                    right_thumb_x_pin.write(right_servo_x_angle)
                    right_thumb_y_pin.write(right_servo_y_angle)

    # Print karenge yaha pe servo angles ko 
    cv2.putText(frame, f'Left X: {left_servo_x_angle}', (left_square_top_left[0], left_square_top_left[1] - 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f'Left Y: {left_servo_y_angle}', (left_square_top_left[0], left_square_top_left[1] - 5),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(frame, f'Right X: {right_servo_x_angle}', (right_square_top_left[0], right_square_top_left[1] - 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f'Right Y: {right_servo_y_angle}', (right_square_top_left[0], right_square_top_left[1] - 5),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("frame", frame)

    # bahar nikle ke liye press 'k'
    k = cv2.waitKey(1)
    if k == ord("k"):
        break

video.release()
cv2.destroyAllWindows()
