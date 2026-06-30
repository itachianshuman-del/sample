# 07 · Computer Vision

> Teaching machines to see — classify, detect, segment, and understand images and
> video. One of deep learning's biggest success stories.

---

## 📌 What it is & why it matters

Computer vision (CV) extracts meaning from images and video: "what's in this
image?", "where is it?", "track it across frames." It powers self-driving,
medical imaging, manufacturing QA, retail analytics, sports analytics, and
document understanding. Modern CV is dominated by deep learning (CNNs and, increasingly,
vision transformers).

---

## 🧠 Core concepts

- **Image basics:** pixels, channels, resolution, normalization, augmentation.
- **CNNs:** convolution, pooling, filters/feature maps, why they exploit spatial
  structure.
- **Core tasks:** image **classification**, **object detection** (bounding boxes),
  **segmentation** (per-pixel), keypoint/pose estimation, tracking.
- **Transfer learning** — fine-tune pretrained backbones (ResNet, EfficientNet,
  ViT) instead of training from scratch.
- **Modern architectures:** YOLO family (real-time detection), Vision
  Transformers (ViT), Segment Anything (SAM).
- **Evaluation:** accuracy/top-k (classification), **mAP/IoU** (detection),
  Dice/IoU (segmentation).

---

## 📚 Best resources

### Courses
- **Stanford CS231n — Deep Learning for Computer Vision** (the canonical course,
  free materials): https://cs231n.stanford.edu/
- **fast.ai** — practical vision with transfer learning: https://course.fast.ai/
- **PyImageSearch** — practical OpenCV + DL tutorials: https://pyimagesearch.com/

### Tools & hands-on
- **Ultralytics YOLO** (real-time detection/segmentation, very easy API):
  https://github.com/ultralytics/ultralytics
- **Roboflow** — dataset labeling/management + tutorials: https://roboflow.com/
- **OpenCV** (classic CV ops): https://opencv.org/
- **Hugging Face — vision models & course** content.

### Example project repos
- **abdullahtarek/tennis_analysis** — detect players & ball with YOLO + CNN
  keypoints (great portfolio project): https://github.com/abdullahtarek/tennis_analysis

---

## 💻 Code example

```python
# Real-time object detection in ~4 lines with Ultralytics YOLO.
from ultralytics import YOLO

model = YOLO("yolov8n.pt")               # tiny pretrained model (auto-downloads)
results = model("street.jpg")            # run detection on an image

for box in results[0].boxes:
    cls = model.names[int(box.cls)]      # class name, e.g. "person", "car"
    conf = float(box.conf)               # confidence
    xyxy = box.xyxy[0].tolist()          # [x1, y1, x2, y2] bounding box
    print(f"{cls}: {conf:.2f} @ {[round(v) for v in xyxy]}")

# Fine-tune on YOUR dataset (data.yaml points to labeled images):
# model.train(data="data.yaml", epochs=50, imgsz=640)
```

---

## 🌍 Real-world use cases

- **Manufacturing QA** — defect detection on production lines.
- **Medical imaging** — tumor detection, X-ray/CT analysis (assistive).
- **Retail** — shelf monitoring, footfall analytics, checkout-free stores.
- **Sports analytics** — player/ball tracking, pose estimation.
- **Document AI** — OCR, layout understanding, table extraction.

---

## 🛠️ Hands-on project ideas

1. **Image classifier** with transfer learning (e.g., classify your own photos).
2. **Custom object detector** with YOLO on a Roboflow-labeled dataset.
3. Recreate the **tennis/football analysis** project (detection + tracking + stats).

---

## 🗺️ Suggested learning path

1. Image basics & OpenCV → 2. CNNs (CS231n) → 3. Transfer learning for
classification → 4. Object detection with YOLO → 5. Segmentation → 6. A real
project (detection + tracking).
