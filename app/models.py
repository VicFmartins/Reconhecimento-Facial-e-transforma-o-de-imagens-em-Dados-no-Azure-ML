from pydantic import BaseModel


class FaceBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class ImageAnalysisResponse(BaseModel):
    filename: str
    width: int
    height: int
    mode: str
    dominant_colors: list[str]
    mean_brightness: float
    faces_detected: int
    face_boxes: list[FaceBox]
    warning: str | None = None
