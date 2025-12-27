import shutil
from pypdf import PdfReader, PdfWriter
import tempfile
import typing

def two_sided_reorder(input_file: typing.IO[bytes], output_file: typing.IO[bytes]) -> None:
    output_pdf = PdfWriter()

    src_pdf = PdfReader(input_file)
    pages = src_pdf.pages

    for p in range(0, len(pages)):
        odd_page = p % 2 == 1
        offset = p // 2
        if odd_page:
            src_index = len(pages) - 1 - offset
            output_pdf.add_page(pages[src_index])
        else:
            src_index = offset
            output_pdf.add_page(pages[src_index])

    output_pdf.write(output_file)

def two_sided_reorder_files(pdf_path: str, merged_path: str) -> None:
    with open(pdf_path, 'rb') as src_pdf_file, open(merged_path, "wb") as writefile:
        two_sided_reorder(src_pdf_file, writefile)

def two_sided_reorder_inplace(pdf_path: str) -> None:
    with open(pdf_path, 'rb') as src_pdf_file, tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_pdf_file:
        two_sided_reorder(src_pdf_file, temp_pdf_file)
        temp_pdf_file.close()
        temp_pdf_file_path = temp_pdf_file.name
        shutil.copy(temp_pdf_file_path, pdf_path)


def odd_even_merge(odd_pages_path: str, even_pages_path: str, merged_path: str) -> None:
    output_pdf = PdfWriter()

    with open(odd_pages_path, 'rb') as odd_pages_file, open(even_pages_path, 'rb') as even_pages_file:
        odd_pdf = PdfReader(odd_pages_file)
        even_pdf = PdfReader(even_pages_file)

        odd_pages = odd_pdf.pages
        even_pages = list(reversed(even_pdf.pages))
        odd_i = 0
        even_i = 0

        while odd_i < len(odd_pages) or even_i < len(even_pages):
            if odd_i < len(odd_pages):
                output_pdf.add_page(odd_pages[odd_i])
                odd_i += 1