# import cv2
# import socketio
# import base64
# import time

# def send_video_frame(frame):
#     # Serialize the frame to send it over the socket
#     sio = socketio.Client()
#     _, frame_buffer = cv2.imencode('.jpg', frame)
#     sio.emit('video_frame', frame_buffer)

# def main2():
#     sio = socketio.Client()

#     @sio.event
#     def connect():
#         print("Connected to server")

#     @sio.event
#     def disconnect():
#         print("Disconnected from server")

#     try:
#         video_path = "/Users/ahmedsaud/Documents/FYP/recordingswithdaydate/Day1/ReceptionViewFrontDeskch14/Ch14 20240311101200.mp4"
#         sio.connect('http://localhost:3000')

#         cap = cv2.VideoCapture(video_path)
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             _, buffer = cv2.imencode('.jpg', frame)
#             jpg_as_text = base64.b64encode(buffer).decode('utf-8')
#             sio.emit('video_frame', jpg_as_text)
#             send_video_frame(frame)
#             time.sleep(1/30)  # Adjust frame rate as necessary

#         cap.release()
#         sio.disconnect()

#     except Exception as e:
#         print(f"Error: {e}")
#         sio.disconnect()

# if __name__ == "__main__":
#     main2()
import socketio
import cv2
import base64
import numpy as np

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print('Connection established')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def video_frame(data):
    print('Received video frame')
    try:
        # Debugging: Print the size of the data received
        print(f'Size of received data: {len(data)}')
        
        # Deserialize the received frame
        np_data = np.frombuffer(base64.b64decode(data), np.uint8)
        
        # Debugging: Check the shape of np_data before decoding
        print(f'Shape of np_data: {np_data.shape}')
        
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        
        if frame is None:
            print('Error: Frame is None after imdecode')
        else:
            cv2.imshow('Received Video Frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sio.disconnect()
    except Exception as e:
        print(f'Error in video_frame handler: {e}')

def send_video_frame(frame):
    try:
        # Serialize the frame to send it over the socket
        _, buffer = cv2.imencode('.jpg', frame)
        
        # Debugging: Print the size of the buffer
        print(f'Size of buffer: {buffer.size}')
        
        frame_data = base64.b64encode(buffer).decode('utf-8')
        sio.emit('video_frame', frame_data)
    except Exception as e:
        print(f'Error in send_video_frame: {e}')

# Connect to the server
sio.connect('http://localhost:3000')

# Capture video from webcam and send frames to the server
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    send_video_frame(frame)

cap.release()
cv2.destroyAllWindows()
sio.disconnect()
