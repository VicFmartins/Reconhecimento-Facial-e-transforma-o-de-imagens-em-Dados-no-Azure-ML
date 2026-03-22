from __future__ import annotations

import io
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image, ImageFilter


@dataclass
class FaceDetectionResult:
    x: int
    y: int
    width: int
    height: int


class FaceDetector:
    def __init__(self) -> None:
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.cascade = cv2.CascadeClassifier(cascade_path)

    def detect_faces(self, image: Image.Image) -> list[FaceDetectionResult]:
        rgb = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return [FaceDetectionResult(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]


def load_image_from_bytes(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data)).convert("RGB")


def dominant_colors(image: Image.Image, top_n: int = 3) -> list[str]:
    resized = image.resize((64, 64))
    palette_image = resized.convert("P", palette=Image.Palette.ADAPTIVE, colors=top_n)
    palette = palette_image.getpalette()
    color_counts = sorted(palette_image.getcolors() or [], reverse=True)
    colors: list[str] = []
    for _, palette_index in color_counts[:top_n]:
        base = palette_index * 3
        rgb = palette[base : base + 3]
        colors.append("#{0:02x}{1:02x}{2:02x}".format(*rgb))
    return colors


def mean_brightness(image: Image.Image) -> float:
    grayscale = image.convert("L")
    pixels = np.array(grayscale, dtype=np.float32)
    return round(float(pixels.mean()) / 255.0, 4)


class VisionPrivacyService:
    def __init__(self, detector: FaceDetector | None = None) -> None:
        self.detector = detector or FaceDetector()

    def analyze_image(self, filename: str, data: bytes) -> dict:
        image = load_image_from_bytes(data)
        faces = self.detector.detect_faces(image)
        warning = None
        if faces:
            warning = "Deteccao usada para anonimizar rostos. O projeto nao realiza identificacao biometrica."

        return {
            "filename": filename,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "dominant_colors": dominant_colors(image),
            "mean_brightness": mean_brightness(image),
            "faces_detected": len(faces),
            "face_boxes": [
                {"x": face.x, "y": face.y, "width": face.width, "height": face.height}
                for face in faces
            ],
            "warning": warning,
        }

    def anonymize_image(self, data: bytes, blur_radius: int = 18) -> tuple[bytes, list[FaceDetectionResult]]:
        image = load_image_from_bytes(data)
        faces = self.detector.detect_faces(image)
        working = image.copy()

        for face in faces:
            box = (face.x, face.y, face.x + face.width, face.y + face.height)
            region = working.crop(box).filter(ImageFilter.GaussianBlur(radius=blur_radius))
            working.paste(region, box)

        output = io.BytesIO()
        working.save(output, format="PNG")
        return output.getvalue(), faces
