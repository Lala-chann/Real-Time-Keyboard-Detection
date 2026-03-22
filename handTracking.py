#TODO(1): import mediapipe , opencv, mediapipe handmark,mediapip for python, vision, keyboard, app_launch file and time

from mediapipe.tasks import python
from mediapipe.tasks. python import vision
from keyboardModel import draw_keyboard
from app_launcher import launch_apps
import mediapipe as mp
import cv2
import time






#TODO(15): Calculate FPS - fps stand for FRAME PER SECOND, which measures how many images(franes) a camera or video system processes in one second
def calculate_fps(ptime):
    cTime = time.time()
    fps = 1 / (cTime - ptime) if (cTime - ptime) > 0 else 0
    return fps, cTime




#TODO(20): Start to draw circle and detect the hand index with draw_line function
def draw_line(img, hand):

    #TODO(21): It is seriously hard to explain. It is for initialize the finger coordinates with -1 to indicate that no finger has been detected yet.
    finger_x , finger_y = -1, -1

    #TODO(22): Start to draw circle for finger's indexes
    h, w, _ = img.shape
    points = [(int(lm.x * w), int(lm.y * h)) for lm in hand]
    for x , y in points:
        cv2.circle(img,(x,y),7,(173,216,230), -1)


    #TODO(23): Show 21 handmarks and check out for each index for landmarks and draw line for connecting
    connections = [
        (0,1),(1,2),(2,3),(3,4),
        (0,5),(5,6),(6,7),(7,8),
        (9,10),(10,11),(11,12),
        (5,9),(9,13),(13,17), # to connect to palm indices
        (13,14),(14,15),(15,16),
        (0,17),(17,18),(18,19),(19,20)
    ]
    for start , end in connections:
        cv2.line(img,points[start],points[end],(0,255,255),2)


    #TODO(24): after connections within all the line, return the coordinates of the index fingertip (index = 8)
    for idd, lm in enumerate(hand):
        h,w,c = img.shape
        x,y = int(lm.x * w), int(lm.y * h)
        print(idd, x, y)
        if idd == 8:
            cv2.circle(img,(x,y),7,(0,0,0),-1)
            finger_x ,finger_y = x,y

    return finger_x, finger_y









#TODO(2): access the webcam with OpenCV and Reset the camera size
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 730)






#TODO(3): load model option and create detector. We are not able to use solution method anymore, that's because it is old version of Mediapipe API
base_options = python.BaseOptions(model_asset_path = "hand_landmarker.task")
options = vision.HandLandmarkerOptions(base_options = base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)



#TODO(4) part 1: Equal ptime variable to 0 and start to calculate fps
#TODO(5) part 2: String where all the letters you "type" with your finger will be collected. It should starts empty and grows as you pres keys
#TODO(6) part 3: Keeps track of the last key that was pressed. This helps prevent repeating the same letter many times if your finger stays on one key
#TODO(7) part 4: Stores the time when the last key was pressed. Together with cooldown, it ensures you do not type the same letter multiple times too quicly
#TODO(8) part 5: A delay between key presses, for example if cooldown = 1.0 you must wait at least one second before the same key can be typed again
#TODO(9) part 6: Text message then the given apps is launching
ptime = 0
typed_text = ""
last_typed_letter = 0
last_typed_time = 0
cooldown = 1.0
status_msg = ""








#TODO(10): Creating continues loop for tracking our hand and opening the webcam
while True:

    #TODO(11): we have to read te given image or the camera
    success, img = cap.read()



    #TODO(12): OpenCv are not able to read BGR color, so next step should be switching into BGR to RGB. That is because OpenCv or other lib might confuse the colors
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data = imgRGB)
    result = detector.detect(mp_img)






    #TODO(14): return calculate_fps and use cv2.putText functon to put text on the screen
    fps , ptime = calculate_fps(ptime)
    cv2.putText(img,str(int(fps)),(10,200),cv2.FONT_HERSHEY_COMPLEX,2, (211,211,211),6)




    #TODO(25): Call the draw_keyboard function which the draws the keyboard on the screen and returns two values with three parameters: img, text in bar, status message
    img , key_positions = draw_keyboard(img, typed_text, status_msg)


    #TODO(18): Track your hand with 5-pixel red circle
    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            #TODO(19): add figer_x,finger_y to detect your finger's coordinates (index = 8)
            #finger_x ve finger_y bize neye gore lazimdir deye fikirlessek, barmagimizin herketini hesabalayir, hjara getdiyini neyi detect etdiyini ve s
            finger_x, finger_y = draw_line(img,hand)

            #TODO(26):
            for letter, (kx,ky,kw,kh) in key_positions.items():
                if kx < finger_x < kx + kw and ky < finger_y < ky + kh:
                    current_time = time.time()
                    if letter != last_typed_letter:
                        last_typed_letter = letter
                        last_typed_time = current_time
                    elif current_time - last_typed_time > cooldown:
                        last_typed_time = current_time
                        last_typed_letter = ""

                        #TODO(27):Launching the apps if the user press enter or removing string the user press back
                        if letter == "ENTER":
                            status_msg = launch_apps(typed_text)
                            typed_text = ""
                        elif letter == "BACK":
                            typed_text = typed_text[:-1]
                        else:
                            typed_text += letter




    #TODO(16): Show the camera with given name
    cv2.imshow("CAMERA", img)



    #TODO(17): Close the webcam when you press 'q' button
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break