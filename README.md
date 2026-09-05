# HH Goa Task 3 - Face Search & Blockchain Verification

A Python-based pipeline that takes an input image, detects and encodes a face, performs a genuine reverse image search using Google Lens through SerpApi, finds a matching social-media result, and stores a SHA-256 fingerprint of the result in a local simulated blockchain for later verification.

## Features

- Face detection using OpenCV YuNet
- Face alignment and 128-dimensional face feature encoding using OpenCV SFace
- Genuine reverse image search using Google Lens via SerpApi
- Dynamic discovery of social-media results
- SHA-256 fingerprint generation
- Local simulated blockchain with hash-linked blocks
- Full blockchain chain integrity verification
- Fingerprint re-verification against the stored record
- End-to-end command-line pipeline

## Pipeline

Input Image
|
v
Face Detection
|
v
Face Alignment
|
v
128-D Face Encoding
|
+----------------------+
|                      |
v                      v
Google Lens       Face Features
via SerpApi
|
v
Social Media Match
|
v
SHA-256 Fingerprint
|
v
Local Simulated Blockchain
|
v
Blockchain Integrity Check
|
v
Fingerprint Re-verification
|
v
VERIFIED

## How It Works

### 1. Face Identification

The input image is processed using OpenCV's YuNet face detector.

After detecting the face, OpenCV SFace is used to:

- Align the detected face
- Generate a 128-dimensional face feature representation

The face encoding is used as a feature representation. This project does not maintain a database of known people and does not perform name-based identity classification.

### 2. Genuine Web / Social-Media Search

The original input image is uploaded to SerpApi and searched through Google Lens.

The returned results are processed dynamically to locate a supported social-media result.

Supported platforms currently include:

- Instagram
- TikTok
- Facebook
- YouTube

The project does not contain a hardcoded social-media post or pre-selected result.

### 3. Blockchain Verification

Once a social-media result is found, selected result metadata is converted into a canonical JSON representation.

A SHA-256 fingerprint is generated from:

- Platform
- Title
- URL
- Snippet

The fingerprint and social-media metadata are stored inside a local simulated blockchain.

Each block contains:

- Block index
- Timestamp
- Data
- Previous block hash
- Current block hash

The current block hash is calculated using SHA-256.

### 4. Re-verification

The blockchain chain is checked from the first block through the latest block.

For each block, the system verifies:

- Block index
- Block hash
- Connection to the previous block
- Genesis block previous hash

The social-media result is also fingerprinted again and compared with the fingerprint stored in the blockchain record.

If both checks succeed, the pipeline reports:

VERIFIED [OK]

## Technologies Used

- Python
- OpenCV
- OpenCV YuNet
- OpenCV SFace
- SerpApi
- Google Lens
- SHA-256
- JSON
- python-dotenv

## Project Structure

