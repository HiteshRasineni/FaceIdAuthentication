import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import os, pickle
from PIL import Image, ImageTk

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(image_size=160, margin=14, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

TARGET_COUNT = 100
collected_embeddings = []
frame_count = 0

root = tk.Tk()
root.title("🧠 Face ID Registration")
root.geometry("640x550")
root.configure(bg="black")

canvas = tk.Canvas(root, width=480, height=360)
canvas.pack(pady=20)

status_text = tk.Label(root, text="Look straight and rotate your head...", font=("Helvetica", 14), fg="white", bg="black")
status_text.pack()

cap = cv2.VideoCapture(0)

def update_frame():
    global frame_count

    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face = mtcnn(img)

    if face is not None and frame_count < TARGET_COUNT:
        with torch.no_grad():
            emb = resnet(face.unsqueeze(0).to(device))
        collected_embeddings.append(emb.squeeze(0).cpu().numpy())
        frame_count += 1

    img_resized = cv2.resize(img, (480, 360))
    img_pil = Image.fromarray(img_resized)
    draw = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor=tk.NW, image=draw)
    canvas.image = draw

    if frame_count >= TARGET_COUNT:
        cap.release()
        finish_registration()
    else:
        status_text.config(text=f"Capturing... {frame_count}/{TARGET_COUNT}")
        root.after(30, update_frame)

def finish_registration():
    username = simpledialog.askstring("Face ID Setup", "Enter your name:")
    embedding_array = np.stack(collected_embeddings)
    mean_embedding = np.mean(embedding_array, axis=0)
    os.makedirs("data", exist_ok=True)
    with open(f"data/{username}_embedding.pkl", "wb") as f:
        pickle.dump(mean_embedding, f)
    status_text.config(text=f"✅ Face ID saved for: {username}")

update_frame()
root.mainloop()