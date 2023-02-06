import os
import numpy as np
from random import shuffle

import torch
import torch.optim as optim
import copy

from monte_carlo_tree_search import MCTS


class Trainer:

    def __init__(self, game, model, args):
        self.game = game
        self.model = model
        self.args = args
        self.mcts = MCTS(self.game, self.model, self.args)
        self.step = 0

    def execute_episode(self):

        train_examples = []
        # state = self.game.get_init_board()

        max_tries = 2
        tries = 0

        # state = self.game.env.reset(fixed_scramble_moves=-1)
        # state = self.game.env._get_obs()
        while True:
            print("New init gameboard")
            state = self.game \
                .get_init_board()  # self.step, self.args['numIters'])  # added

            self.mcts = MCTS(self.game, self.model, self.args)
            node = self.mcts.run(self.model, state)

            for n in range(0, 20):

                action_probs = [0 for _ in range(self.game.get_action_size())]
                for k, v in node.children.items():
                    action_probs[k] = v.visit_count \
                        if v.visit_count > 0 \
                        and v.visit_count is not None \
                        and not np.isnan(v.visit_count) \
                        else 0

                if np.isnan(np.sum(action_probs)):
                    print("isnan had NaNs so skip?")
                    break

                action_probs = action_probs / np.sum(action_probs)

                print("actprobs and sum", action_probs, np.sum(action_probs))
                train_examples.append((state, action_probs))

                # print("state, action_probs", state, action_probs)
                if len(node.children) == 0:
                    # print(
                    #    "Reached a node with no children before we got a reward so fail.")
                    break
                action = node.select_action(temperature=0)
                node = node.children[action]
                # print("state b4 action:", action, state)
                # print(n, "node", node)
                # print(n, "a", action)
                # print(n, "s1", state)

                state = self.game.get_next_state(state, action)
                # print("state now:", state)
                reward = self.game.get_reward(state)
                # print("action, next state, reward", action, state, reward)
                # print(n, "s2", state)
                if reward is not None:
                    print("reward is not none, or i == max_depth, should end episode")
                    ret = []
                    for hist_state, hist_action_probs in train_examples:
                        # [Board, actionProbabilities, Reward]
                        ret.append((hist_state, hist_action_probs, reward))

                    return ret

    def learn(self):
        for i in range(1, self.args['numIters'] + 1):

            print("{}/{}".format(i, self.args['numIters']))

            train_examples = []

            self.step = i

            for eps in range(self.args['numEps']):
                print("Eps:", eps)
                iteration_train_examples = self.execute_episode()
                train_examples.extend(iteration_train_examples)

            shuffle(train_examples)
            self.train(train_examples)
            filename = self.args['checkpoint_path']
            self.save_checkpoint(folder=".", filename=filename)

    def train(self, examples):
        optimizer = optim.Adam(self.model.parameters(), lr=5e-4)
        pi_losses = []
        v_losses = []

        print("Train started, examples:", examples)

        for epoch in range(self.args['epochs']):
            self.model.train()

            batch_idx = 0

            while batch_idx < int(len(examples) / self.args['batch_size']):
                sample_ids = np.random.randint(
                    len(examples), size=self.args['batch_size'])
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                # predict
                boards = boards.contiguous().cuda()
                target_pis = target_pis.contiguous().cuda()
                target_vs = target_vs.contiguous().cuda()

                # compute output
                out_pi, out_v = self.model(boards)
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v

                pi_losses.append(float(l_pi))
                v_losses.append(float(l_v))

                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

                batch_idx += 1

            print()
            print("Policy Loss", np.mean(pi_losses))
            print("Value Loss", np.mean(v_losses))
            print("Examples:")
            print(out_pi[0].detach())
            print(target_pis[0])

    def loss_pi(self, targets, outputs):
        loss = -(targets * torch.log(outputs)).sum(dim=1)
        return loss.mean()

    def loss_v(self, targets, outputs):
        loss = torch.sum((targets-outputs.view(-1))**2)/targets.size()[0]
        return loss

    def save_checkpoint(self, folder, filename):
        if not os.path.exists(folder):
            os.mkdir(folder)

        filepath = os.path.join(folder, filename)
        torch.save({
            'state_dict': self.model.state_dict(),
        }, filepath)
