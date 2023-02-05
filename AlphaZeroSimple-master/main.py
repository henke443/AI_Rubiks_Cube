import torch

from game import RubiksGame
from model import RubiksModel
from trainer import Trainer

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

args = {
    'batch_size': 64,
    # Total number of training iterations
    'numIters': 500,
    # Total number of MCTS simulations to run when deciding on a move to play
    'num_simulations': 100,
    # Number of full games (episodes) to run during each iteration
    'numEps': 100,
    'numItersForTrainExamplesHistory': 20,
    # Number of epochs of training per iteration
    'epochs': 2,
    # location to save latest set of weights
    'checkpoint_path': 'latest.pth'
}

game = RubiksGame()
game.env.reset()
board_size = game.get_board_size()
action_size = game.get_action_size()

model = RubiksModel(board_size, action_size, device)

trainer = Trainer(game, model, args)
trainer.learn()