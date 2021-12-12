import numpy as np
import pandas as pd

class Ants():
    def __init__(self, n:int) -> None:
        if n<=0:
            raise ValueError("Error: 'n' must be a positive integer")
        self.num_initial = n
        self.num_alive = n
        self.perc_alive = 1.0
        self.step = 0
        self.death_history = {0: 0}
        self.positions = self.initial_positions()
        self.possible_moves =  np.array([[1,0], [-1,0], [0,1], [0,-1]])
        self.position_summary = {}

    def initial_positions(self):
        
        positions = pd.DataFrame(columns = ['x', 'y'])
        positions['x'] = np.zeros(self.num_initial)
        positions['y'] = np.zeros(self.num_initial)
        
        return positions

    def move(self, constraints):
        self.step +=1
        # create random moves per each ant
        moves = self.possible_moves[np.random.choice(4, self.num_alive)]
        # make move
        self.positions += moves
        # check if the ant reaches the food
        alive = self.positions.apply(lambda pos: constraints(pos['x'], pos['y']), axis=1)
        self.death_history[self.step] = (~alive).astype(int).sum()
        self.num_alive -= self.death_history[self.step]
        self.perc_alive = self.num_alive/self.num_initial
        self.positions = self.positions[alive]
        return self.death_history[self.step]
    
    def summarize_positions(self):
        summary = self.positions.value_counts()
        self.position_summary[self.step]= summary
        return summary
