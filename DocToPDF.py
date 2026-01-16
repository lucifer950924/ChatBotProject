from pathlib import Path
import win32com.client

def docxToPdf(path:str,outPath = None):
    docx_path = Path(path).resolve()
    if outPath is None:
        outPath = docx_path.with_suffix(".pdf")


    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False

    doc = word.Documents.Open(str(path))
    doc.SaveAs(str(outPath),FileFormat = 17)
    doc.Close()
    word.Quit()
