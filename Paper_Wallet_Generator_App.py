import os
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
import fitz  # PyMuPDF
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Line, Ellipse, Canvas
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.core.window import Window

from kivy.graphics import Color, Rectangle
from pdf_utils.PDF_Helper import PDF_Helper
from coin_utils.coin_utils.Create_Address_Doge import Create_Address_Doge
from Paper_Wallet_Generator_Helper import Paper_Wallet_Generator_Helper
from PIL import Image as pil_img

from pdf_utils.Draw_Wallet import Draw_Wallet


class ColoredLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # Set the background color (RGBA)
            Color(0.5, 0.5, 0.5, 1)  # Grey color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Bind the size and position to update the rectangle
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# class PDFViewer(FloatLayout):
class Paper_Wallet_Generator_ui(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pdf_helper: PDF_Helper = PDF_Helper()
        self.create_address_doge: Create_Address_Doge = Create_Address_Doge()
        self.privkey: str = ""
        self.pub_address: str = ""
        self.privkey, self.pub_address = self.create_address_doge.make_address_doge(
            print_result=False
        )
        self.paper_wallet_generator_helper: Paper_Wallet_Generator_Helper = (
            Paper_Wallet_Generator_Helper()
        )

        self.privkey_qr_img: pil_img.Image = (
            self.paper_wallet_generator_helper.generate_qrcode_img(qr_text=self.privkey)
        )
        self.pub_address_qr_img: pil_img.Image = (
            self.paper_wallet_generator_helper.generate_qrcode_img(
                qr_text=self.pub_address
            )
        )
        self.drawwallet: Draw_Wallet = Draw_Wallet()
        self.pdf_as_bytes: bytes = self.drawwallet.draw_wallet_return_bytes_2(
            pub_address=self.pub_address,
            pub_address_qr_img=self.pub_address_qr_img,
            privkey=self.privkey,
            privkey_qr_img=self.privkey_qr_img,
        )

        self.orientation = "vertical"
        self.size_hint = (1, 1)
        self.padding = 30

        self.pdf_document: fitz.Document = self.pdf_helper.open_pdf_from_bytes(
            pdf_bytes=self.pdf_as_bytes
        )
        self.pages_count: int = len(self.pdf_document)
        # self.current_page_lbl: ColoredLabel = ColoredLabel(
        #     text=str(self.pdf_helper.current_page),
        #     size_hint=(0.3, 1),
        #     font_size="20dp",
        #     halign="center",  # Center horizontally
        #     valign="middle",  # Center vertically
        # )
        self.print_paper_wallet_text: str = "Print"
        self.print_paper_wallet = Button(
            text=f"{self.print_paper_wallet_text}",
            size_hint=(1, 1),
        )
        self.print_paper_wallet.bind(on_press=self.print_wallet)
        self.generate_paper_wallet_text: str = "Generate"
        self.generate_paper_wallet = Button(
            text=f"{self.generate_paper_wallet_text}",
            size_hint=(1, 1),
        )
        self.generate_paper_wallet.bind(on_press=self.generate_wallet)

        # if self.pdf_helper.pages_count == 1:
        #     self.next_page_btn.text = ">"
        #     self.prev_page_btn.text = "<"
        #     # self.next_page_btn.disabled = True
        #     # self.prev_page_btn.disabled = True
        # self.image_box: BoxLayout = BoxLayout(orientation="vertical")
        self.image_widget: Image = Image()
        self.image_widget.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.btns_box: BoxLayout = BoxLayout(orientation="horizontal")
        self.btns_box.size_hint = (1, 2)
        self.btns_box.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.btns_box.add_widget(self.print_paper_wallet)
        # self.btns_box.add_widget(self.current_page_lbl)
        self.btns_box.add_widget(self.generate_paper_wallet)

        self.add_widget(self.image_widget)
        self.add_widget(self.btns_box)
        self.load_page()
        # self.label = Label(
        #     text="Hello",
        #     # size_hint=(0, 0.2),
        #     size=(200, 50),
        # )
        # # self.label.color = (0, 0, 0, 1)  # black
        # self.label.color = (0, 0, 1, 1)  # blue
        # Window.bind(mouse_pos=self.on_mouse_move)
        # self.add_widget(self.label)
        # self.points = []
        self.window_y_add: float = 100
        self.window_x_add: float = 30
        self.set_window_size()

    def set_window_size(
        self,
    ):
        Window.size = (
            self.image_widget.size[0] + self.window_x_add,
            self.image_widget.size[1] + self.window_y_add,
        )

    def generate_wallet(self, instance):
        print(f"TODO Generate wallet")

    def print_wallet(self, instance):
        print(f"TODO Printing wallet")

    def load_page(self):
        """
        Loads the specified page from the PDF document and displays it in the image widget.

        This method retrieves the current page from the PDF document, converts it to a pixmap,
        and then sets the texture and size of the image widget to display the page content.
        """
        pix_map: fitz.Pixmap = self.pdf_helper.get_current_pixmap()
        self.image_widget.texture = self.create_texture(pix=pix_map)
        self.image_widget.size = (
            pix_map.width,
            pix_map.height,
        )  # Set the image widget's size
        self.image_widget.size_hint = (
            None,
            None,
        )  # Disable size hints for manual control
        self.btns_box.size_hint_y = None
        self.btns_box.size_hint = (None, None)
        self.btns_box.height = 100
        self.btns_box.width = pix_map.width
        # self.set_btn_texts()

    def set_btn_texts(self):
        self.current_page_lbl.text = str(self.pdf_helper.current_page)
        if not self.pdf_helper.pages_count == 1:
            if self.pdf_helper.current_page == 0:
                self.print_paper_wallet.text = (
                    f"< to Page:({self.pdf_helper.pages_count-1})"
                )
                self.generate_paper_wallet.text = (
                    f"to Page:({self.pdf_helper.current_page+1}) >"
                )

            elif self.pdf_helper.current_page == self.pdf_helper.pages_count - 1:
                self.print_paper_wallet.text = (
                    f"< to Page:({self.pdf_helper.current_page-1})"
                )
                self.generate_paper_wallet.text = f"to Page:({0}) >"

            else:
                self.print_paper_wallet.text = (
                    f"< to Page:({self.pdf_helper.current_page-1})"
                )
                self.generate_paper_wallet.text = (
                    f"to Page:({self.pdf_helper.current_page+1}) >"
                )

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

    def on_mouse_move(self, window, pos):
        # Update label position to follow the mouse
        center_position: tuple[float, float] = (
            pos[0] - self.label.width / 2,
            pos[1] - self.label.height / 2,
        )
        center_below_mouse_position: tuple[float, float] = (
            pos[0] - self.label.width / 2 - 10,
            pos[1] - self.label.height / 2 - 70,
        )
        # self.label.pos = center_position  # (pos[0] - self.label.width / 2, pos[1] - self.label.height / 2)
        self.label.pos = center_below_mouse_position

    def draw_red_point(
        self,
        canvas: Canvas,
        position: tuple[int, int] = (100, 100),
        size: tuple[int, int] = (5, 5),
    ) -> None:
        """Draws a red point (small ellipse) on the canvas.

        Args:
            canvas: The canvas object to draw on.
            position: A tuple representing the x, y coordinates of the point's center. Defaults to (100, 100).
            size: A tuple representing the width and height of the point. Defaults to (10, 10).
        """
        with canvas:
            Color(1, 0, 0)  # RGB for red
            self.point = Ellipse(
                pos=(position[0] - size[0] / 2, position[1] - size[1] / 2), size=size
            )

    def remove_last_drawing(self):
        """Removes the last drawn line and point from the canvas."""
        if len(self.canvas.children) > 3:
            # Remove the last instruction (usually the line)
            self.canvas.remove(self.canvas.children[-1])
            # Remove the second-to-last instruction (usually the point)
            self.canvas.remove(self.canvas.children[-1])
            self.canvas.remove(self.canvas.children[-1])

    # def on_touch_down(self, touch):
    #     # Check if the touch event is from a mouse and if it's a scroll event
    #     if touch.is_mouse_scrolling:
    #         return False  # Ignore mouse scroll events

    #     if self.image_widget.collide_point(touch.x, touch.y):
    #         self.points.append((touch.x, touch.y))
    #         if len(self.points) == 2:
    #             self.measure_distance()

    #             with self.canvas:
    #                 # Color(1, 0, 0, 1)  # Red color for the line
    #                 Color(0, 0, 1, 1)  # blue color for the line
    #                 # Line(points=[touch.x, touch.y, touch.x, touch.y], width=2)
    #                 Line(points=self.points, width=2)

    #                 return super().on_touch_down(
    #                     touch
    #                 )  # Ensure other touch events are handled
    #         if len(self.points) == 3:
    #             self.remove_last_drawing()
    #             self.points = []  # Reset points after measuring
    #             self.points.append((touch.x, touch.y))
    #         if len(self.points) == 1:
    #             self.draw_red_point(
    #                 canvas=self.canvas,
    #                 position=(self.points[0]),
    #             )
    #     return super().on_touch_down(touch)  # Ensure other touch events are handled

    def measure_distance(self):
        """
        Measures the distance between two points in pixels, DPI, millimeters, and inches.

        This method calculates the Euclidean distance between two points provided in the `self.points` attribute.
        It then converts the pixel distance to DPI, millimeters, and inches based on the page's DPI.
        """

        distance_pixels: float
        distance_mm: float
        distance_inch: float

        distance_pixels, distance_mm, distance_inch = self.pdf_helper.measure_distance(
            p1=self.points[0],
            p2=self.points[1],
        )

        # Print the distances in different units
        print("-" * 30)
        print(f"Distance: {distance_pixels:.2f} pixels")
        print(f"Distance: {distance_mm:.2f} mm")
        print(f"Distance: {distance_inch:.2f} inches")

        # Update the label with all distances
        self.label.text = (
            f"Distance: \n"
            f"{distance_mm:.2f} mm\n"
            f"{distance_inch:.2f} inches\n"
            f"{distance_pixels:.2f} pixels\n"
            # f"{distance_dpi:.2f} DPI\n"
        )


class Paper_Wallet_Generator_App(App):
    def build(self):
        # my_path: str = os.path.dirname(__file__)
        # Ruler_inch: str = "Ruler_6-inch_by_4.pdf"
        # ruler_12_inch_30cm: str = "Print-Ruler-12-inches-and-30-centimeters-A4.pdf"
        # Ruler_cm: str = "Ruler_15-cm_by_mm.pdf"
        # Meta_quest: str = "Meta-Quest-2-Quickstart-Guide-DE.pdf"

        # pdf_path: str = os.path.join(my_path, Ruler_inch)
        # # pdf_path: str = os.path.join(my_path, ruler_12_inch_30cm)
        # # pdf_path: str = os.path.join(my_path, Ruler_cm)
        # # pdf_path: str = os.path.join(my_path, Meta_quest)

        # # pdf_path: str = r"D:\11\02\14\kivy_measure_pdf\Ruler_6-inch_by_4.pdf"
        # # pdf_path: str = (
        # #     r"D:\11\02\14\kivy_measure_pdf\Print-Ruler-12-inches-and-30-centimeters-A4.pdf"
        # # )
        # # # pdf_path: str = r"D:\11\02\14\kivy_measure_pdf\eosc300mk3-500mk2-im13-en.pdf"
        # # pdf_path: str = r"D:\11\02\13\pdf_utils\outputs\Draw_Wallet_test.pdf"
        paper_wallet_generator_ui: Paper_Wallet_Generator_ui = (
            Paper_Wallet_Generator_ui()
        )
        return paper_wallet_generator_ui


if __name__ == "__main__":
    Paper_Wallet_Generator_App().run()
