# train_dqn.py

import torch
import torch.optim as optim
import numpy as np
import time
import random
from replay_buffer import ReplayBuffer
from dqn_network import DQN
from flying_bird_env import FlyingBirdEnv
from visualize import plot_rewards, plot_losses
import config

# Hyperparameters
GAMMA = 0.99  # Discount factor
EPSILON_START = 1.0  # Initial epsilon for exploration
EPSILON_END = 0.01  # Final epsilon after decay
EPSILON_DECAY = 500  # Number of steps for epsilon to decay
BATCH_SIZE = 64  # Size of mini-batches for training
BUFFER_SIZE = 10000  # Max size of the replay buffer
LEARNING_RATE = 0.0005  # Learning rate for the DQN
TARGET_UPDATE = 100  # How often to update the target network
MAX_EPISODES = 10000  # Total number of episodes for training

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def epsilon_by_frame(frame_idx):
    """Decay epsilon over time"""
    return EPSILON_END + (EPSILON_START - EPSILON_END) * np.exp(-1. * frame_idx / EPSILON_DECAY)

def compute_td_loss(batch, model, target_model, optimizer):
    """Compute the loss between predicted and target Q-values"""
    states, actions, rewards, next_states, dones = batch
    states = torch.FloatTensor(states).to(device)
    next_states = torch.FloatTensor(next_states).to(device)
    actions = torch.LongTensor(actions).to(device)
    rewards = torch.FloatTensor(rewards).to(device)
    dones = torch.FloatTensor(dones).to(device)

    # Get the Q-values for the actions taken
    q_values = model(states)
    next_q_values = target_model(next_states)

    q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
    next_q_value = next_q_values.max(1)[0]
    expected_q_value = rewards + GAMMA * next_q_value * (1 - dones)

    # Loss function: Mean Squared Error (MSE)
    loss = (q_value - expected_q_value.detach()).pow(2).mean()

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss

def train():
    """Main DQN training loop"""
    env = FlyingBirdEnv(render=False)
    replay_buffer = ReplayBuffer(BUFFER_SIZE)

    model = DQN(env.observation_space.shape[0], env.action_space.n).to(device)
    target_model = DQN(env.observation_space.shape[0], env.action_space.n).to(device)
    target_model.load_state_dict(model.state_dict())

    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    print("Training started...")

    frame_idx = 0
    all_rewards = []
    cumulative_rewards = []
    losses = []

    for episode in range(MAX_EPISODES):
        state = env.reset()
        episode_reward = 0
        done = False

        while not done:
            # Select action using epsilon-greedy policy
            epsilon = epsilon_by_frame(frame_idx)
            if random.random() > epsilon:
                action = model(torch.FloatTensor(state).to(device)).argmax().item()
            else:
                action = env.action_space.sample()  # Random action (exploration)

            next_state, reward, done, _ = env.step(action)
            replay_buffer.add((state, action, reward, next_state, done))

            state = next_state
            episode_reward += reward
            frame_idx += 1

            if replay_buffer.size() > BATCH_SIZE:
                loss = compute_td_loss(replay_buffer.sample(BATCH_SIZE), model, target_model, optimizer)
                losses.append(loss.item())

            if frame_idx % TARGET_UPDATE == 0:
                target_model.load_state_dict(model.state_dict())

            # Control the step speed during training
            time.sleep(1 / config.FPS_TRAINING)

        all_rewards.append(episode_reward)
        if len(cumulative_rewards) == 0:
            cumulative_rewards.append(episode_reward)
        else:
            cumulative_rewards.append(cumulative_rewards[-1] + episode_reward)

        print(f"Episode {episode}, Reward: {episode_reward}, Cumulative Reward: {cumulative_rewards[-1]}, Epsilon: {epsilon}")

    # Visualize rewards and losses
    plot_rewards(all_rewards, cumulative_rewards)
    plot_losses(losses)
    
    torch.save(model.state_dict(), 'dqn_model.pth')
    model = DQN(env.observation_space.shape[0], env.action_space.n).to(device)
    model.load_state_dict(torch.load('dqn_model.pth'))

    env.close()

if __name__ == "__main__":
    train()