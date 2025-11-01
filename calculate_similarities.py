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
    # Resize to smaller size for faster processing
    frame = cv2.resize(frame, (240, 135))  # Reduce resolution
    frames.append(frame)

print(f"✅ Loaded {len(frames)} frames")

# Initialize SIFT detector
print("\n🔍 Initializing SIFT feature detector...")
sift = cv2.SIFT_create()

# Extract features from all frames
print("📍 Extracting keypoints and descriptors...")
keypoints = []
descriptors = []

for i, frame in enumerate(tqdm(frames)):
    kp, des = sift.detectAndCompute(frame, None)
    keypoints.append(kp)
    # If no features found, use empty descriptor
    descriptors.append(des if des is not None else np.array([]))

print(f"✅ Extracted features from all frames")

# Calculate similarity between frame pairs
print("\n📊 Calculating similarity scores...")

n_frames = len(frames)
similarity_matrix = np.zeros((n_frames, n_frames))

# FLANN matcher for efficient feature matching
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# Compare each frame with nearby frames
for i in range(n_frames):
    if descriptors[i].size == 0:  # Skip if no features
        continue
    
    for j in range(max(0, i-15), min(n_frames, i+16)):
        if i == j or descriptors[j].size == 0:
            continue
        
        try:
            # KNN match
            matches = flann.knnMatch(descriptors[i], descriptors[j], k=2)
            
            # Apply Lowe's ratio test
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
            
            # Similarity = number of good matches
            similarity_matrix[i][j] = len(good_matches)
        except:
            similarity_matrix[i][j] = 0
    
    if (i + 1) % 50 == 0:
        print(f"  Compared {i+1} frames...")

print(f"✅ Similarity matrix computed")

# Save the matrix
np.save('similarity_matrix.npy', similarity_matrix)
print("💾 Saved similarity matrix")
