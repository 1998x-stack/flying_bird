# replay_buffer.py
import random
import numpy as np
from collections import deque

class ReplayBuffer:
    def __init__(self, max_size: int):
        """Initialize the Replay Buffer with a max size"""
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        """Add a new experience to the buffer"""
        self.buffer.append(experience)

    def sample(self, batch_size: int):
        """Sample a batch of experiences from the buffer"""
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        batch = [self.buffer[idx] for idx in indices]
        return map(np.array, zip(*batch))  # returns tuple of (states, actions, rewards, next_states, dones)

    def size(self):
        """Return the current size of the buffer"""
        return len(self.buffer)