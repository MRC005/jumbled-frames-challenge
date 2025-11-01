# Jumbled Frames Reconstruction Challenge

## 🎯 Overview
Reconstruction of a 10-second video (300 frames) that have been randomly jumbled. Using SIFT feature matching and greedy algorithm to restore correct frame sequence.

## 🔧 Challenge Details
- **Video**: 1080p, 30 FPS, 10 seconds (300 frames total)
- **Problem**: Frames are in random order
- **Goal**: Find correct sequential order and rebuild video
- **Evaluation**: Frame similarity, execution speed, code quality

## 📊 Algorithm

### 1. Frame Extraction
- Extract all 300 frames from MP4 video
- Store as individual PNG files
- Preserve video metadata (FPS, resolution)

### 2. Feature Detection (SIFT)
- Scale-Invariant Feature Transform detects distinctive keypoints
- Each frame analyzed for unique features
- Features are rotation and scale invariant

### 3. Similarity Matching
- FLANN (Fast Approximate Nearest Neighbors) matcher
- Compare keypoint descriptors between frame pairs
- Lowe's Ratio Test (0.7 threshold) filters weak matches
- Similarity = number of good feature matches

### 4. Sequence Reconstruction
- Build similarity matrix for all frame pairs
- Greedy algorithm: find best next frame at each step
- Try multiple starting points for robustness
- Select sequence with highest total similarity score

### 5. Video Rebuild
- Read frames in correct order
- Write to MP4 with original properties
- Output: `reconstructed_video.mp4`

## 🚀 Quick Start

### Prerequisites


