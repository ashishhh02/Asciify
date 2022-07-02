import cv2
import os

cam = cv2.VideoCapture(r"C:\Users\Ashish Kumar\Desktop\Video to ascii project\yt1s.com - van darkholme intro.mp4")
try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print('Error: Creating directory of data')

current_frame = 0

while(True):
    ret,frame = cam.read()
    
    if ret:
        name = './data/frame' + str(current_frame) + '.jpg'
        print('Creating...' + name)

        #writing the extracted images
        cv2.imwrite(name, frame)

        current_frame += 1
    else:
        break
cam.release()
cv2.destroyAllWindows()
