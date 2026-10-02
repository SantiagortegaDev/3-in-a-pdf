from fastapi import FastAPI
from fastapi.responses import FileResponse
import tempfile
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from starlette.background import BackgroundTask
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import XPreformatted

app = FastAPI()


@app.get("/")
async def root():
    content = (
    "   _____    _                             ______\n"
    "  |__  /   (_)___     ____ _   ____  ____/ / __/\n"
    "   /_ <   / / __ \\   / __ `/  / __ \\/ __  / /_\n"
    " ___/ /  / / / / /  / /_/ /  / /_/ / /_/ / __/\n"
    "/____/  /_/_/ /_/   \\__,_/  / .___/\\__,_/_/\n"
    "                           /_/\n"
    "test\n"
    '<u><a href="https://loose-atlanta-built-median.trycloudflare.com/" color="blue">test link</a></u>\n'
    "test"
)
    textfont = ParagraphStyle("mono", fontName="Courier", fontSize=9, leading=11)

    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    try:
        doc = SimpleDocTemplate(path, pagesize=A4, title="3 in a pdf", author="@santiagortega")
        doc.build([XPreformatted(content, textfont)])
    except Exception as e:
        os.remove(path)  
        print(e)
        return {"error" : f"{e}"}

    return FileResponse(
    path,
    status_code=200,
    media_type="application/pdf",
    filename=f"test.pdf",
    content_disposition_type="inline",
    background=BackgroundTask(os.remove, path)
    )
