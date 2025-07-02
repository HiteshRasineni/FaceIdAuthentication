# FaceIdAuth

A desktop Face ID authentication system using deep learning(MTCNN & InceptionResNetV1) and computer vision. This project provides a simple GUI for registering, authenticating, viewing, and deleting face IDs using your webcam. It leverages the facenet-pytorch library for face detection and embedding, and stores user embeddings locally.

## Features
- Register your face with your name (Face ID)
- Authenticate using your face and username
- View all registered users
- Delete a registered Face ID
- User-friendly GUI built with Tkinter

## Screenshots
(Add screenshots of the GUI here if available)

## Requirements
- Python 3.7+
- Webcam

### Python Dependencies
- opencv-python
- numpy
- facenet-pytorch
- torch
- pillow

You can install the dependencies with:
```bash
pip install opencv-python numpy facenet-pytorch torch pillow
```

## File Structure
- `faceid_main_gui.py`: Main menu GUI for the Face ID system
- `faceid_register_gui.py`: GUI for registering a new face
- `faceid_authenticate_gui.py`: GUI for authenticating a user
- `data/`: Stores user face embeddings as .pkl files

## Usage
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd FaceIdAuth
   ```
2. **Install dependencies**
   ```bash
   pip install opencv-python numpy facenet-pytorch torch pillow
   ```
3. **Run the main GUI**
   ```bash
   python faceid_main_gui.py
   ```
4. **Register a Face ID**
   - Click "Register Face ID" and follow the instructions.
5. **Authenticate**
   - Click "Authenticate" and show your face to the camera.
6. **View or Delete Users**
   - Use the respective buttons in the main menu.

## Notes
- All face embeddings are stored locally in the `data/` directory as `<username>_embedding.pkl`.
- The system uses your webcam for face capture.
- For best results, ensure good lighting and face visibility during registration.

## License
MIT License (or specify your license here)

## Acknowledgements
- [facenet-pytorch](https://github.com/timesler/facenet-pytorch)
- [PyTorch](https://pytorch.org/)
- [OpenCV](https://opencv.org/) 
