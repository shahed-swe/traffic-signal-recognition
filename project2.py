import numpy as np  # Import the NumPy library for numerical operations
import cv2  # Import the OpenCV library for computer vision
import pickle  # Import the pickle module for reading and writing Python objects as binary data

# for serial port
import serial  # Import the serial module for communication with serial devices
import time  # Import the time module for time-related functions

# Set some initial parameters
frameWidth = 640  # Define the width of the camera frame
frameHeight = 480  # Define the height of the camera frame
brightness = 180  # Set the camera brightness
threshold = 0.90  # Set a probability threshold for object detection
font = cv2.FONT_HERSHEY_SIMPLEX  # Set the font for text in the video feed

# Initialize communication with an Arduino device on COM3 port at a baud rate of 115200
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)

# Set up the video camera
cap = cv2.VideoCapture(0)  # Initialize the video capture using the default camera (index 0)
cap.set(3, frameWidth)  # Set the camera frame width
cap.set(4, frameHeight)  # Set the camera frame height
cap.set(10, brightness)  # Set the camera brightness

# Load a trained machine learning model from a file
pickle_in = open("model_trained.p", "rb")  # Open the model file in binary read mode
model = pickle.load(pickle_in)  # Load the model from the file

# Define image processing functions
def grayscale(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
    return img

def equalize(img):
    img = cv2.equalizeHist(img)  # Perform histogram equalization on the image
    return img

def preprocessing(img):
    img = grayscale(img)  # Convert the image to grayscale
    img = equalize(img)  # Perform histogram equalization
    img = img / 255  # Normalize the pixel values to a range of [0, 1]
    return img

# Define a function to map class numbers to human-readable class names
def getClassName(classNo):
    if classNo == 0:
        return '20'
    elif classNo == 1:
        return '30'
    elif classNo == 2:
        return '50'
    elif classNo == 3:
        return '60'
    elif classNo == 4:
        return '70'
    elif classNo == 5:
        return '80'
    elif classNo == 6:
        return '90'
    elif classNo == 7:
        return '100'
    elif classNo == 8:
        return '120'

# Function to send a signal to the Arduino
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))  # Send a message to the Arduino as bytes
    time.sleep(0.05)  # Wait for a short time for a response (not used in this code)

# Main loop for real-time object detection
while True:
    # Read an image frame from the camera
    success, imgOrignal = cap.read()

    # Process the image
    img = np.asarray(imgOrignal)
    img = cv2.resize(img, (32, 32))  # Resize the image to 32x32 pixels
    img = preprocessing(img)  # Apply grayscale, equalization, and normalization
    cv2.imshow("Processed Image", img)

    img = img.reshape(1, 32, 32, 1)  # Reshape the image for model prediction

    cv2.putText(imgOrignal, "CLASS: ", (20, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(imgOrignal, "PROBABILITY: ", (20, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

    # Predict the class of the image
    predictions = model.predict(img)
    classIndex = np.argmax(predictions, axis=-1)[0]
    probabilityValue = np.amax(predictions)

    if probabilityValue > threshold:
        cv2.putText(imgOrignal, str(classIndex) + " " + str(getClassName(classIndex)), (120, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(imgOrignal, str(round(probabilityValue * 100, 2)) + "%", (180, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

        write_read(getClassName(classIndex))  # Send the detected class to the Arduino

    cv2.imshow("Result", imgOrignal)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all OpenCV windows
