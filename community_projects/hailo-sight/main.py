from detect_signal import detect_signal
import time
from picamera import PiCamera

def main():
    print("Running Hailo sight")
    camera = PiCamera()

    # Set the desired resolution (optional)
    camera.resolution = (640, 480)

    try:
        while True:  # Take 10 pictures
            camera.capture(f'image_{i}.jpg')  # Save the image
            print(f'Captured image_{i}.jpg')
            time.sleep(3)  # Wait for 3 seconds
    finally:
        camera.close()  







if __name__ == "__main__":
    main()