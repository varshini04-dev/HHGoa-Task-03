import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import serpapi


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise RuntimeError("SERPAPI_KEY not found in .env file")


# --------------------------------------------------
# REVERSE IMAGE SEARCH
# --------------------------------------------------

def reverse_search(image_path):
    """
    Upload the input image and perform a genuine
    Google Lens reverse-image search through SerpApi.
    """

    print("[1] Uploading image to SerpApi...")

    client = serpapi.Client(api_key=API_KEY)

    upload = client.upload_image(str(image_path))

    if "error" in upload:
        raise RuntimeError(
            f"Image upload failed: {upload['error']}"
        )

    if "image_id" not in upload:
        raise RuntimeError(
            "Image upload succeeded but no image_id was returned."
        )

    image_id = upload["image_id"]

    print("[2] Image uploaded successfully.")
    print("[3] Searching Google Lens...")

    results = client.search({
        "engine": "google_lens",
        "image_id": image_id
    })
    if hasattr(results, "get"):
        if results.get("error"):
            raise RuntimeError(
                f"Google Lens search failed: {results['error']}"
            )

    print("[4] Google Lens search completed.")

    return results
    


# --------------------------------------------------
# SOCIAL-MEDIA RESULT EXTRACTION
# --------------------------------------------------

def detect_platform(link, source):
    """
    Identify supported social-media platforms from
    a search result's URL or source.
    """

    link_lower = link.lower()
    source_lower = source.lower()

    if "instagram.com" in link_lower or "instagram" in source_lower:
        return "Instagram"

    if "tiktok.com" in link_lower or "tiktok" in source_lower:
        return "TikTok"

    if "facebook.com" in link_lower or "facebook" in source_lower:
        return "Facebook"

    if "youtube.com" in link_lower or "youtube" in source_lower:
        return "YouTube"

    return None


def extract_social_result(results):
    """
    Find a social-media result dynamically from
    Google Lens results.
    """

    # --------------------------------------------------
    # CHECK ORGANIC RESULTS
    # --------------------------------------------------

    for item in results.get("organic_results", []):

        link = item.get("link", "")
        source = item.get("source", "")

        if not link:
            continue

        social_platform = detect_platform(link, source)

        if social_platform:
            return {
                "platform": social_platform,
                "title": item.get("title", ""),
                "url": link,
                "snippet": item.get("snippet", ""),
                "type": "organic_result"
            }

    # --------------------------------------------------
    # CHECK SHORT VIDEOS
    # --------------------------------------------------

    for item in results.get("short_videos", []):

        link = item.get("link", "")
        source = item.get("source", "")

        if not link:
            continue

        social_platform = detect_platform(link, source)

        if social_platform:
            return {
                "platform": social_platform,
                "title": item.get("title", ""),
                "url": link,
                "snippet": item.get("snippet", ""),
                "type": "short_video"
            }

    return None


# --------------------------------------------------
# COMMAND-LINE TEST
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python src\\reverse_search.py input\\test_image.jpg")
        sys.exit(1)

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        print(f"ERROR: Image not found: {image_path}")
        sys.exit(1)

    try:

        results = reverse_search(image_path)

        social_result = extract_social_result(results)

        print("\n========================================")
        print("      SOCIAL MEDIA MATCH")
        print("========================================")

        if social_result:

            print(
                f"Platform : "
                f"{social_result['platform']}"
            )

            print(
                f"Title    : "
                f"{social_result['title']}"
            )

            print(
                f"URL      : "
                f"{social_result['url']}"
            )

            if social_result["snippet"]:
                print(
                    f"Snippet  : "
                    f"{social_result['snippet']}"
                )

            print(
                f"Type     : "
                f"{social_result['type']}"
            )

            print("\n[5] Social-media match found [OK]")

        else:

            print("No suitable social-media result found.")
            print("\n[5] Social-media match not found [FAIL]")

    except Exception as error:

        print("\nERROR:")
        print(error)
        sys.exit(1)