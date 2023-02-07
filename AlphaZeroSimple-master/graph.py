from __future__ import annotations
from typing import List

import game
import numpy as np
import binascii
import copy


def state_equals(s1, s2):
    return np.array_equal(s1, s2)


def get_best_reducer_i(node: Node):
    reducers = node.connections_reducing
    if len(reducers) > 0:
        best_node_i = min(reducers.keys(),
                          key=lambda i: reducers[i].distance)
        return best_node_i
    return -1


def get_cancel_move(action):
    cancel_action = -1
    if action % 2 == 0:
        cancel_action = action + 1
    else:
        cancel_action = action - 1

    return cancel_action


class Node:

    def __init__(self, state, distance=0):
        self.id = binascii.b2a_hex(np.random.bytes(5)).decode("utf-8")
        self.connections_reducing = {}
        # self.connections_expanding = {}
        self.state = state
        # self.value = 0
        self.distance = distance

    def reduces_into(self, action, node: Node):
        if node.distance < self.distance:
            self.connections_reducing[action] = node
            self.distance = node.distance + 1
        else:
            print("reduces into got called with node.distance > self.distance")
            exit(1)
        # node.connections_expanding[get_cancel_move(action)] = self

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Id:\n{self.id}" +\
            f"\nConnections reducing: [{', '.join([str(k)+': '+v.id for k, v in self.connections_reducing.items()])}]" + \
            f"\nState: {self.state}\nDistance: {self.distance}\n\n"


class RubiksExample:
    def __init__(self, model=None, depth=25, n_iters=2):
        self.model = model
        self.cube = game.RubiksGame()
        self.target_state = self.cube.correct_state
        self.depth = depth + 1
        self.n_iters = n_iters

    def connect_to_best_reducer(self, node: Node, path: List[Node]):
        org_state = node.state

        terminated = False
        actions = []
        action_states = []
        state = org_state
        for i in range(0, self.depth):
            action_probs, value = self.model.predict(state)
            # print("value", value)
            if value[0] < -0.8:
                return
            # best_action = i
            # best_action_val = 0
            # for act in range(0, 12):
            #    _, value = self.model.predict(state)
            #    best_action_val = value

            action = np.argmax(action_probs)
            state = self.cube.get_next_state(state, action)

            action_states.append(state)
            actions.append(action)

            if state_equals(state, self.cube.correct_state):
                terminated = True
                break

        if terminated:

            if len(actions) > node.distance:
                return
            elif len(actions) < node.distance:
                print("We actually managed to generate a terminal path:",
                      len(actions), "instead of", node.distance)
                print("And it was actually shorter!!!")
            p_len = len(path)
            for i, action in enumerate(actions):

                for pi in range(0, p_len):
                    p = path[pi]

                    if state_equals(p.state, action_states[i]):
                        # print("Yep it should work")
                        cur_node = node
                        for x in range(0, i):
                            new_node = Node(
                                action_states[i], distance=len(actions))

                            cur_node.reduces_into(actions[i], new_node)
                            cur_node = new_node
                            path.append(new_node)
                        # node.reduces_into()

        """
        for action in range(0, 12):

            state = self.cube.get_next_state(org_state, action)

            best_reducer = None
            best_reducer_distance = 1000

            for prev_node in reversed(path):
                if prev_node.id != node.id:
                    if state_equals(state, prev_node.state):
                        if prev_node.distance < best_reducer_distance:
                            best_reducer = prev_node

            if best_reducer is not None and best_reducer.id != node.id:
                node.reduces_into(action, best_reducer)
                # reducers = best_reducer.connections_reducing
                # best_reducer_i = get_best_reducer_i(best_reducer)

                # if best_reducer_i > 0:
                #    if reducers[best_reducer_i].id != node.id:
                #        node.reduces_into(
                #            best_reducer_i, reducers[best_reducer_i])
                # else:
                # If there's no best reducer then this action made the state solved
                # Old node is the root node
                #    node.reduces_into(action, best_reducer)
        """

    def _build(self, depth):
        state = self.target_state
        root = Node(state, distance=0)

        node = root

        path = [node]

        for i in range(1, depth):

            action = np.random.randint(0, 12)
            # move = self.cube.env._discrete_action_to_action(action)

            # self.cube.env._load_obs(state)
            # self.cube.env.cube.print()

            # self.all_moves = ["U", "U'", "L", "L'", "B",
            #        "B'", "R", "R'", "F", "F'", "D", "D'"]

            state = self.cube.get_next_state(state, action, i)

            new_node = Node(state, distance=i)

            new_node.reduces_into(action, node)

            # Get's the best old reducing path from this state
            # connect_to_best_reducer(new_node, path, state, action)

            node = new_node
            path.append(new_node)

        org_path = copy.deepcopy(path)
        for n in org_path:
            self.connect_to_best_reducer(n, path)

        return path

    def generate(self):

        # Examples are a tuple of (state, action)
        examples = []
        lens = []

        for _ in range(0, self.n_iters):

            path = self._build(self.depth)

            for i in reversed(range(1, self.depth)):
                # print("\n===================================\nAnd i:",
                #      i, "=======================================")
                node = path[i]
                thelen = 0
                while node.connections_reducing:
                    thelen += 1
                    # print(node)
                    best_reducer_i = get_best_reducer_i(node)
                    # print("best_reducer_i", best_reducer_i)
                    example_action_probs = np.zeros((12,), dtype=np.float32)
                    example_action_probs[best_reducer_i] = 1.
                    examples.append(
                        (node.state, example_action_probs, 1-(node.distance/self.depth)*2))
                    node = node.connections_reducing[best_reducer_i]
                lens.append(thelen)
                # print(node)

        # print("examples actions:", [x[1] for x in examples])
        print("num examples:", len(examples))
        # print("lens:", lens)
        print("avg length:", sum(lens)/len(lens))

        return examples


if __name__ == "__main__":
    r = RubiksExample()

    r.generate()