```text
HHGoa_Task-03/
|
+-- input/
|   +-- test_image.jpg
|
+-- models/
|   +-- face_detection_yunet_2026may.onnx
|   +-- face_recognition_sface_2021dec.onnx
|
+-- src/
|   +-- face.py
|   +-- reverse_search.py
|   +-- blockchain.py
|   +-- main.py
|
+-- .env
+-- .gitignore
+-- requirements.txt
+-- README.md
Note: .env and blockchain.json are local files and are excluded from Git using .gitignore.

Requirements
Python 3.14 or compatible Python version
Internet connection
SerpApi API key
Installation

Open a terminal in the project directory and install the required packages:

python -m pip install -r requirements.txt
API Key Setup

Create a .env file in the project root:

SERPAPI_KEY=your_serpapi_api_key

The .env file is excluded from Git using .gitignore.

Do not commit or share your API key.

Running the Project

Run the complete pipeline from the project root:

python src\main.py input\test_image.jpg

The pipeline performs:

Face Detection
Face Encoding
Google Lens Reverse Search
Social-Media Match
SHA-256 Fingerprint
Blockchain Storage
Blockchain Verification
Fingerprint Re-verification
Example Output
========================================
       HH GOA TASK 3 PIPELINE
========================================

[1] FACE IDENTIFICATION
----------------------------------------
Face detection : SUCCESS [OK]
Face encoding  : SUCCESS [OK]
Encoding size  : 128 values

[2] WEB / SOCIAL MEDIA SEARCH
----------------------------------------
Social-media match : FOUND [OK]
Platform : Instagram

[3] BLOCKCHAIN VERIFICATION
----------------------------------------
Fingerprint created [OK]
Block index : 0
Block hash  : <generated hash>

[4] VERIFYING BLOCKCHAIN
----------------------------------------
Blockchain integrity : VALID [OK]

[5] RE-VERIFYING DATA
----------------------------------------
Fingerprint match : MATCH [OK]

========================================
             VERIFIED [OK]
========================================
The exact social-media result, block index, timestamp, and hash will vary between runs.

Blockchain Implementation

This project uses a local simulated blockchain.

It does not currently use Ethereum, Polygon, Solana, or another public blockchain network.

The local blockchain is implemented using JSON storage, SHA-256 hashing, and hash-linked blocks.

A simplified block structure is:
{
  "index": 0,
  "timestamp": "generated at runtime",
  "data": {
    "fingerprint": "SHA-256 fingerprint",
    "social_media": {
      "platform": "Instagram",
      "title": "result title",
      "url": "result URL",
      "snippet": "result snippet"
    }
  },
  "previous_hash": "0",
  "hash": "SHA-256 block hash"
}
A subsequent block references the hash of the previous block through previous_hash.

Verification Model

Two levels of verification are performed.

Blockchain Integrity

The entire local blockchain is traversed from the first block to the latest block.

For each block, the system verifies that:

The block index is correct.
The stored block hash matches a newly calculated hash.
The previous hash matches the hash of the preceding block.
The first block has a previous hash value of 0.

If the chain is valid:
Blockchain chain integrity: VALID [OK]
If the chain has been modified:

Blockchain chain integrity: INVALID [FAIL]
Fingerprint Verification

The social-media result is fingerprinted again using the same canonical representation.

The new fingerprint is compared with the fingerprint stored in the blockchain record.

A match produces:

Fingerprint match : MATCH
Limitations
The blockchain is a local simulated blockchain, not a public blockchain network.
Google Lens results depend on external search availability and may change over time.
SerpApi requires an API key and is subject to its API limits.
A social-media result may not always be available for every input image.
The current implementation selects the first supported social-media result returned by the search results.
Face encoding represents facial features but does not by itself identify a person's name.
The reverse image search and face encoding are separate processing stages.
The blockchain stores a fingerprint and selected metadata rather than the original social-media post itself.
The system is intended as a demonstration of the requested pipeline and is not a production identity-verification system.
Privacy and Responsible Use

Use images that you have permission to process or that are appropriate for public reverse-image-search testing.

Do not use sensitive identity documents or private images without appropriate authorization.

This project should not be treated as proof of a person's real-world identity. A reverse-image-search match indicates that a visually related result was found on the web; it does not independently establish identity.

Model Sources

The face detection and face recognition models are from the OpenCV Zoo model collection.

YuNet face detection
SFace face recognition

The project uses the downloaded ONNX model files included in the models/ directory.

Task 3 Compliance

This implementation addresses the requested Task 3 pipeline:
| Requirement               | Implementation                                           |
| ------------------------- | -------------------------------------------------------- |
| Face identification       | YuNet detection + SFace 128-D encoding                   |
| Genuine web/social search | Google Lens through SerpApi                              |
| Dynamic result discovery  | Social-media result extracted from live search results   |
| Blockchain verification   | SHA-256 fingerprint stored in local simulated blockchain |
| Re-verification           | Block hash, chain, and fingerprint verification          |
| GitHub submission         | Source code + README                                     |
License

This project was created as a hackathon submission and demonstration project.
