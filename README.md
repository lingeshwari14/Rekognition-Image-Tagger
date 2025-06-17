# Rekognition-Image-Tagger

This project is a Python-based tool that uses **Amazon Rekognition** to automatically analyze images stored in **Amazon S3**, detect objects and scenes, and draw bounding boxes around them with confidence scores. It then uploads the labeled image back to S3 with public access.

---

## 🚀 Features

- ✅ Detects up to 10 labels per image using Amazon Rekognition.
- ✅ Draws bounding boxes and confidence scores on detected objects.
- ✅ Uploads the annotated image back to S3.
- ✅ Automatically makes output image public for easy viewing.
- ✅ Python script powered with `boto3`, `Pillow`, and AWS CLI access.

---

## 📌 Architecture

```plaintext
1. Upload image to S3 bucket
2. Use AWS Rekognition to detect labels from the image
3. Download image from S3 and process it
4. Draw bounding boxes and label summaries
5. Save the annotated image locally and upload it back to S3
