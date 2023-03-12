import cv2
import numpy as np
import HandTrackingModule as htm


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector()

drawingColor = (0,0,255)
imgCanvas = np.zeros((720,1280,3),np.uint8)

eraserSize = 50
brushSize = 15

while True:

    #1.preprocess screen
    sucess,image = cap.read()
    
    image = cv2.flip(image,1)
    cv2.rectangle(image,(0,0),(1280,110),(0,0,0),cv2.FILLED)
    cv2.rectangle(image,(10,10),(230,100),(0,0,255),cv2.FILLED)
    cv2.rectangle(image,(250,10),(470,100),(0,255,0),cv2.FILLED)
    cv2.rectangle(image,(490,10),(710,100),(255,0,0),cv2.FILLED)
    cv2.rectangle(image,(730,10),(950,100),(0,255,255),cv2.FILLED)
    cv2.rectangle(image,(970,10),(1270,100),(255,255,255),cv2.FILLED)
    cv2.putText(image,'Eraser',(1080,65),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)

#2.find  hand landmarks

    image = detector.findHands(image)
    lmlist = detector.findPosition(image)



#[8, 763, 402]
#[12, 813, 452]


    # print(lmlist)



    if len(lmlist)!=0:


        x1,y1 = lmlist[8][1:] #finger 1
        x2,y2 = lmlist[12][1:] # finger 2


        # print(x2,y2)

#3.check which finger is up
    fingers = detector.fingersUp()
    # print(fingers)


#4.selection mode - two finger is up
    if fingers[1] and fingers[2]:   

        xp,yp = 0,0
        # print('selection mode')

        if y1<120:

            if 10<x1<230:

                drawingColor = (0,0,255)
                # print('red selected')
                
            elif 250<x1<470:

                drawingColor = (0,255,0)
                # print('green selected')

            elif 490<x1<710:

                drawingColor = (255,0,0)
                # print('blue selected')

            elif 730<x1<950:
                drawingColor = (0,255,255)

                # print('yellow selected')

            elif 970<x1<1270:
                drawingColor = (0,0,0)

                # print('eraser')
            
        cv2.rectangle(image,(x1,y1),(x2,y2),drawingColor,cv2.FILLED)

#5. drawing mode - one finger is up

    if (fingers[1] and not fingers[2]):

        cv2.circle(image,(x1,y1),15,drawingColor,thickness=-1)
        print('drawing mode')

        if xp == 0 and yp == 0:
            xp = x1
            yp = y1

        if drawingColor ==( 0,0,0):
            cv2.line(image,(xp,yp),(x1,y1),drawingColor,eraserSize)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawingColor,eraserSize)

        else:
            cv2.line(image,(xp,yp),(x1,y1),drawingColor,brushSize)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawingColor,brushSize)


        xp , yp = x1 , y1

    imgGray = cv2.cvtColor (imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,20,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    image = cv2.bitwise_and(image,imgInv)
    image  = cv2.bitwise_or(image,imgCanvas)


    image = cv2.addWeighted(image,1,imgCanvas,0.5,0)



    cv2.imshow('virtual painter',image)
    if cv2.waitKey(1) & 0xFF ==27:
        break