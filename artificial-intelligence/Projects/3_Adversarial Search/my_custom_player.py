
from sample_players import DataPlayer
import random

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        # randomly select a move as player 1 or 2 on an empty board, otherwise
        # return the optimal minimax move at a fixed search depth of 3 plies
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.minimax(state, depth_limit=2))

    def minimax(self, state, depth_limit):

        def min_value(state, depth, alpha, beta):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1, alpha, beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, depth, alpha, beta):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1, alpha, beta))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        # I don't know how to implement alpha-beta in such short way :(
        # return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

        def alpha_beta_pruning(state, depth):
            alpha = float("-inf")
            beta = float("inf")
            best_score = float("-inf")
            best_move_pruning = None
            for m in state.actions():
                v = min_value(state.result(m), depth - 1, alpha, beta)
                alpha = max(alpha, v)
                if v > best_score:
                    best_score = v
                    best_move_pruning = m
            return best_move_pruning

        #iterative deepening
        best_move = None
        for depth in range(1, depth_limit + 1):
            best_move = alpha_beta_pruning(state, depth)
        return best_move

    def score_0(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    def score_1(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - 2 * len(opp_liberties)

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)

        # Convert from board index value to xy coordinates
        # The coordinate frame is 0 in the bottom right corner, with x increasing
        # along the columns progressing towards the left, and y increasing along
        # the rows progressing towards teh top.
        _WIDTH = 11
        _HEIGHT = 9
        own_score = 0
        opp_score = 0
        for l in own_liberties:
            x = l % (_WIDTH + 2)
            y = l // (_WIDTH + 2)
            if x <= (_WIDTH - 3) and x >= 2 and y <= (_HEIGHT - 3) and y >= 2:
                own_score += 3
            elif ((x <= 1 and x >= 0 and y <= 1 and y >= 0) or
                  (x <= 1 and x >= 0 and y <= (_HEIGHT - 1) and y >= (_HEIGHT - 2)) or
                  (x <= (_WIDTH - 1) and x >= (_WIDTH - 2) and y <= (_HEIGHT - 1) and y >= (_HEIGHT - 2)) or
                  (x <= (_WIDTH - 1) and x >= (_WIDTH - 2) and y <= 1 and y >= 0)):
                own_score += 1
            else:
                own_score += 2

        for l in opp_liberties:
            x = l % (_WIDTH + 2)
            y = l // (_WIDTH + 2)
            if x <= (_WIDTH - 3) and x >= 2 and y <= (_HEIGHT - 3) and y >= 2:
                opp_score += 3
            elif ((x <= 1 and x >= 0 and y <= 1 and y >= 0) or
                  (x <= 1 and x >= 0 and y <= (_HEIGHT - 1) and y >= (_HEIGHT - 2)) or
                  (x <= (_WIDTH - 1) and x >= (_WIDTH - 2) and y <= (_HEIGHT - 1) and y >= (_HEIGHT - 2)) or
                  (x <= (_WIDTH - 1) and x >= (_WIDTH - 2) and y <= 1 and y >= 0)):
                opp_score += 1
            else:
                opp_score += 2

        return own_score - 2 * opp_score