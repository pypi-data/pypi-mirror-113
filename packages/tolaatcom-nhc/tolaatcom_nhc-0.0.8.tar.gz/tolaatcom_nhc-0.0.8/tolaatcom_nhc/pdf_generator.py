import boto3
import json
import base64
import io
import tempfile
import shutil
import PIL

class PdfGenerator:

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
    def process_images(images, title):

        def pages_iterator(images):
            for page in images:
                page = PdfGenerator.to_png(page)
                page = io.BytesIO(page)
                page = PIL.Image.open(page)
                page.load()
                yield page

        first = images[0]
        first_as_pil = PdfGenerator.to_pil(first)
        first_as_p = first_as_pil.convert('P')

        spooled_pdf = tempfile.SpooledTemporaryFile()
        first_as_p.save(spooled_pdf, format='pdf', title=title, append_images=pages_iterator(images[1:]), save_all=True)

        spooled_pdf.seek(0)
        return spooled_pdf



    def build_document(self, caseid, decision_type, number, url_path, title):
        number = str(number).zfill(3)
        path = f'documents_v2/decision_documents/{caseid}/{decision_type}/{number}.json'
        bucket = 'cloud-eu-central-1-q97dt1m5d4rndek'

        s3 = boto3.client('s3')

        r = s3.get_object(Bucket=bucket, Key=path)
        j = json.load(r['Body'])
        pages = j['d']
        return PdfGenerator.process_images(pages, title), r['LastModified']


if __name__=='__main__':

    pg = PdfGenerator()
    pg.do('32485892', 'decisions', 1, '5-01-10', """ר"צ שלום נ' דוד: 323""")