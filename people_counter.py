import argparse, datetime
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area")
args = vars(ap.parse_args())
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)

else:
    camera = cv2.Videocapture(args["video"])

firstFrame = None

while True:
    (grabbed, frame) = camera.read()
    text = "Unoccupied"
    b=0
    if not grabbed:
        break

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]


    thresh = cv2.dilate(thresh, None, iterations=2)
    (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            b+=1
            continue


        (x,y,h,w) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        text = "Occupied"


    cv2.putText(frame, "Room Status:"+str(len(cnts)-b), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %b %Y %I:%M:%S%p"), (10,frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1)

    cv2.imshow("security fee", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
        



        
