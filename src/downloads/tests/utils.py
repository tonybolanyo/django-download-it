from io import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile


def get_fake_pdf_file(filename='foo.pdf', content_type='application/pdf'):
    """
    Creafe a fake PDF file for tests.
    Use StringIO writing `%PDF-1.5` at the begining of file,
    so `magic` get the mime as `application/pdf`.
    """

    io = StringIO()
    io.write('%PDF-1.5')
    pdf_file = InMemoryUploadedFile(
        file=io, field_name=None, name=filename,
        content_type='application/pdf', size=2300, charset=None)
    pdf_file.seek(0)
    return pdf_file
