import cv2
import sys
from pathlib import Path


# --------------------------------------------------
# MODEL PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DETECTOR_MODEL = BASE_DIR / "models" / "face_detection_yunet_2026may.onnx"
RECOGNIZER_MODEL = BASE_DIR / "models" / "face_recognition_sface_2021dec.onnx"


def detect_and_encode(image_path):
    """
    Detect a face in the input image and generate
    a 128-dimensional SFace embedding.
    """

    print("[1] Loading input image...")

    image = cv2.imread(str(image_path))

    if image is None:
        raise RuntimeError(f"Could not read image: {image_path}")

    height, width = image.shape[:2]

    print(f"[2] Image loaded: {width}x{height}")

    # --------------------------------------------------
    # FACE DETECTION - YuNet
    # --------------------------------------------------

    detector = cv2.FaceDetectorYN.create(
        str(DETECTOR_MODEL),
        "",
        (width, height),
        0.9,
        0.3,
        5000
    )

    print("[3] Detecting face...")

    _, faces = detector.detect(image)

    if faces is None or len(faces) == 0:
        raise RuntimeError("No face detected in the image.")

    print(f"[4] Face detected [OK] ({len(faces)} face(s))")

    # Use the first detected face
    face = faces[0]

    # --------------------------------------------------
    # FACE RECOGNITION - SFace
    # --------------------------------------------------

    recognizer = cv2.FaceRecognizerSF.create(
        str(RECOGNIZER_MODEL),
        ""
    )

    print("[5] Aligning face...")

    aligned_face = recognizer.alignCrop(image, face)

    print("[6] Generating face encoding...")

    feature = recognizer.feature(aligned_face)

    embedding = feature.flatten()

    print("[7] Face encoding generated [OK]")
    print(f"    Encoding dimensions: {embedding.shape[0]}")

    return {
        "image": image,
        "face": face,
        "embedding": embedding
    }


# --------------------------------------------------
# COMMAND-LINE TEST
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python src\\face.py input\\test_image.jpg")
        sys.exit(1)

    image_path = Path(sys.argv[1])

    try:
        result = detect_and_encode(image_path)

        print("\n========================================")
        print("       FACE IDENTIFICATION")
        print("========================================")

        print("Face detection : SUCCESS [OK]")
        print("Face encoding  : SUCCESS [OK]")
        print(
            f"Encoding size  : "
            f"{len(result['embedding'])} values"
        )

        print("\nFace pipeline completed successfully [OK]")

    except Exception as error:
        print("\nERROR:")
        print(error)
        sys.exit(1)