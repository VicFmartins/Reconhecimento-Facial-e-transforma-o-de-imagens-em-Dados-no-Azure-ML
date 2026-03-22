from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Query, UploadFile
from fastapi.responses import FileResponse

from app.models import ImageAnalysisResponse
from app.vision_service import VisionPrivacyService


app = FastAPI(
    title="Safe Vision Analysis Lab",
    version="1.0.0",
    description="API para analise de imagem e anonimizacao de rostos, com foco em privacidade e extracao segura de dados visuais.",
)

service = VisionPrivacyService()
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "safe-vision-analysis"}


@app.post("/api/images/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...)) -> ImageAnalysisResponse:
    content = await file.read()
    result = service.analyze_image(file.filename or "uploaded-image", content)
    return ImageAnalysisResponse(**result)


@app.post("/api/images/anonymize")
async def anonymize_image(
    file: UploadFile = File(...),
    blur_radius: int = Query(default=18, ge=5, le=50),
):
    content = await file.read()
    image_bytes, faces = service.anonymize_image(content, blur_radius=blur_radius)
    filename = f"{uuid4().hex}.png"
    output_path = OUTPUT_DIR / filename
    output_path.write_bytes(image_bytes)

    headers = {
        "X-Faces-Detected": str(len(faces)),
        "X-Output-File": filename,
    }
    return FileResponse(output_path, media_type="image/png", filename=filename, headers=headers)
