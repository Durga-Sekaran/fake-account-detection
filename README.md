# Fake Social Media Account Detection System

This project is a rule-based web application that detects suspicious or fake social
media accounts by analyzing account metadata, bio content, and profile image similarity.

The application is built using Streamlit and provides a clear fake percentage along
with reasons for classification.

---

## Problem Statement
Fake social media accounts are commonly used for spamming, scams, and spreading
misinformation. Manual identification is difficult and time-consuming, making an
automated detection system necessary.

---

## Proposed Solution
We propose a rule-based fake account detection system that evaluates multiple
account features and assigns a risk score.

Based on the score, the system classifies the account as:
- Real
- Suspicious
- Fake

The system also provides clear reasons for why an account is detected as fake.

---

## Features
- Followers–Following ratio analysis
- Account age evaluation
- Post count analysis
- Bio content spam keyword detection
- Profile image similarity detection using perceptual hashing
- Fake percentage and risk level output
- Interactive Streamlit user interface

---

## Technologies Used
- Python
- Streamlit
- NumPy
- Pillow
- ImageHash

---

## How It Works
1. User enters account details such as followers, following, posts, account age, and bio
2. User uploads a profile image
3. Rule-based checks are applied to each feature
4. A risk score is calculated
5. The system outputs:
   - Fake percentage
   - Risk level (LOW / MEDIUM / HIGH)
   - Reasons for detection

---

## Installation & Run
```bash
pip install -r requirements.txt
streamlit run app.py