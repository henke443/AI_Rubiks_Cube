import torch
import math
import numpy as np
import copy


def ucb_score(parent, child):
    """
    The score for an action that would transition between the parent and child.
    """
    prior_score = child.prior * \
        math.sqrt(parent.visit_count) / (child.visit_count + 1)
    if child.visit_count > 0:
        # The value of the child is from the perspective of the opposing player
        value_score = -child.value()
    else:
        value_score = 0

    return value_score + prior_score


class Node:
    def __init__(self, prior):
        self.visit_count = 0
        self.prior = prior
        self.value_sum = 0
        self.children = {}
        self.state = None

    def expanded(self):
        return len(self.children) > 0

    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

    def select_action(self, temperature):
        """
        Select action according to the visit count distribution and the temperature.
        """
        visit_counts = np.array(
            [child.visit_count for child in self.children.values()])
        actions = [action for action in self.children.keys()]
        if temperature == 0:
            action = actions[np.argmax(visit_counts)]
        elif temperature == float("inf"):
            action = np.random.choice(actions)
        else:
            # See paper appendix Data Generation
            visit_count_distribution = visit_counts ** (1 / temperature)
            visit_count_distribution = visit_count_distribution / \
                sum(visit_count_distribution)
            action = np.random.choice(actions, p=visit_count_distribution)

        return action

    def select_child(self):
        """
        Select the child with the highest UCB score.
        """
        best_score = -np.inf
        best_action = -1
        best_child = None

        for action, child in self.children.items():
            score = ucb_score(self, child)
            if score > best_score:
                best_score = score
                best_action = action
                best_child = child

        return best_action, best_child

    def expand(self, state, action_probs):
        """
        We expand a node and keep track of the prior policy probability given by neural network
        """
        self.state = state
        for a, prob in enumerate(action_probs):
            if prob != 0:
                self.children[a] = Node(prior=prob)

    def __repr__(self):
        """
        Debugger pretty print node info
        """
        prior = "{0:.2f}".format(self.prior)
        return "{} Prior: {} Count: {} Value: {}".format(self.state.__str__(), prior, self.visit_count, self.value())


class MCTS:

    def __init__(self, game, model, args):
        self.game = game
        self.model = model
        self.args = args
        self.max_depth = 3

    def run(self, model, state):

        root = Node(0)

        # EXPAND root
        action_probs, value = model.predict(state)
        valid_moves = self.game.get_valid_moves(state)
        action_probs = action_probs * valid_moves  # mask invalid moves
        action_probs /= np.sum(action_probs)
        root.expand(state, action_probs)

        # print("MCTS simulation started, root:", root)

        for _ in range(self.args['num_simulations']):

            value = None

            node = root
            search_path = [node]

            # SELECT
            while node.expanded():
                action, node = node.select_child()
                search_path.append(node)

            parent = search_path[-2]
            state = parent.state
            # Now we're at a leaf node and we would like to expand
            # Players always play from their own perspective
            # print("len(search_path)", len(search_path))
            next_state = self.game.get_next_state(
                state, action=action, total_moves=len(search_path))
            # Get the board from the perspective of the other player
            # next_state = self.game.get_canonical_board(next_state, player=-1)

            # The value of the new state from the perspective of the other player
            value = self.game.get_reward(next_state)
            # nextcopy = copy.copy(next_state)

            """
            if value is not None:
                print("Value:", value)
                print("Solved once, parent state, action:", parent.state, action)

                actions = [[ac, child.visit_count, child.prior, child.value_sum]
                           for ac, child in parent.children.items()]
                print("Parent probs:\n", actions)
                print("Parent would choose:",
                      parent.select_action(temperature=0))
                print("resulting state:", next_state, "\n")

            """

            if value is None:
                # If the game has not ended:
                # EXPAND
                old_action_probs = action_probs
                action_probs, value = model.predict(next_state)

                # print("Value was none and now:", value)
                if hasattr(value, "__len__"):
                    value = value[0]
                # print("Value was none and after thing:", value)

                if len(search_path) <= self.max_depth:
                    valid_moves = self.game.get_valid_moves(next_state)
                    action_probs = action_probs * valid_moves  # mask invalid moves
                    action_probs /= np.sum(action_probs)
                    node.expand(next_state, action_probs)
                else:
                    action_probs = old_action_probs
                    # value = 0

            self.backpropagate(search_path, value)

        # print("mcts run ended")
        return root

    def backpropagate(self, search_path, value):
        """
        At the end of a simulation, we propagate the evaluation all the way up the tree
        to the root.
        """
        for node in reversed(search_path):
            node.value_sum += value
            node.visit_count += 1
