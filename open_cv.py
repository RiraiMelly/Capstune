from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.core.window import Window  # To capture keyboard input
import cv2

class CameraApp(App):
    def build(self):
        self.img_widget = Image()
        # Start capturing from the webcam
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            self.img_widget = Label(text="Error: Could not open webcam.")
        else:
            # Schedule the update method to refresh the image every frame
            Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 fps
        
        # Bind keyboard events to the window
        Window.bind(on_key_down=self.on_key_down)
        return self.img_widget

    def update(self, dt):
        ret, frame = self.cap.read()
        if ret:
            # Convert the image to texture for Kivy
            buf = cv2.flip(frame, 0).tobytes()  # Flip the image
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img_widget.texture = texture

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 113:  # 'q' key ASCII
            self.stop()  # Stop the app
        elif key == 27:  # ESC key
            self.stop()  # Stop the app
        elif key == 114:  # 'r' key ASCII
            self.capture_image()

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite("captured_image.png", frame)
            print("Image captured and saved as captured_image.png")

    def on_stop(self):
        # Release the webcam when the app is stopped
        self.cap.release()

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    CameraApp().run()
    