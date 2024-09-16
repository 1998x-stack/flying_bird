# visualize.py
import matplotlib.pyplot as plt

def plot_rewards(all_rewards, cumulative_rewards):
    """Plot both rewards per episode and cumulative rewards over episodes"""
    plt.figure(figsize=(12, 6))

    # Plot rewards per episode
    plt.subplot(1, 2, 1)
    plt.plot(all_rewards, label="Rewards Per Episode")
    plt.title("Rewards Per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.legend()

    # Plot cumulative rewards
    plt.subplot(1, 2, 2)
    plt.plot(cumulative_rewards, label="Cumulative Rewards", color='green')
    plt.title("Cumulative Rewards")
    plt.xlabel("Episode")
    plt.ylabel("Cumulative Reward")
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_losses(losses):
    """Plot the loss over time (training steps)"""
    plt.figure(figsize=(12, 6))
    plt.plot(losses, label="Loss")
    plt.title("Loss Per Training Step")
    plt.xlabel("Training Step")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()