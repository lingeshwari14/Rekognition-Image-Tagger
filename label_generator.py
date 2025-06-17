import boto3
from PIL import Image, ImageDraw, ImageFont
import io

# Configuration
bucket = 'img-label-generator'
images = ['car.jpg', 'dog.jpg', 'trafficlights.jpg']

# AWS Clients
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

for image_name in images:
    print(f"\n🔍 Processing image: {image_name}")
    output_image_name = f'labeled_{image_name}'

    # Step 1: Detect labels from Rekognition
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': image_name}},
        MaxLabels=10,
        MinConfidence=70
    )

    # Step 2: Download image from S3
    image_obj = s3.get_object(Bucket=bucket, Key=image_name)
    image_bytes = image_obj['Body'].read()
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font = ImageFont.load_default()

    # Step 3: Draw bounding boxes with labels
    for label in response['Labels']:
        for instance in label.get('Instances', []):
            box = instance['BoundingBox']
            left = width * box['Left']
            top = height * box['Top']
            box_width = width * box['Width']
            box_height = height * box['Height']

            draw.rectangle([left, top, left + box_width, top + box_height], outline='red', width=2)
            label_text = f"{label['Name']} ({label['Confidence']:.2f}%)"
            draw.text((left, max(0, top - 10)), label_text, fill='yellow', font=font)

    # Step 4: Draw summary box at top-left
    summary_lines = [f"{label['Name']} - {label['Confidence']:.2f}%" for label in response['Labels']]
    summary_text = "\n".join(summary_lines)
    text_line_height = 12
    text_block_height = len(summary_lines) * text_line_height + 5
    draw.rectangle([(0, 0), (250, text_block_height)], fill='white')
    for idx, line in enumerate(summary_lines):
        draw.text((5, 5 + idx * text_line_height), line, fill='black', font=font)

    # Step 5: Save and upload image
    image.save(output_image_name)
    s3.upload_file(output_image_name, bucket, output_image_name)

    # Make the file public
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=output_image_name)

    print(f"✅ View result: https://{bucket}.s3.amazonaws.com/{output_image_name}")
