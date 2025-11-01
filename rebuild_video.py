import cv2
import numpy as np
import os
from tqdm import tqdm

def write_video(frame_seq, output_path):
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

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    frames_dir = 'frames'
    for new_pos, original_frame_idx in enumerate(tqdm(frame_seq)):
        frame_file = f'frames/frame_{original_frame_idx:04d}.png'
        frame = cv2.imread(frame_file)
        if frame is None:
            print(f"Warning: Could not read frame {original_frame_idx}")
            continue
        if frame.shape[1] != width or frame.shape[0] != height:
            frame = cv2.resize(frame, (width, height))
        out.write(frame)
    out.release()
    print(f"\n✅ Video written to {output_path}")

print("🎬 Rebuilding videos with both frame orders...")

orig = np.load('frame_sequence.npy').astype(int)
rev = orig[::-1]

write_video(orig, "reconstructed_video_orig.mp4")
write_video(rev,  "reconstructed_video_reversed.mp4")
