import matplotlib.pyplot as plt

plt.ion()  # Turn on interactive mode

def plot(scores, mean_scores):
    plt.clf()  # Clear the current figure
    plt.title('Training Progress')
    plt.xlabel('Episode')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Mean Score')
    plt.ylim(ymin=0)
    
    # Add text labels for last values
    if len(scores) > 0:
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    if len(mean_scores) > 0:
        plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    
    plt.legend()
    plt.pause(0.001)  # Pause to update the plot
