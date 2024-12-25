from detect_signal import detect_signal
import time
from picamera import PiCamera

def main():
    print("Running Hailo sight")
    camera = PiCamera()

    # Set the desired resolution (optional)
    camera.resolution = (640, 480)

    try:
        while True:
            camera.capture(f'image_.jpg')  # Save the image
            if detect_signal('image_.jpg'):
                print(f'Detected a hand in image.jpg')
            else:
                print(f'No hand detected in image.jpg')
            print(f'Captured image.jpg')
            time.sleep(3)  # Wait for 3 seconds
    finally:
        camera.close()  







if __name__ == "__main__":
    main()