import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BLOCKCHAIN_FILE = BASE_DIR / "blockchain.json"


def create_fingerprint(social_result):
    data = {
        "platform": social_result.get("platform", ""),
        "title": social_result.get("title", ""),
        "url": social_result.get("url", ""),
        "snippet": social_result.get("snippet", ""),
    }

    canonical_data = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    )

    fingerprint = hashlib.sha256(
        canonical_data.encode("utf-8")
    ).hexdigest()

    return fingerprint, data


def calculate_block_hash(block):
    block_data = {
        "index": block["index"],
        "timestamp": block["timestamp"],
        "data": block["data"],
        "previous_hash": block["previous_hash"],
    }

    block_string = json.dumps(
        block_data,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        block_string.encode("utf-8")
    ).hexdigest()


def load_blockchain():
    if not BLOCKCHAIN_FILE.exists():
        return []

    with BLOCKCHAIN_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_blockchain(blockchain):
    with BLOCKCHAIN_FILE.open("w", encoding="utf-8") as file:
        json.dump(blockchain, file, indent=4)


def add_to_blockchain(social_result):
    fingerprint, data = create_fingerprint(social_result)

    blockchain = load_blockchain()

    if blockchain:
        previous_hash = blockchain[-1]["hash"]
        index = blockchain[-1]["index"] + 1
    else:
        previous_hash = "0"
        index = 0

    block = {
        "index": index,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "fingerprint": fingerprint,
            "social_media": data,
        },
        "previous_hash": previous_hash,
    }

    block["hash"] = calculate_block_hash(block)

    blockchain.append(block)
    save_blockchain(blockchain)

    return block


def verify_block(block):
    stored_hash = block["hash"]
    recalculated_hash = calculate_block_hash(block)

    return stored_hash == recalculated_hash


def verify_chain():
    blockchain = load_blockchain()

    if not blockchain:
        return True

    for index, block in enumerate(blockchain):

        # Verify block index
        if block["index"] != index:
            return False

        # Verify the block's own hash
        if not verify_block(block):
            return False

        # Verify connection to the previous block
        if index == 0:
            if block["previous_hash"] != "0":
                return False
        else:
            if block["previous_hash"] != blockchain[index - 1]["hash"]:
                return False

    return True


def verify_fingerprint(social_result, block):
    current_fingerprint, _ = create_fingerprint(social_result)

    stored_fingerprint = block["data"]["fingerprint"]

    return current_fingerprint == stored_fingerprint