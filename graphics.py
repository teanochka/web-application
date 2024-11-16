import matplotlib.pyplot as plt

def draw_train_loss(num_epochs, train_losses):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, num_epochs + 1), train_losses, label="Train Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Train Loss over Epochs")
    plt.legend()
    plt.savefig("results/train-loss.png")

def draw_mAP(num_epochs, valid_mAPs):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, num_epochs + 1), valid_mAPs, label="Validation mAP", color="orange")
    plt.xlabel("Epoch")
    plt.ylabel("mAP")
    plt.title("Validation mAP over Epochs")
    plt.legend()
    plt.savefig("results/mAP.png")
