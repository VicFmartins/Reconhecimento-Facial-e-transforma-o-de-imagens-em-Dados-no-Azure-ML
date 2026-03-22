import io

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app, service
from app.vision_service import FaceDetectionResult


client = TestClient(app)


def make_test_image() -> bytes:
    image = Image.new("RGB", (120, 120), color=(240, 240, 240))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_analyze_image_returns_metadata(monkeypatch) -> None:
    monkeypatch.setattr(
        service.detector,
        "detect_faces",
        lambda image: [FaceDetectionResult(x=20, y=20, width=40, height=40)],
    )
    response = client.post(
        "/api/images/analyze",
        files={"file": ("sample.png", make_test_image(), "image/png")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["width"] == 120
    assert data["height"] == 120
    assert data["faces_detected"] == 1
    assert data["face_boxes"][0]["width"] == 40


def test_anonymize_image_returns_png(monkeypatch) -> None:
    monkeypatch.setattr(
        service.detector,
        "detect_faces",
        lambda image: [FaceDetectionResult(x=10, y=10, width=30, height=30)],
    )
    response = client.post(
        "/api/images/anonymize?blur_radius=12",
        files={"file": ("sample.png", make_test_image(), "image/png")},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.headers["x-faces-detected"] == "1"
    assert response.content


def test_analyze_image_without_faces(monkeypatch) -> None:
    monkeypatch.setattr(service.detector, "detect_faces", lambda image: [])
    response = client.post(
        "/api/images/analyze",
        files={"file": ("sample.png", make_test_image(), "image/png")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["faces_detected"] == 0
    assert data["warning"] is None
