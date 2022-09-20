import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import random


cap=cv2.VideoCapture(0)
cap.set(3,300)  #width
cap.set(4,300)  #height
# crop the cap from the middle to focus on the hand

detector = HandDetector(maxHands=2 ) # by default confidence value is 0.5

scores = [0,0] # [ai_score, player_score]
timer = 0
stateResult = False #initial state
startGame = False #flag (if it is true then only check the conditions will be checked)


while True:
    imgBG = cv2.imread('resources/BGimg.png')
    info = cv2.imread('resources/info.png')
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.48, 0.55)

    # find hands
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:

            timer = time.time() - initialTime
            cv2.putText(imgBG,str(int(timer)),(300,176),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)

            randomNumber = random.randint(1, 8)

            if timer > 3:
                stateResult = True
                timer = 0
                playerMove = None

                if hands:
                    hand = hands[0]  # main hand
                    fingers = detector.fingersUp(hand)  # returns an array of 1s and 0s (1 means finger is up and 0 means finger is down)


                if fingers == [0, 1, 0, 0, 0]:
                    playerMove = 1
                if fingers == [0, 1, 1, 0, 0]:
                    playerMove = 2
                if fingers == [0, 1, 1, 1, 0]:
                    playerMove = 3
                if fingers == [0, 1, 1, 1, 1]:
                    playerMove = 4
                if fingers == [1, 1, 1, 1, 1]:
                    playerMove = 5
                if fingers == [1, 0, 0, 0, 0]:
                    playerMove = 6
                if fingers == [1, 0, 0, 0, 1]:
                    playerMove = 7
                if fingers == [0, 1, 0, 0, 1]:
                    playerMove = 8

                cv2.putText(imgBG, str(playerMove), (100, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)


                imgAI = cv2.imread(f'resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                #overlay this image on to the BG image
                imgBG[111:269, 382:551] = imgScaled  # mask down the imgScaled on the imgBG

                AIMove = randomNumber

                # we have playerMove and AIMove
                # if the sum of both is even, then increase the score of player

                sum = AIMove + playerMove
                if sum%2 == 0:
                    # player wins
                    scores[1]+=1
                    cv2.putText(imgBG,"EVEN",(300,220),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),2)
                if sum%2 != 0:
                    # AI wins
                    scores[0]+=1
                    cv2.putText(imgBG, "ODD", (300, 220), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)





    imgBG[114:272 , 385:554] = imgScaled  #mask down the imgScaled on the imgBG
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (118,135))

        cv2.putText(imgBG, str(scores[0]), (158, 303), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
        cv2.putText(imgBG, str(scores[1]), (450, 303), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)



    cv2.imshow("imgBG", imgBG)

    cv2.imshow("info", info)


    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
