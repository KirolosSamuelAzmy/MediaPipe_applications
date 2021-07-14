import cv2
import mediapipe

cap=cv2.VideoCapture(0)

medhands=mediapipe.solutions.hands
hands=medhands.Hands(max_num_hands=2,min_detection_confidence=0.7)
draw=mediapipe.solutions.drawing_utils


while True:
    success, img=cap.read()
    img = cv2.flip(img,1)
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    res = hands.process(imgrgb)
    
    lmlist=[]
    tipids=[4,8,12,16,20] #list of all landmarks of the tips of fingers
    
    cv2.rectangle(img,(20,350),(90,440),(0,255,204),cv2.FILLED)
    cv2.rectangle(img,(20,350),(90,440),(0,0,0),5)
    output=''
    if res.multi_hand_landmarks:
        for idx, classification in enumerate(res.multi_handedness):
            label = classification.classification[0].label
            if label == 'Right':
                for handlms in res.multi_hand_landmarks:
                    for id,lm in enumerate(handlms.landmark):
                        h,w,c= img.shape
                        cx,cy=int(lm.x * w) , int(lm.y * h)
                        lmlist.append([id,cx,cy])
                        if len(lmlist) != 0 and len(lmlist)==21:
                            fingerlist=[]
                            if (lmlist[4][2] > lmlist[0][2]) and (lmlist[8][1] > lmlist[6][1]) and (lmlist[16][1] > lmlist[14][1]) and (lmlist[12][1] > lmlist[10][1]) and (lmlist[20][1] > lmlist[18][1])  and (lmlist[4][2] > lmlist[8][2]):
                                output='down'
                            elif (lmlist[4][2] < lmlist[0][2]) and (lmlist[8][1] > lmlist[6][1]) and (lmlist[16][1] > lmlist[14][1]) and (lmlist[12][1] > lmlist[10][1]) and (lmlist[20][1] > lmlist[18][1]) and (lmlist[4][2] < lmlist[9][2]) :
                                output='up'
                            else :         
                            # #thumb and dealing with flipping of hands
                                if lmlist[12][1] > lmlist[20][1]:
                                    if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
                                        fingerlist.append(1)
                                    else:
                                        fingerlist.append(0)
                                else:
                                    if lmlist[tipids[0]][1] < lmlist[tipids[0]-1][1]:
                                        fingerlist.append(1)
                                    else:
                                        fingerlist.append(0)
                    
                            #others
                                for id in range (1,5):
                                    if lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]:
                                        fingerlist.append(1)
                                    else:
                                        fingerlist.append(0)

                            if len(fingerlist)!=0:
                                if sum(fingerlist)==0 and (output !='up' or output !='down'):
                                    output='0'
                                elif sum(fingerlist)==1 and (output !='up' or output !='down'):
                                    output='1'
                                elif sum(fingerlist)==2 and (output !='up' or output !='down'):
                                    output='2'
                                elif sum(fingerlist)==3 and (output !='up' or output !='down'):
                                    output='3'
                                elif sum(fingerlist)==4 and (output !='up' or output !='down'):
                                    output='4'
                                elif sum(fingerlist)==5 and (output !='up' or output !='down'):
                                    output='5'
                                fingercount=fingerlist.count(1)
                    
                            cv2.putText(img,output,(25,430),cv2.FONT_HERSHEY_PLAIN,6,(0,0,0),5)
                    
                        #change color of points and lines
                        draw.draw_landmarks(img,handlms,medhands.HAND_CONNECTIONS,draw.DrawingSpec(color=(0,255,204),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3))

            elif label== 'Left':
                for handlms in res.multi_hand_landmarks:
                    for id,lm in enumerate(handlms.landmark):
                        h,w,c= img.shape
                        cx,cy=int(lm.x * w) , int(lm.y * h)
                        lmlist.append([id,cx,cy])
                        if len(lmlist) != 0 and len(lmlist)==21:
                            fingerlist=[]
                            if (lmlist[4][2] > lmlist[0][2]) and (lmlist[8][1] < lmlist[6][1]) and (lmlist[16][1] < lmlist[14][1]) and (lmlist[12][1] < lmlist[10][1]) and (lmlist[20][1] < lmlist[18][1])  and (lmlist[4][2] > lmlist[8][2]):
                                output='down'
                            elif (lmlist[4][2] < lmlist[0][2]) and (lmlist[8][1] < lmlist[6][1]) and (lmlist[16][1] < lmlist[14][1]) and (lmlist[12][1] < lmlist[10][1]) and (lmlist[20][1] < lmlist[18][1]) and (lmlist[4][2] < lmlist[9][2]):
                                output='up'
                            else :         
                            # #thumb and dealing with flipping of hands
                                if lmlist[12][1] > lmlist[20][1]:
                                    if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
                                        fingerlist.append(1)
                                    else:
                                        fingerlist.append(0)
                                else:
                                    if lmlist[tipids[0]][1] < lmlist[tipids[0]-1][1]:
                                        fingerlist.append(1)
                                    else:
                                        fingerlist.append(0)
                    
                            #others
                                for id in range (1,5):
                                    if lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]:
                                        fingerlist.append(1)
                                    else:
                                        fingerlist.append(0)

                            if len(fingerlist)!=0 and (output !='up' or output !='down'):
                                if sum(fingerlist)==0 :
                                    output='0'
                                elif sum(fingerlist)==1 :
                                    output='1'
                                elif sum(fingerlist)==2 :
                                    output='2'
                                elif sum(fingerlist)==3 :
                                    output='3'
                                elif sum(fingerlist)==4 :
                                    output='4'
                                elif sum(fingerlist)==5 :
                                    output='5'
                                fingercount=fingerlist.count(1)
                    
                            cv2.putText(img,output,(25,430),cv2.FONT_HERSHEY_PLAIN,6,(0,0,0),5)
                    
                        #change color of points and lines
                        draw.draw_landmarks(img,handlms,medhands.HAND_CONNECTIONS,draw.DrawingSpec(color=(0,255,204),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3))
                    

             
    cv2.imshow("hand gestures",img)
    #press q to quit
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()