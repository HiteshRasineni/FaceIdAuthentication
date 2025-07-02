import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import pickle
from PIL import Image, ImageTk

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(image_size=160, margin=14, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

username = simpledialog.askstring("Authenticate", "Enter username:")
try:
    with open(f"data/{username}_embedding.pkl", "rb") as f:
        registered_embedding = pickle.load(f)
except FileNotFoundError:
    print("❌ User not found.")
    exit()

root = tk.Tk()
root.title("🔐 Face ID Authentication")
root.geometry("640x550")
root.configure(bg="black")

canvas = tk.Canvas(root, width=480, height=360)
canvas.pack(pady=20)

status_text = tk.Label(root, text="Show your face to authenticate...", font=("Helvetica", 14), fg="white", bg="black")
status_text.pack()

cap = cv2.VideoCapture(0)
authenticated = False

def update_frame():
    global authenticated
    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face = mtcnn(img)

    result = "Face not detected."

    if face is not None:
        with torch.no_grad():
            emb = resnet(face.unsqueeze(0).to(device)).cpu().numpy()[0]
        sim = cosine_similarity(emb, registered_embedding)
        if sim > 0.85:
            result = f"✅ Authenticated: {username}"
            authenticated = True
        else:
            result = "❌ Access Denied"

    img_resized = cv2.resize(img, (480, 360))
    img_pil = Image.fromarray(img_resized)
    draw = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor=tk.NW, image=draw)
    canvas.image = draw

    status_text.config(text=result)

    if not authenticated:
        root.after(30, update_frame)
    else:
        cap.release()

update_frame()
root.mainloop()
