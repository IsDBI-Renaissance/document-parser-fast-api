from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import fitz  
import tempfile

app = FastAPI()

@app.post("/parse")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    # Save uploaded PDF temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Open the PDF and extract text
        doc = fitz.open(tmp_path)
        extracted_text = ""

        for page in doc:
            extracted_text += page.get_text()

        doc.close()
        return JSONResponse(content={"text": extracted_text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")
