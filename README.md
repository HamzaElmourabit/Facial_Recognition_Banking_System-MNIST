# 🏦 Facial Recognition Banking System using MNIST

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![TensorFlow](https://img.shields.io/badge/TensorFlow-DeepLearning-orange?style=for-the-badge&logo=tensorflow)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-MNIST-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

<h3>🔐 AI-Powered Banking Authentication System</h3>

<p>
A smart banking security system using <strong>Facial Recognition</strong>,
<strong>Computer Vision</strong>, and <strong>MNIST Machine Learning Models</strong>.
</p>

</div>

---

# 📌 Table of Contents

- [📖 Introduction](#-introduction)
- [🎯 Objectives](#-objectives)
- [🧠 About MNIST](#-about-mnist)
- [🚀 Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [⚙️ Technologies Used](#️-technologies-used)
- [📂 Project Structure](#-project-structure)
- [🔄 Workflow](#-workflow)
- [⚙️ Installation](#️-installation)
- [▶️ Usage](#️-usage)
- [🧠 Machine Learning Pipeline](#-machine-learning-pipeline)
- [📸 Screenshots](#-screenshots)
- [🔐 Security Advantages](#-security-advantages)
- [📊 Future Improvements](#-future-improvements)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

# 📖 Introduction

The **Facial Recognition Banking System** is an artificial intelligence project designed to improve banking authentication security using:

- 👁️ Facial Recognition
- 🧠 Machine Learning
- 📷 Computer Vision
- 🔐 Biometric Authentication

Traditional banking systems rely heavily on passwords and PIN codes, which are vulnerable to:

- Password theft
- Phishing attacks
- Identity fraud
- Unauthorized access

This project introduces a smarter authentication mechanism based on **face recognition technology** integrated with machine learning models trained using the **MNIST dataset**.

---

# 🎯 Objectives

The main objectives of this project are:

✅ Build a secure banking authentication system  
✅ Implement real-time face recognition  
✅ Use machine learning for identity verification  
✅ Integrate OpenCV for image processing  
✅ Improve authentication speed and reliability  
✅ Reduce risks of identity theft and fraud  

---

# 🧠 About MNIST

## What is MNIST?

The **MNIST dataset** is one of the most famous datasets in Machine Learning and Computer Vision.

It contains:

- 70,000 grayscale images
- Handwritten digits from 0 to 9
- 28x28 pixel images

The dataset is commonly used for:

- Machine learning training
- Image classification
- Pattern recognition
- Neural network benchmarking

---

## Why MNIST in this Project?

MNIST is used in this project to:

- Train machine learning models
- Learn image feature extraction
- Understand recognition pipelines
- Build prediction systems

Even though the project focuses on facial recognition, MNIST concepts help implement and test classification algorithms effectively.

---

# 🚀 Features

## 🔐 Authentication Features

✅ Facial recognition login  
✅ User verification  
✅ Real-time camera capture  
✅ Identity authentication  
✅ Access control system  

---

## 🧠 Machine Learning Features

✅ MNIST dataset integration  
✅ Image preprocessing  
✅ Model training  
✅ Prediction and classification  
✅ Feature extraction  

---

## 👁️ Computer Vision Features

✅ Face detection with OpenCV  
✅ Grayscale conversion  
✅ Image normalization  
✅ Face cropping  
✅ Camera integration  

---

# 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      User Camera     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Face Detection    │
                    │       OpenCV         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Image Preprocessing │
                    │ Resize • Normalize   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  MNIST ML Model      │
                    │ Classification Layer │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
         ┌────────────────┐      ┌────────────────┐
         │ Authorized User│      │ Unknown Person │
         └────────────────┘      └────────────────┘
```

---

# ⚙️ Technologies Used

| Technology | Description |
|---|---|
| Python | Main programming language |
| OpenCV | Face detection and computer vision |
| NumPy | Numerical operations |
| TensorFlow / Keras | Deep learning framework |
| MNIST Dataset | ML training dataset |
| Scikit-learn | Machine learning algorithms |
| Tkinter | Graphical User Interface |
| Haar Cascades | Face detection model |

---

# 📂 Project Structure

```bash
Facial_Recognition_Banking_System-MNIST/
│
├── dataset/
│   ├── mnist/
│   └── faces/
│
├── models/
│   ├── trained_model.h5
│   └── classifier.pkl
│
├── images/
│   ├── screenshots/
│   └── samples/
│
├── src/
│   ├── train.py
│   ├── recognize.py
│   ├── preprocess.py
│   ├── detect_face.py
│   └── main.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🔄 Workflow

## Step 1 — User Registration

The user registers into the system using facial images.

---

## Step 2 — Face Detection

OpenCV detects the face using Haar Cascade classifiers.

---

## Step 3 — Image Processing

The system:

- Converts image to grayscale
- Resizes the image
- Normalizes pixel values
- Extracts important features

---

## Step 4 — Model Prediction

The machine learning model compares the captured image with trained data.

---

## Step 5 — Authentication

The system decides whether access should be:

✅ Granted  
❌ Denied  

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/HamzaElmourabit/Facial_Recognition_Banking_System-MNIST.git
```

---

## 2️⃣ Navigate into Project

```bash
cd Facial_Recognition_Banking_System-MNIST
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

## Run Main Application

```bash
python main.py
```

---

## Train the Model

```bash
python train.py
```

---

## Start Recognition System

```bash
python recognize.py
```

---

# 🧠 Machine Learning Pipeline

## 📥 Data Collection

- Capture facial images
- Import MNIST dataset
- Organize training samples

---

## 🧹 Data Preprocessing

- Resize images
- Normalize data
- Convert grayscale
- Remove noise

---

## 🏋️ Model Training

The ML model learns patterns and facial features from training data.

---

## 🔍 Prediction

The trained model predicts user identity from real-time images.

---

# 📸 Screenshots

## 🔐 Login Interface

```text
[ Add login interface screenshot ]
```

---

## 👁️ Face Detection

```text
[ Add face detection screenshot ]
```

---

## 🧠 Model Prediction

```text
[ Add prediction result screenshot ]
```

---

# 🔐 Security Advantages

✅ Biometric authentication  
✅ Reduced password dependency  
✅ Faster authentication  
✅ Improved banking security  
✅ Fraud prevention  
✅ Better user experience  

---

# 📊 Future Improvements

## 🚀 Planned Enhancements

- CNN Deep Learning integration
- FaceNet implementation
- Database connectivity
- Multi-user management
- Mobile banking application
- Cloud deployment
- Anti-spoofing system
- Liveness detection
- Real-time analytics dashboard

---

# 🤝 Contributing

Contributions are welcome!

## Steps

### 1️⃣ Fork Repository

```bash
git fork
```

### 2️⃣ Create Feature Branch

```bash
git checkout -b feature/NewFeature
```

### 3️⃣ Commit Changes

```bash
git commit -m "Add new feature"
```

### 4️⃣ Push Changes

```bash
git push origin feature/NewFeature
```

### 5️⃣ Open Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## Hamza Elmourabit

📌 GitHub Repository:

https://github.com/HamzaElmourabit/Facial_Recognition_Banking_System-MNIST

---

# ⭐ Support

If you like this project:

⭐ Star the repository  
🍴 Fork the project  
🛠️ Contribute to improve it  

---

# 📚 References

- OpenCV Documentation
- TensorFlow Documentation
- MNIST Dataset
- Machine Learning Concepts
- Computer Vision Research Papers

---

#  Final Note

This project demonstrates how Artificial Intelligence and Computer Vision can be integrated into banking systems to create secure, modern, and intelligent authentication solutions.

The combination of:

- Facial Recognition
- Machine Learning
- OpenCV
- MNIST Concepts

creates a strong foundation for future AI-powered banking applications.

---
