import os
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
import fitz  # PyMuPDF
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from Paper_Wallet_Generator_Helper import Paper_Wallet_Generator_Helper


# class PDFViewer(FloatLayout):
class Paper_Wallet_Generator_ui(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paper_wallet_generator_helper: Paper_Wallet_Generator_Helper = (
            Paper_Wallet_Generator_Helper()
        )
        self.orientation = "vertical"
        self.size_hint = (1, 1)
        self.padding = 10
        # setup print button
        self.print_wallet_btn_text: str = "Print"
        self.print_wallet_btn = Button(
            text=f"{self.print_wallet_btn_text}",
            size_hint=(1, 1),
        )
        self.print_wallet_btn.bind(on_press=self.print_wallet)
        # setup generate paper wallet button
        self.generate_wallet_btn_text: str = "Generate"
        self.generate_wallet_btn = Button(
            text=f"{self.generate_wallet_btn_text}",
            size_hint=(1, 1),
        )
        self.generate_wallet_btn.bind(on_press=self.generate_wallet)
        # setup save_pdf_btn button
        self.save_pdf_btn_text: str = "save as pdf"
        self.save_pdf_btn = Button(
            text=f"{self.save_pdf_btn_text}",
            size_hint=(1, 1),
        )
        self.save_pdf_btn.bind(on_press=self.save_pdf)
        # setup image widged(for showing the paper wallet)
        self.image_widget: Image = Image()
        self.image_widget.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        # create btns box
        self.btns_box_height: float = 100
        self.btns_box_size_hint: tuple = (None, None)
        self.btns_box: BoxLayout = BoxLayout(orientation="horizontal")
        self.btns_box.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.btns_box.size_hint = self.btns_box_size_hint
        self.btns_box.height = self.btns_box_height
        self.btns_box.add_widget(self.print_wallet_btn)
        self.btns_box.add_widget(self.generate_wallet_btn)
        self.btns_box.add_widget(self.save_pdf_btn)

        # Create a TextInput for terminal output
        self.terminal_output_height: float = 200
        self.terminal_output_size_hint: tuple = (None, None)
        self.terminal_output_pos_hint = {"center_x": 0.5, "center_y": 0.35}
        self.terminal_output = TextInput(
            size_hint=self.terminal_output_size_hint,
            readonly=False,
            multiline=True,
            pos_hint=self.terminal_output_pos_hint,
        )
        self.terminal_output.height = self.terminal_output_height
        # Add widgets to the screen
        self.add_widget(self.image_widget)
        self.add_widget(self.btns_box)
        self.add_widget(self.terminal_output)  # Add terminal output area

        self.load_page(pix_map=self.paper_wallet_generator_helper.pix_map)
        self.window_y_add: float = 100
        self.window_x_add: float = 30
        self.set_window_size()
        self.dotted_line: str = "-" * 40

    def update_terminal(self, message: str):
        """Update the terminal output area with a new message."""
        self.terminal_output.text += f"{message}\n"  # Append new message

    def set_window_size(
        self,
    ):
        Window.size = (
            self.image_widget.size[0] + self.window_x_add,
            self.image_widget.size[1] + self.window_y_add,
        )

    def generate_wallet(self, instance):
        self.paper_wallet_generator_helper.Generate_new_paper_wallet()
        self.load_page(pix_map=self.paper_wallet_generator_helper.pix_map)

    def save_pdf(self, instance):
        is_saved: bool = False
        path: str = ""
        is_saved, path = self.paper_wallet_generator_helper.save_as_pdf()
        dotted_line: str = "-" * 40
        terminal_message: str = f"""{dotted_line}
Is pdf saved:{is_saved}"""

        self.update_terminal(message=terminal_message)
        terminal_message = f"""PDF Path:{path}
{dotted_line}"""
        self.update_terminal(message=terminal_message)

    def update_terminal_info(
        self,
    ):
        dotted_line: str = "-" * 40
        message: str = (
            f"""{dotted_line}
Private key:
{self.paper_wallet_generator_helper.privkey}"""
        )
        self.update_terminal(message=message)
        message = f"""Public adress:
{self.paper_wallet_generator_helper.pub_address}
{dotted_line}"""
        self.update_terminal(message=message)

    def print_wallet(self, instance):
        self.paper_wallet_generator_helper.print_paper_wallet()
        dotted_line: str = "-" * 40
        message: str = (
            f"""{dotted_line}
printing Paper wallet:
{self.paper_wallet_generator_helper.pub_address}
{dotted_line}"""
        )
        self.update_terminal(message=message)
        # print(f"TODO Printing wallet")

    def load_page(
        self,
        pix_map: fitz.Pixmap,
    ):
        """
        Loads the specified page from the PDF document and displays it in the image widget.

        This method retrieves the current page from the PDF document, converts it to a pixmap,
        and then sets the texture and size of the image widget to display the page content.
        """
        self.image_widget.texture = self.create_texture(pix=pix_map)
        self.image_widget.size = (
            pix_map.width,
            pix_map.height,
        )  # Set the image widget's size
        self.image_widget.size_hint = (
            None,
            None,
        )  # Disable size hints for manual control

        self.btns_box.width = pix_map.width
        self.terminal_output.width = pix_map.width
        self.update_terminal_info()

    def create_texture(self, pix: fitz.Pixmap):
        """
        Creates a Kivy texture from a PyMuPDF Pixmap, flipping it vertically.

        This method converts a PyMuPDF Pixmap object into a Kivy Texture.
        It also flips the texture vertically to match the standard Kivy coordinate system.
        """
        texture: Texture = Texture.create(size=(pix.width, pix.height))
        texture.blit_buffer(pix.samples, colorfmt="rgb", bufferfmt="ubyte")
        # Flip the texture vertically
        texture.flip_vertical()
        return texture


class Paper_Wallet_Generator_App(App):
    def build(self):
        paper_wallet_generator_ui: Paper_Wallet_Generator_ui = (
            Paper_Wallet_Generator_ui()
        )
        return paper_wallet_generator_ui


if __name__ == "__main__":
    Paper_Wallet_Generator_App().run()
