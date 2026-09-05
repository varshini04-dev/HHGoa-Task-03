import sys
from pathlib import Path

from face import detect_and_encode
from reverse_search import reverse_search, extract_social_result
from blockchain import (
    add_to_blockchain,
    verify_chain,
    verify_fingerprint
)


def main(image_path):
    print("========================================")
    print("       HH GOA TASK 3 PIPELINE")
    print("========================================\n")

    # --------------------------------------------------
    # STEP 1: FACE IDENTIFICATION
    # --------------------------------------------------

    print("[1] FACE IDENTIFICATION")
    print("----------------------------------------")

    face_result = detect_and_encode(image_path)

    print("Face detection : SUCCESS [OK]")
    print("Face encoding  : SUCCESS [OK]")
    print(
        f"Encoding size  : "
        f"{len(face_result['embedding'])} values"
    )

    # --------------------------------------------------
    # STEP 2: GENUINE REVERSE IMAGE SEARCH
    # --------------------------------------------------

    print("\n[2] WEB / SOCIAL MEDIA SEARCH")
    print("----------------------------------------")

    print("Searching Google Lens...")

    results = reverse_search(image_path)

    social_result = extract_social_result(results)

    if not social_result:
        print("Social-media match : NOT FOUND [FAIL]")
        return False

    print("Social-media match : FOUND [OK]")
    print(f"Platform : {social_result['platform']}")
    print(f"Title    : {social_result['title']}")
    print(f"URL      : {social_result['url']}")

    # --------------------------------------------------
    # STEP 3: BLOCKCHAIN FINGERPRINT
    # --------------------------------------------------

    print("\n[3] BLOCKCHAIN VERIFICATION")
    print("----------------------------------------")

    print("Creating SHA-256 fingerprint...")

    block = add_to_blockchain(social_result)

    print("Fingerprint created [OK]")
    print(f"Block index : {block['index']}")
    print(f"Block hash  : {block['hash']}")

    # --------------------------------------------------
    # STEP 4: VERIFY BLOCKCHAIN INTEGRITY
    # --------------------------------------------------

    print("\n[4] VERIFYING BLOCKCHAIN")
    print("----------------------------------------")

    block_valid = verify_chain()
    if not block_valid:
        print("Blockchain integrity : INVALID [FAIL]")
        return False

    print("Blockchain integrity : VALID [OK]")

    # --------------------------------------------------
    # STEP 5: RE-VERIFY FINGERPRINT
    # --------------------------------------------------

    print("\n[5] RE-VERIFYING DATA")
    print("----------------------------------------")

    fingerprint_valid = verify_fingerprint(
        social_result,
        block
    )

    if not fingerprint_valid:
        print("Fingerprint match : MISMATCH [FAIL]")
        return False

    print("Fingerprint match : MATCH [OK]")

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    print("\n========================================")
    print("             VERIFIED [OK]")
    print("========================================")

    return True


# --------------------------------------------------
# COMMAND-LINE ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python src\\main.py input\\test_image.jpg")
        sys.exit(1)

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        print(f"ERROR: Image not found: {image_path}")
        sys.exit(1)

    try:
        success = main(image_path)

        if not success:
            sys.exit(1)

    except Exception as error:
        print("\n========================================")
        print("ERROR")
        print("========================================")
        print(error)
        sys.exit(1)