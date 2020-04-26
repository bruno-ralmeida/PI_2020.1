from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os

def ler_pdf(arquivo):
    """
    Função criada para leitura de arquivos .pdf
    É necessário instalar o pdfminer 
    pip install pdfminer

    @Params Informar o nome do arquivo.
    @Return Retorna uma string com todos os dados do pdf
    """
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = f'{BASE}\{arquivo}'
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    
    for page in PDFPage.get_pages(filepath, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    
    filepath.close()
    device.close()
    retstr.close()
    return text

