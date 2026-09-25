#!/usr/bin/env python3
import random
from cmath import inf

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return

def heuristic_function (node, player):
    return node.state.player_scores[0] - node.state.player_scores[1]

def minimax (node, player, alpha, beta):
    child_list = node.compute_and_get_children()
    if len(child_list) == 1:
        return minimax(child_list[0], 1-player, alpha, beta)
    elif len(child_list) == 0 or node.depth >= 10:
        return heuristic_function(node, 0)
    else:
        if player == 0:
            best_possible_max = -inf
            for child in child_list:
                v = minimax(child, 1, alpha, beta)
                best_possible_max = max(best_possible_max, v)
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return best_possible_max
        else:
            best_possible_min = inf
            for child in child_list:
                v = minimax(child, 0, alpha, beta)
                best_possible_min = min(best_possible_min, v)
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return best_possible_min


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!
        child_list = initial_tree_node.compute_and_get_children()
        if len(child_list) == 1:
            return ACTION_TO_STR[child_list[0].move]
        else:
            minimax_list = [None] * 5
            for child in child_list:
                #minimax_list.append(minimax(child, 0))
                minimax_list[child.move] = minimax(child,0, -inf, inf)
            i = 0
            max_value = -inf
            for j in range(len(minimax_list)):
                if minimax_list[j] > max_value:
                    i = j
                    max_value = minimax_list[j]
            return ACTION_TO_STR[i]
        #random_move = random.randrange(5)
        #return ACTION_TO_STR[random_move]