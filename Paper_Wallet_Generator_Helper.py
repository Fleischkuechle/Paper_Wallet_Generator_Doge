from PIL import Image as pil_img
import qrcode


class Paper_Wallet_Generator_Helper:
    def __init__(self):
        self.width: int = 800
        self.height: int = self.width
        self.img_size: tuple[int, int] = (self.width, self.height)

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
