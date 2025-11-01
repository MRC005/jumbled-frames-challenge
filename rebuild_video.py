import cv2
import numpy as np
import os
from tqdm import tqdm

print("🎬 Rebuilding video with correct frame order...")

# Load the frame sequence
frame_sequence = np.load('frame_sequence.npy')
frame_sequence = frame_sequence.astype(int)

print(f"Frame sequence: {frame_sequence[:10]}... (showing first 10)")

# Load metadata
metadata = {}
with open('metadata.txt', 'r') as f:
    for line in f:
        key, value = line.strip().split('=')
        if key == 'fps':
            metadata['fps'] = float(value)
        else:
            metadata[key] = int(value)

fps = metadata['fps']
width = metadata['width']
height = metadata['height']

print(f"\nVideo metadata:")
print(f"  FPS: {fps}")
print(f"  Resolution: {width}x{height}")

# Create video writer
output_path = 'reconstructed_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

if not out.isOpened():
    print("❌ Error: Could not open video writer")
    exit(1)

print(f"\n📹 Writing frames to {output_path}...")

# Write frames in correct order
frames_dir = 'frames'
for new_pos, original_frame_idx in enumerate(tqdm(frame_sequence)):
    frame_file = f'frames/frame_{original_frame_idx:04d}.png'
    
    # Read frame
    frame = cv2.imread(frame_file)
    
    if frame is None:
        print(f"Warning: Could not read frame {original_frame_idx}")
        continue
    
    # Ensure frame has correct dimensions
    if frame.shape[1] != width or frame.shape[0] != height:
        frame = cv2.resize(frame, (width, height))
    
    # Write frame
    out.write(frame)

out.release()
print(f"\n✅ Video successfully reconstructed!")
print(f"📁 Output: {output_path}")
