import cv2
import os
from tqdm import tqdm

# Create output folder for frames
if not os.path.exists('frames'):
    os.makedirs('frames')

# Open the jumbled video
video_path = 'jumbled_video.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Video Properties:")
print(f"  Total Frames: {total_frames}")
print(f"  FPS: {fps}")
print(f"  Resolution: {width}x{height}")

# Extract all frames
frame_index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Save frame as image
    frame_path = f'frames/frame_{frame_index:04d}.png'
    cv2.imwrite(frame_path, frame)
    
    frame_index += 1
    if frame_index % 50 == 0:
        print(f"Extracted {frame_index} frames...")

cap.release()

print(f"\n✅ Extracted {frame_index} frames successfully!")
print(f"Frames saved in './frames' directory")

# Save metadata for later
with open('metadata.txt', 'w') as f:
    f.write(f"fps={fps}\n")
    f.write(f"width={width}\n")
    f.write(f"height={height}\n")
    f.write(f"total_frames={frame_index}\n")

print("✅ Metadata saved!")
