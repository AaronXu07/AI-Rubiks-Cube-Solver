import matplotlib.pyplot as plt

plt.ion()  # Turn on interactive mode

def plot(scores, mean_scores):
    plt.clf()  # Clear the current figure
    plt.title('Training Progress')
    plt.xlabel('Episode')
    plt.ylabel('Score (%)')
    plt.plot(scores, label='Rolling Avg (Last 100)')
    plt.plot(mean_scores, label='Cumulative Mean')
    plt.ylim(ymin=0)
    
    # Add text labels for last values
    if len(scores) > 0:
        plt.text(len(scores)-1, scores[-1], f'{scores[-1]:.1f}')
    if len(mean_scores) > 0:
        plt.text(len(mean_scores)-1, mean_scores[-1], f'{mean_scores[-1]:.1f}')
    
    plt.legend()
    plt.pause(0.001)  # Pause to update the plot
