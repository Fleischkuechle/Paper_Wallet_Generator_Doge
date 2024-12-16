import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from kivy.uix.button import Button
from PIL import Image as pil_img
import qrcode
from kivy.uix.image import Image as kv_img
from kivy.utils import get_color_from_hex

kivy.require("2.0.0")


class Paper_Wallet_Generator_Helper(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.Main_Color = get_color_from_hex("171514")
        self.input_text = TextInput(
            hint_text="Enter text",
            multiline=False,
        )

        self.input_text.size_hint_max_y = 40
        layout.add_widget(self.input_text)
        self.kv_image: kv_img = kv_img(
            fit_mode="contain",
        )
        layout.add_widget(self.kv_image)
        generate_button = Button(text="Generate QR Code")
        generate_button.size_hint_max_y = 50
        generate_button.bind(on_press=self.generate_qrcode)
        layout.add_widget(generate_button)  # Create a blank white image
        self.script_parent_folder_path: str = os.path.dirname(__file__)
        self.qr_code_img_name: str = "QR_Code_Generator_App_result"
        width: int = 800
        height: int = width
        self.img_size: tuple[int, int] = (width, height)
        self.qr_code_img_size: str = f"_{width}_{height}"
        self.extension: str = ".png"
        self.final_img_name: str = (
            f"{self.qr_code_img_name}{self.qr_code_img_size}{self.extension}"
        )
        self.img_path: str = os.path.join(
            self.script_parent_folder_path, self.final_img_name
        )
        return layout

    def generate_qrcode(self, instance):
        qr_text: str = self.input_text.text
        if qr_text:
            try:
                qr = qrcode.QRCode(
                    # version=1,
                    # box_size=10,
                    # border=5,
                )
                qr.add_data(qr_text)
                qr.make(fit=True)
                img: pil_img.Image = qr.make_image(
                    fill_color="black",
                    back_color="white",
                )
                resized_image: pil_img.Image = self.resize_image(
                    img=img,
                    size=self.img_size,
                )
                resized_image.save(self.img_path)
                self.kv_image.source = self.img_path
                # Load the generated QR code image
                self.kv_image.reload()
                print(f"Created qr code form text:({qr_text})")
                print(f"Saved here: {self.img_path}")
                print(f"Image width:{self.img_size[0]} , height:{self.img_size[1]}")
            except Exception as e:
                print(f"Error {e}")
        else:
            print("Please enter text or URL.")


if __name__ == "__main__":
    Paper_Wallet_Generator_Helper().run()
