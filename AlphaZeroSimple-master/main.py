import torch

from game import RubiksGame
from model import RubiksModel
from trainer import Trainer


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    args = {
        # batch_size of mcts simulations when training neural nets
        'batch_size': 16,

        # Total number of training iterations
        # (outer loop of episodes, aka number of batches of numEps episodes)
        'numIters': 100,

        # Number of full games (episodes) to run during each iteration
        # (outer loop of MCTS, aka number of batches of num_simulations MCTS simulations)
        'numEps': 1,

        # Total number of MCTS simulations to run when deciding on a move to play
        'num_simulations': 100,

        'numItersForTrainExamplesHistory': 20,

        # Number of epochs of training per iteration
        'epochs': 1,
        # location to save latest set of weights
        'checkpoint_path': 'latest.pth'
    }

    game = RubiksGame()
    game.env.reset(fixed_extra_scrambles=0)
    board_size = game.get_board_size()
    action_size = game.get_action_size()

    model = RubiksModel(board_size, device)

    trainer = Trainer(game, model, args)
    trainer.learn()


if __name__ == "__main__":
    main()
