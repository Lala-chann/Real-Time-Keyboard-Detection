#TODO(1): Import Opencv
import cv2


#TODO(2): Start to call draw_keyboard function with three parameters: img, typed text and status message
def draw_keyboard(img, typed_text = "", status_msg = ""):
    #TODO(3): write down all letter you need for your virtual keyboard
    rows = [
        ["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M","Enter", "BACK"]
    ]

    #TODO(4): We need to make clarify button's width and height for each letter
    key_width = 50
    key_height = 50
    spacing = 8

    #TODO(5): You need to calculate where you want to put the letters
    h,w,_ = img.shape
    total_keyboard = 10 * (key_width + spacing)
    start_x = ( w - total_keyboard) // 2
    start_y = 200

    #TODO(6): Initialize bar koordinates and use cv2.putText for showing the typen strings
    bar_x = start_x
    bar_y = 120
    bar_w = total_keyboard
    bar_h = 50

    #TODO(7): Remember that cv2.rectangle does not support transparent color. So we need to use alpha and cv2.addWeighted
    overlay = img.copy()
    cv2.rectangle(overlay, (bar_x,bar_y), (bar_x + bar_w, bar_y + bar_h), (135,206,235),-1)
    alpha = 0.4
    cv2.addWeighted(overlay,alpha,img, 1- alpha, 0,img)
    cv2.rectangle(img,(bar_x,bar_y),(bar_x + bar_w, bar_y + bar_h),(218,218,218),2)

    #TODO(8): After typing we need to sgow the string we typed and we need to send status message. Hints: use .putText
    cv2.putText(img,typed_text,(bar_x + 8,bar_y + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (218,218,218),2)
    cv2.putText(img,status_msg,(start_x + 90, start_y + 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)


    #TODO(9): Start to draw keyboard keys. Hints: for saving key positions we need dictionary to return
    key_positions = {}
    for row_index, row in enumerate(rows):
        for col_index, letter in enumerate(row):
            #TODO(10): Beside normal letter, we need to calculate differently Enter and Back button. Hints: enter and Back is bitter than normal letter
            if letter == "Enter":
                x = start_x + col_index * (key_width + spacing)
                y = start_y + row_index * (key_height + spacing)
                w_key = key_width * 2

                #TODO(11): Add transparent color to rectangle and put text like ENTER. Hints: Save key position
                overlay = img.copy()
                cv2.rectangle(overlay,(x,y),(x + w_key, y + key_height),(0,255,0),-1)
                cv2.addWeighted(overlay,alpha,img,1-alpha,0,img)
                cv2.rectangle(img,(x,y),(x + w_key, y + key_height), (218,218,218),2)
                cv2.putText(img,"ENTER",(x,y + 35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

                key_positions["ENTER"] = (x,y,key_width * 2, key_height)

                continue

            if letter == "BACK":
                x = start_x + col_index * (key_width + spacing) + key_width
                y = start_y + row_index * (key_height + spacing)
                w_key = key_width * 2

                #TODO(12): Same code source with todo11
                overlay = img.copy()
                cv2.rectangle(overlay,(x,y), (x + w_key, y + key_height), (0,255,0),-1)
                cv2.addWeighted(overlay,alpha,img,1-alpha, 0 ,img)
                cv2.rectangle(img,(x,y), (x + w_key, y + key_height), (218,218,218),2)
                cv2.putText(img,"BACK",(x + 10, y + 35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

                key_positions["BACK"] = (x,y,key_width * 2, key_height)
                continue


            #TODO(13): Organize normal letter and use same method as todo12 and do not forget to save key position
            x = start_x + col_index * (key_width + spacing)
            y = start_y + row_index * (key_height + spacing)

            overlay = img.copy()
            cv2.rectangle(overlay,(x,y), (x + key_width, y + key_height), (135,206,235),-1)
            cv2.addWeighted(overlay,alpha,img,1-alpha, 0,img)
            cv2.rectangle(img,(x,y),(x + key_width, y + key_height), (218,218,218),2)
            cv2.putText(img,letter,(x + 15, y+ 35), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

            key_positions[letter] = (x, y, key_width, key_height)


    #TODO(14): return 2 important arguments
    return img, key_positions
