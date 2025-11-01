import numpy as np
from tqdm import tqdm

print("🔄 Loading similarity matrix...")
similarity_matrix = np.load('similarity_matrix.npy')
n_frames = similarity_matrix.shape[0]

print(f"Matrix shape: {similarity_matrix.shape}")
print(f"Statistics: min={similarity_matrix.min():.2f}, max={similarity_matrix.max():.2f}, mean={similarity_matrix.mean():.2f}")

# Find best sequence
print("\n🔗 Finding optimal frame sequence...")

best_sequence = None
best_score = -float('inf')

# Try each frame as starting point
for start_frame in range(n_frames):
    sequence = [start_frame]
    visited = {start_frame}
    current_frame = start_frame
    total_score = 0
    
    # Greedy: always pick next frame with highest similarity
    for step in range(n_frames - 1):
        best_next = -1
        best_sim = -float('inf')
        
        for next_frame in range(n_frames):
            if next_frame not in visited:
                sim = similarity_matrix[current_frame][next_frame]
                if sim > best_sim:
                    best_sim = sim
                    best_next = next_frame
        
        if best_next == -1:
            break
        
        sequence.append(best_next)
        visited.add(best_next)
        total_score += best_sim
        current_frame = best_next
    
    # Keep best sequence
    if len(sequence) == n_frames:
        if total_score > best_score:
            best_score = total_score
            best_sequence = sequence
            print(f"  Start {start_frame}: Score={total_score:.2f}")

print(f"\n✅ Best sequence found: Score={best_score:.2f}")
print(f"First 10: {best_sequence[:10]}")
print(f"Last 10: {best_sequence[-10:]}")

# Save
np.save('frame_sequence.npy', np.array(best_sequence))
np.save('frame_sequence_reversed.npy', np.array(best_sequence[::-1]))

with open('frame_order.txt', 'w') as f:
    f.write("Frame Order Mapping\n")
    f.write("=" * 40 + "\n")
    for new_pos, orig_idx in enumerate(best_sequence):
        f.write(f"{orig_idx:4d} -> {new_pos:4d}\n")

print("✅ Sequence saved!")
