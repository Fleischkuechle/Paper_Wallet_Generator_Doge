import os
import qrcode
from PIL import Image as pil_img
import fitz  # PyMuPDF

from pdf_utils.PDF_Helper import PDF_Helper
from coin_utils.coin_utils.Create_Address_Doge import Create_Address_Doge
from pdf_utils.Draw_Wallet import Draw_Wallet
from pdf_utils.ImagePrinter import ImagePrinter


class Paper_Wallet_Generator_Helper:
    def __init__(self):
        self.width: int = 800
        self.height: int = self.width
        self.img_size: tuple[int, int] = (self.width, self.height)

        self.pdf_helper: PDF_Helper = PDF_Helper()
        self.create_address_doge: Create_Address_Doge = Create_Address_Doge()
        self.drawwallet: Draw_Wallet = Draw_Wallet()
        self.image_printer: ImagePrinter = ImagePrinter()
        self.privkey: str = ""
        self.pub_address: str = ""
        self.privkey_qr_img: pil_img.Image = None
        self.pub_address_qr_img: pil_img.Image = None
        self.pdf_as_bytes: bytes = bytes()
        self.pdf_document: fitz.Document = None
        self.pix_map: fitz.Pixmap = None
        self.Generate_new_paper_wallet()

    def Generate_new_paper_wallet(
        self,
    ) -> fitz.Document:

        self.privkey, self.pub_address = self.create_address_doge.make_address_doge(
            print_result=False
        )

        self.privkey_qr_img = self.generate_qrcode_img(qr_text=self.privkey)
        self.pub_address_qr_img: pil_img.Image = self.generate_qrcode_img(
            qr_text=self.pub_address
        )
        self.pdf_as_bytes = self.drawwallet.draw_wallet_return_bytes_2(
            pub_address=self.pub_address,
            pub_address_qr_img=self.pub_address_qr_img,
            privkey=self.privkey,
            privkey_qr_img=self.privkey_qr_img,
        )

        self.pdf_document = self.pdf_helper.open_pdf_from_bytes(
            pdf_bytes=self.pdf_as_bytes
        )
        self.pix_map = self.pdf_helper.get_current_pixmap()
        return self.pdf_document

    def save_paralell(
        self,
    ) -> tuple[bool, str]:
        is_saved: bool = False
        path: str = ""
        folder_path: str = os.path.dirname(__file__)
        path = os.path.join(folder_path, self.pub_address + ".pdf")
        # self.pdf_document.save_snapshot(filename=path)
        self.pdf_document.save(filename=path)
        is_saved = True
        return is_saved, path

    def save_as_pdf(self, folder_path: str = "") -> tuple[bool, str]:
        is_saved: bool = False
        path: str = ""
        if folder_path != "":
            # directory_path:str = os.path.dirname(folder_path)
            if os.path.exists(path=folder_path):
                path = os.path.join(folder_path, self.pub_address + ".pdf")
                # self.pdf_document.save_snapshot(filename=path)
                self.pdf_document.save(filename=path)
                is_saved = True
                return is_saved, path
            else:
                is_saved, path = self.save_paralell()
        else:
            is_saved, path = self.save_paralell()

        return is_saved, path

    def print_paper_wallet(
        self,
    ):
        self.image_printer.print_pdf_from_memory(
            pdf_data=self.pdf_as_bytes,
            document_name=self.pub_address,
        )

    def get_current_pixmap(
        self,
    ):
        # self.pix_map = self.pdf_helper.get_current_pixmap()
        return self.pix_map

    def generate_qrcode_img(
        self,
        qr_text: str = "",
    ) -> pil_img.Image:
        resized_image: pil_img.Image = None
        if qr_text != "":
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
                resized_image = self.resize_image(
                    img=img,
                    size=self.img_size,
                )
                return resized_image

            except Exception as e:
                print(f"Error {e}")
                return resized_image

        else:
            print("Please enter text or URL.")
            return resized_image

    def resize_image(
        self,
        img: pil_img.Image,
        size: tuple[int, int],
    ) -> pil_img.Image:
        """Resize the image to the specified size.

        Args:
            img (pil_img.Image): The image to be resized.
            size (: tuple[int, int]): A tuple containing the desired width and height of the resized image.
                - **size[0]**: The width of the resized image in pixels.
                - **size[1]**: The height of the resized image in pixels.

        Returns:
            pil_img.Image: The resized image.
        """
        resized_image: pil_img.Image = img.resize(size)
        return resized_image


if __name__ == "__main__":
    pass
