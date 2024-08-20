from lib.paperscraper.pdf import save_pdf_from_dump


if __name__ == '__main__':
    # Save PDFs in the pdf folder and name the files by their DOI
    try:
        save_pdf_from_dump('../../data/Gaucher.jsonl', pdf_path='../../data/downloaded_pdfs', key_to_save='doi')
    except NameError:
        print(NameError)

