import json
from PIL import Image
import imagehash
from image_utils import image_check

# ---------- LOAD DATASET (RELATIVE PATH) ----------
with open("data/profiles.json", "r") as f:
    dataset = json.load(f)

fake_accounts = [a for a in dataset if a["is_fake"] == 1]

avg_fake_posts = sum(a["posts"] for a in fake_accounts) / len(fake_accounts)

# ---------- LOAD STORED IMAGE HASHES ----------
IMAGE_FOLDER = "images"
stored_hashes = image_check(IMAGE_FOLDER)

# ---------- BIO CHECK ----------
def bio_check(bio):
    if not bio or len(bio.strip()) < 10:
        return 1

    spam_words = ["earn", "free", "click", "money", "work from home", "promo"]
    for word in spam_words:
        if word in bio.lower():
            return 1
    return 0

# ---------- IMAGE SIMILARITY CHECK ----------
def image_similarity(profile_image_path):
    if not profile_image_path:
        return 0, None

    try:
        new_img = Image.open(profile_image_path)
        new_hash = imagehash.phash(new_img)

        for img_name, old_hash in stored_hashes.items():
            if new_hash - old_hash < 8:
                return 1, img_name

    except Exception as e:
        print("Image error:", e)

    return 0, None

def ratio_check(followers, following):
    if followers < 50 and following < 50:
        return 0, None

    if followers < 50 and following > 200:
        return 1, round(followers / following, 2)

    return 0, None

# ---------- MAIN DETECTION ----------
def detect_account(account):
    score = 0
    reasons = []

    if account["posts"] < avg_fake_posts:
        score += 1
        reasons.append("Very low post count")

    if account["account_age_days"] < 30:
        score += 1
        reasons.append("Account is newly created")

    if bio_check(account.get("bio", "")):
        score += 1
        reasons.append("Bio contains spam-like content")

    reused, matched_image = image_similarity(account.get("profile_image"))
    if reused:
        score += 1
        reasons.append(f"Profile picture reused ({matched_image})")

    flag, ratio = ratio_check(account["followers"], account["following"])
    if flag:
        score += 1
        reasons.append(f"Suspicious followers–following ratio ({ratio})")

    fake_percentage = int((score / 5) * 100)

    risk = "HIGH" if fake_percentage >= 70 else "MEDIUM" if fake_percentage >= 40 else "LOW"

    return fake_percentage, risk, reasons