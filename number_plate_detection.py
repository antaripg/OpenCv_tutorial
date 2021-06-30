# Detecting Number Plates
import cv2
import os
import time
from datetime import datetime

# Scanned directory creation


def createDirectory():
    '''Creating the Directory to store the scans'''
    imgDir = 'scanned_images/NumberPlates/'
    flag = 'success'
    dirPath = os.path.dirname(os.path.realpath(__file__))
    try:
        os.mkdir(os.path.join(dirPath, imgDir))
    except OSError as e:
        flag = e
        print(e)
    return flag, imgDir

# extracting the Cascade Model


def haarModel():
    '''Defining the Haar Model'''
    haarModelPath = 'data/haarcascade_licence_plate_rus_16stages.xml'
    cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
    haar_model = os.path.join(cv2_base_dir, haarModelPath)
    nPlateCascade = cv2.CascadeClassifier(haar_model)
    return nPlateCascade


# Main Function


def main():
    '''Main Function'''
    frameWidth, frameHeight, brightness = 640, 480, 100
    minArea = 500
    thickness = 2
    color = (255, 0, 0)
    font = cv2.FONT_ITALIC
    fontSize = 0.5
    model = haarModel()
    _, nameDir = createDirectory()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, brightness)

    while (cap.isOpened()):
        _, frame = cap.read()
        imgResize = cv2.resize(frame, (frameWidth, frameHeight))
        imgGray = cv2.cvtColor(imgResize, cv2.COLOR_BGR2GRAY)
        numberPlates = model.detectMultiScale(imgGray, 1.1, 4)
        # bounding Boxes
        for num, (x, y, w, h) in enumerate(numberPlates):
            area = w*h
            if area > minArea:
                cv2.rectangle(imgResize, (x, y), (x+w, y+h), color, 2)
                cv2.putText(imgResize, "Number Plate", (x-10, y-10),
                            font, fontSize, color, thickness)
                # get number plate image
                imgRoi = imgResize[y:y+h, x:x+w]
                cv2.imshow('NumberPlate', imgRoi)
        cv2.imshow("Result", imgResize)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            try:
                time.sleep(1)
                timeNow = datetime.now()
                timeNow_str = timeNow.strftime("%d-%m_%Y_%H_%M_%S")
                savePath = nameDir+'image_{}.jpg'.format(timeNow_str)
                cv2.imwrite(savePath, imgRoi)
                cv2.rectangle(imgResize, (0, 200), (640, 300), (0, 255, 0),
                              cv2.FILLED)
                cv2.putText(imgResize, "Successfully Scanned", (150, 300),
                            cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 2)
                cv2.imshow("Result", imgResize)
                cv2.waitKey(500)
            except Exception as e:
                print(e)
        elif cv2.waitKey(1) & 0xFF == ord('x'):
            # print("nothing Scanned")
            # cv2.rectangle(imgResize, (0, 200), (640, 300), (0, 255, 0),
            #               cv2.FILLED)
            # cv2.putText(imgResize, "Nothing Scanned", (150, 300),
            #             cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 2)
            # cv2.imshow("Result", imgResize)
            # cv2.waitKey(1)
            break
    # releasing the capture
    cap.release()
    # out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
