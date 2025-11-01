import numpy as np
from tqdm import tqdm

print("🔄 Loading similarity matrix...")
similarity_matrix = np.load('similarity_matrix.npy')
n_frames = similarity_matrix.shape[0]

print(f"Matrix shape: {similarity_matrix.shape}")
print(f"Total frames: {n_frames}")

# Find the best sequence using greedy approach
print("\n🔗 Finding optimal frame sequence...")

# Try multiple starting points and pick the best sequence
best_sequence = None
best_score = -float('inf')

for start_frame in range(min(10, n_frames)):  # Try first 10 frames as start
    sequence = [start_frame]
    visited = {start_frame}
    
    current_frame = start_frame
    total_similarity = 0
    
    # Build sequence greedily
    for step in range(n_frames - 1):
        # Find unvisited frame with highest similarity to current frame
        best_next_frame = -1
        best_similarity = -1
        
        for next_frame in range(n_frames):
            if next_frame not in visited:
                sim = similarity_matrix[current_frame][next_frame]
                if sim > best_similarity:
                    best_similarity = sim
                    best_next_frame = next_frame
        
        if best_next_frame == -1:
            # No more frames to visit
            break
        
        sequence.append(best_next_frame)
        visited.add(best_next_frame)
        total_similarity += best_similarity
        current_frame = best_next_frame
    
    # Check if this is a complete sequence
    if len(sequence) == n_frames and total_similarity > best_score:
        best_score = total_similarity
        best_sequence = sequence
        print(f"  Start frame {start_frame}: Score = {total_similarity:.2f}")

print(f"\n✅ Best sequence found with score: {best_score:.2f}")
print(f"Sequence (first 20 frames): {best_sequence[:20]}")

# Save the sequence
np.save('frame_sequence.npy', np.array(best_sequence))
print("💾 Saved frame sequence")

# Create a mapping file (human readable)
with open('frame_order.txt', 'w') as f:
    f.write("Original Frame Index -> New Position\n")
    f.write("=" * 40 + "\n")
    for new_pos, original_idx in enumerate(best_sequence):
        f.write(f"{original_idx:4d} -> {new_pos:4d}\n")

print("📄 Saved frame order mapping to frame_order.txt")
