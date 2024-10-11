import cv2
import math
from cvzone.HandTrackingModule import HandDetector
from pyfirmata import Arduino

# Initialize HandDetector for both hands
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Initialize video capture
video = cv2.VideoCapture(2)

# Setup the Arduino board
board = Arduino('/dev/ttyACM0')  # Replace with your port, e.g., 'COM3' on Windows

# Define pins for the four servos
left_thumb_x_pin = board.get_pin('d:9:s')   # Left thumb X-axis servo
left_thumb_y_pin = board.get_pin('d:10:s')  # Left thumb Y-axis servo
right_thumb_x_pin = board.get_pin('d:11:s') # Right thumb X-axis servo
right_thumb_y_pin = board.get_pin('d:12:s') # Right thumb Y-axis servo

# Define square properties
square_size = 200  # Length of one side of the square
left_square_top_left = (350, 200)
right_square_top_left = (100, 200)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)

    # Draw squares on the frame
    cv2.rectangle(frame, left_square_top_left, 
                  (left_square_top_left[0] + square_size, left_square_top_left[1] + square_size), 
                  (0, 255, 0), 2)
    
    cv2.rectangle(frame, right_square_top_left, 
                  (right_square_top_left[0] + square_size, right_square_top_left[1] + square_size), 
                  (0, 255, 0), 2)

    # Initialize servo angles
    left_servo_x_angle = 90
    left_servo_y_angle = 90
    right_servo_x_angle = 90
    right_servo_y_angle = 90

    # Detect hands in the frame
    hands, img = detector.findHands(frame)

    if hands:
        for hand in hands:
            lmList = hand['lmList']  # Landmark list of the hand
            thumb_tip_pos = lmList[4][:2]  # Get the (x, y) position of the thumb tip

            print(f'Thumb Tip Position: {thumb_tip_pos}')  # Debugging statement

            # Check if left hand
            if hand['type'] == "Left":
                # Check if the thumb tip is inside the left square
                if (left_square_top_left[0] <= thumb_tip_pos[0] <= left_square_top_left[0] + square_size and
                        left_square_top_left[1] <= thumb_tip_pos[1] <= left_square_top_left[1] + square_size):
                    
                    # Calculate coordinates relative to square's top-left corner
                    x = thumb_tip_pos[0] - left_square_top_left[0]
                    y = thumb_tip_pos[1] - left_square_top_left[1]

                    # Debugging statement to check x, y values
                    print(f'Left Thumb X: {x}, Y: {y}') 

                    # Map coordinates to servo angles
                    left_servo_x_angle = int((x / square_size) * 180)  # Map X to 0-180
                    left_servo_y_angle = int((y / square_size) * 180)  # Map Y to 0-180

                    # Control left thumb servos
                    left_thumb_x_pin.write(left_servo_x_angle)
                    left_thumb_y_pin.write(left_servo_y_angle)

            # Check if right hand
            elif hand['type'] == "Right":
                # Check if the thumb tip is inside the right square
                if (right_square_top_left[0] <= thumb_tip_pos[0] <= right_square_top_left[0] + square_size and
                        right_square_top_left[1] <= thumb_tip_pos[1] <= right_square_top_left[1] + square_size):

                    # Calculate coordinates relative to square's top-left corner
                    x = thumb_tip_pos[0] - right_square_top_left[0]
                    y = thumb_tip_pos[1] - right_square_top_left[1]

                    # Debugging statement to check x, y values
                    print(f'Right Thumb X: {x}, Y: {y}') 

                    # Map coordinates to servo angles
                    right_servo_x_angle = int((x / square_size) * 180)  # Map X to 0-180
                    right_servo_y_angle = int((y / square_size) * 180)  # Map Y to 0-180

                    # Control right thumb servos
                    right_thumb_x_pin.write(right_servo_x_angle)
                    right_thumb_y_pin.write(right_servo_y_angle)

    # Print servo angles above the squares
    cv2.putText(frame, f'Left X: {left_servo_x_angle}', (left_square_top_left[0], left_square_top_left[1] - 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f'Left Y: {left_servo_y_angle}', (left_square_top_left[0], left_square_top_left[1] - 5),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(frame, f'Right X: {right_servo_x_angle}', (right_square_top_left[0], right_square_top_left[1] - 20),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f'Right Y: {right_servo_y_angle}', (right_square_top_left[0], right_square_top_left[1] - 5),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("frame", frame)

    # Exit on pressing 'k'
    k = cv2.waitKey(1)
    if k == ord("k"):
        break

video.release()
cv2.destroyAllWindows()
