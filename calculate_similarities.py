import cv2
import numpy as np
import os
from tqdm import tqdm

print("🔄 Loading frames...")
frames_dir = 'frames'
frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
frames = []

for frame_file in frame_files:
    frame = cv2.imread(os.path.join(frames_dir, frame_file), cv2.IMREAD_GRAYSCALE)
    # Resize for faster processing
    frame = cv2.resize(frame, (240, 135))
    frames.append(frame)

print(f"✅ Loaded {len(frames)} frames")

# Calculate similarity using optical flow
print("\n📊 Calculating similarity scores using optical flow...")

n_frames = len(frames)
similarity_matrix = np.zeros((n_frames, n_frames))

# Optical flow detector
optical_flow = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)

for i in range(n_frames):
    for j in range(n_frames):
        if i == j:
            similarity_matrix[i][j] = 0
            continue
        
        try:
            # Calculate optical flow from frame i to frame j
            flow = optical_flow.calc(frames[i], frames[j], None)
            
            # Calculate flow magnitude (measure of motion)
            magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            
            # Smooth flow = good continuity between frames
            # We want SMALL flow magnitude for consecutive frames
            smooth_score = -np.mean(magnitude)  # Negative because small flow is good
            
            # Also check for correlation
            correlation = np.corrcoef(frames[i].flatten(), frames[j].flatten())[0, 1]
            if np.isnan(correlation):
                correlation = 0
            
            # Combined score: prefer similar frames with smooth motion
            similarity_matrix[i][j] = correlation * 100 + smooth_score
            
        except:
            similarity_matrix[i][j] = -1000
    
    if (i + 1) % 50 == 0:
        print(f"  Processed {i+1} frames...")

print(f"✅ Similarity matrix computed using optical flow")

# Save the matrix
np.save('similarity_matrix.npy', similarity_matrix)
print("💾 Saved similarity matrix")
