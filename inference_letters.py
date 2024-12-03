from kivy.core.window import Window
from kivy.config import Config
# Set the window size for phone resolution
Config.set('graphics', 'width', '380')
Config.set('graphics', 'height', '640')
# Ensure these settings are applied
Window.size = (380, 640)
import os
import pickle
import cv2
import mediapipe as mp
import numpy as np
import threading
import warnings
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

# Suppress the specific deprecation warning from Google Protobuf
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf.symbol_database')

# Disable TensorFlow's oneDNN optimizations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load the trained model
model_dict = pickle.load(open('./model_2.p', 'rb'))
model = model_dict['model_2']

# Set up MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3)

# Extended label dictionary for predictions
labels_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E',
    5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
    15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
    20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
}

class HandSignDetector(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Image widget for displaying camera feed
        self.image_widget = Image(size_hint=(1, 0.9), pos_hint={'top': 1})
        self.add_widget(self.image_widget)

        # Create the prediction label (Top)
        self.prediction_label = Label(
            text="Detecting...", 
            size_hint=(None, None), 
            size=(0.8 * 380, 0.1 * 640),  # 80% width, 10% height of the screen
            pos_hint={'x': 0.2, 'y': 0.85},  # Positioning near the top (y=0.85 for 85% from bottom)
            halign='center',  # Center text horizontally
            valign='middle'   # Center text vertically
        )
        self.prediction_label.color = (0.678, 0.847, 0.902, 1)
        self.prediction_label.font_size = '20sp'  # Adjust font size for better visibility
        self.add_widget(self.prediction_label)

        # Create the history label (Bottom)
        self.history_label = Label(
            text="Self History: None", 
            size_hint=(None, None), 
            size=(0.8 * 380, 0.1 * 640),  # 80% width, 10% height of the screen
            pos_hint={'x': 0.2, 'y': 0.15},  # Positioning near the bottom (y=0.05 for 5% from bottom)
            halign='center',  # Center text horizontally
            valign='middle'   # Center text vertically
        )
        self.history_label.color = (0.678, 1, 0.184, 1)
        self.history_label.font_size = '13sp'  # Adjust font size for better visibility
        self.add_widget(self.history_label)

        # List to store predictions during runtime
        self.gesture_history = []

        # Open camera and set resolution for faster performance
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.camera.isOpened():
            print("Error: Camera could not be opened.")
            exit()

        self.frame_count = 0
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        # Flag to track if the current gesture is already saved
        self.gesture_saved = False
        self.last_detected_gesture = None  # Track the last detected gesture

    def update_history(self):
        # Create a string of the current history to display in the label
        history_display = ""
        for gesture in self.gesture_history:
            history_display += f"{gesture}\n"
        self.history_label.text = f"History:\n{history_display.strip()}"

    def predict_in_thread(self, data_aux):
        try:
            prediction = model.predict([np.asarray(data_aux)])
            current_gesture = labels_dict[int(prediction[0])]
            self.prediction_label.text = current_gesture  # Update label text

            # Save the gesture only if it hasn't been saved already and it's a new gesture
            if current_gesture != self.last_detected_gesture:
                # Add new gesture to history
                if len(self.gesture_history) >= 5:
                    # Remove the first gesture (keeping only the latest 5)
                    self.gesture_history.pop(0)
                self.gesture_history.append(current_gesture)

                # Update the history display
                self.update_history()

                # Mark that the gesture has been saved
                self.gesture_saved = True
                self.last_detected_gesture = current_gesture  # Update the last detected gesture

        except Exception as e:
            print(f"Prediction error: {e}")
            self.prediction_result = "Error"
            self.prediction_label.text = "Error"  # Update label on error

    def update(self, dt):
        ret, frame = self.camera.read()
        if not ret:
            return

        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        results = hands.process(frame_rgb)
        data_aux = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x_ = []
                y_ = []

                # Extract hand landmarks and append raw coordinates for simplicity
                for landmark in hand_landmarks.landmark:
                    x_.append(landmark.x)
                    y_.append(landmark.y)

                # Prepare the input features for the model
                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                    data_aux.append(hand_landmarks.landmark[i].y - min(y_))

            # Only make predictions if we have 42 features (1 hand detected)
            if len(data_aux) == 42:
                threading.Thread(target=self.predict_in_thread, args=(data_aux,)).start()
            else:
                print(f"Warning: Unexpected feature count {len(data_aux)}")

            # Draw bounding box
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) + 10
            y2 = int(max(y_) * H) + 10
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # Update Kivy UI with the camera frame
        buf = cv2.flip(frame, 0)
        texture = Texture.create(size=(buf.shape[1], buf.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        self.image_widget.texture = texture

    def on_stop(self):
        if self.camera.isOpened():
            self.camera.release()
            print("Camera released.")
        
        # Reset gesture history and saved flag when stopping the app
        self.gesture_history.clear()
        self.gesture_saved = False
        self.last_detected_gesture = None  # Reset last detected gesture
        self.history_label.text = "History: None"

class HandSignApp(App):
    def build(self):
        return HandSignDetector()

    def on_stop(self):
        self.root.on_stop()

if __name__ == '__main__':
    HandSignApp().run()
