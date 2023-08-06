import boto3
import PIL.Image
import json
import base64
import io
from os.path import join, dirname
import tempfile
import gzip
import shutil

from PIL import Image, ImageFont, ImageDraw
import qrcode
import numpy as np

class Watermarker:

    _MAX_PAGES=349

    def get_qr(self, url):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4)
        qr.add_data(url)
        img = qr.make_image(fill_color='#471BD9', back_color='white')
        return img


    def white_to_trans(self, image):

        data = np.array(image)
        red, green, blue, alpha = data.T

        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[...][white_areas.T] = (0, 0, 0, 0)  # Transpose back needed

        im2 = Image.fromarray(data)
        return im2

    def place_watermark(self, decision, case, number_of_pages):
        decision = decision.convert('RGBA')
        decision_size = decision.size

        short = f'tl8.me/{case}'

        stamp_file = join(dirname(__file__), 'tolaat-stamp.png')
        watermark = Image.open(stamp_file, 'r')
        watermark_size = watermark.size


        qr = self.get_qr(short)
        qr_size = qr.size

        font_size = 20

        total_width = qr_size[0]+watermark_size[0]
        graphics_height = max(qr_size[1], watermark_size[1])
        total_height = graphics_height + font_size + 5

        new_im = Image.new('RGBA', (total_width, total_height),  (255, 255, 255, 0))
        new_im.paste(watermark, (0, 0))
        new_im.paste(qr, (watermark_size[0], 0))

        margin = (5,5)

        d = ImageDraw.Draw(new_im)
        text_color = (71, 27, 217, 255)

        fontFile = join(dirname(__file__), 'Arimo-Bold.ttf')

        font = ImageFont.truetype(fontFile, size=font_size)
        text_size = font.getsize(short)
        location = (total_width//2-text_size[0]//2, max(watermark_size[1], qr_size[1])+5)
        d.text(location, short, fill=text_color, font=font)


        x = margin[0]
        y = decision_size[1] - new_im.size[1] - margin[1]

        transparent_background = self.white_to_trans(new_im)

        transparency = Image.new('RGBA', decision_size, (0, 0, 0, 0))
        transparency.paste(transparent_background, (x, y), transparent_background)

        decision.paste(transparent_background, (x, y), transparent_background)

        if number_of_pages > Watermarker._MAX_PAGES:
            long_doc_warning = 'המסמך מוצג באופן חלקי בשל אורכו החריג'
            long_doc_warning = long_doc_warning[::-1]
            long_doc_warning_size = font.getsize(long_doc_warning)
            long_doc_warning_location = (decision_size[0]//2-long_doc_warning_size[0]//2,
                                            decision_size[1] - long_doc_warning_size[1] - margin[1])
            d = ImageDraw.Draw(decision)
            d.text(long_doc_warning_location, long_doc_warning, fill=text_color, font=font)

        return decision

class PdfGenerator:

    watermarker = Watermarker()

    @staticmethod
    def to_png(page):
        page = page.replace("<img class='picCenter' style='width: inherit;' src='data:image/.png;base64,", "")
        page = page.replace("'></img>", "")
        page = base64.b64decode(page)
        return page


    @staticmethod
    def to_pil(page):
        page = PdfGenerator.to_png(page)
        page = io.BytesIO(page)
        page = PIL.Image.open(page)
        return page

    @staticmethod
    def process_images(images, url_path, title):

        def pages_iterator(images):
            for page in images:
                page = PdfGenerator.to_png(page)
                page = io.BytesIO(page)
                page = PIL.Image.open(page)
                page.load()
                yield page

        first = images[0]

        pil = PdfGenerator.to_pil(first)
        pil2 = PdfGenerator.watermarker.place_watermark(pil, url_path, len(images))
        pil3 = pil2.convert('P')

        spooled_pdf = tempfile.SpooledTemporaryFile()
        pil3.save(spooled_pdf, format='pdf', title=title, append_images=pages_iterator(images[1:]), save_all=True)

        spooled_pdf.seek(0)
        spooled_gz = tempfile.SpooledTemporaryFile()
        gzf = gzip.open(spooled_gz, 'wb')

        shutil.copyfileobj(spooled_pdf, gzf)
        gzf.close()

        spooled_gz.seek(0)
        return spooled_gz



    def build_document(self, caseid, decision_type, number, url_path, title):
        number = str(number).zfill(3)
        path = f'documents_v2/decision_documents/{caseid}/{decision_type}/{number}.json'
        bucket = 'cloud-eu-central-1-q97dt1m5d4rndek'

        s3 = boto3.client('s3')

        r = s3.get_object(Bucket=bucket, Key=path)
        j = json.load(r['Body'])
        pages = j['d']
        return PdfGenerator.process_images(pages, url_path, title), r['LastModified']


if __name__=='__main__':

    pg = PdfGenerator()
    pg.do('32485892', 'decisions', 1, '5-01-10', """ר"צ שלום נ' דוד: 323""")