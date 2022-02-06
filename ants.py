import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Ants():
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    possible_moves : list
        possible moves to do at each time step
    num_initial : int
        initial number of ants
    step : int
        current time step
    initial_position : tuple
        initial ants position
    positions : pd.DataFrame
        current position of each ant
    position_summary : pd.DataFrame
        current number of ants on each occupied position
    mu : dict
        average time (per each time step) that the dead ants needed to reach the food 
    sigma : dict
        standard deviation (per each time step) of the time that the dead ants needed to reach the food
    upper_bound : dict
        upper bound (per each time step) of the predicted average time that the dead ants needed to reach the food 
    lower_bound : dict
        lower bound (per each time step) of the predicted average time that the dead ants needed to reach the food
    dead : dict
        number of ants dead per each time step
    dead_perc : dict
        percentage of ants dead from the beginning per each time step
    alive : dict
        number of alive ants per each time step
    alive_perc : dict
        percentage of alive ants per each time step
    font_plots : dict
        parameters regarding the font of the plot to display


    Methods
    -------
    set_initial_positions()
        Initializes the ants position according to the initial_position variable
    move(constraints)
        Makes a move, checks the alive ants after the move and updates the metrics
    plot_alive_history_plot(max_steps:int=None, ax=None, **plt_kwargs)
        Plots a graph with the historical data regarding the alive ants
    plot_death_history(max_steps:int=None, ax=None, **plt_kwargs)
        Plots a graph with the historical data regarding the dead ants
    calculate_metrics()
        Calculates, stores and returns the metrics: mu, sigma, upper_bound, lower_bound
    get_info(step:int=None, decimals:int=3)
        Returns all the useful metadata at a specific time step with a specific precision
    get_history()
        Returns the whole historical data regarding the useful metadata
    """
    
    
    def __init__(self, n:int, initial_position:tuple=(0,0)) -> None:
    
        # consistency checking
        if n<=0:
            raise ValueError("Error: 'n' must be a positive integer")
        assert len(initial_position)==2
        
        self.possible_moves =  np.array([[1,0], [-1,0], [0,1], [0,-1]])
        # tracking data
        self.num_initial = n
        self.step = 0
        self.initial_position = initial_position
        self.positions = self.set_initial_positions()
        self.position_summary = self.positions.value_counts()
        # metadata
        self.mu = {0: np.nan}
        self.sigma = {0: np.nan}
        self.upper_bound = {0: np.nan}
        self.lower_bound = {0: np.nan}
        self.dead = {0: 0}
        self.alive = {0: n}
        self.dead_perc = {0: 0.0}
        self.alive_perc = {0: 1.0}
        # plot parameters
        self.font_plots = {
            'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
            }

    def set_initial_positions(self):
        
        positions = pd.DataFrame(columns = ['x', 'y'])
        positions['x'] = np.ones(self.num_initial)*self.initial_position[0]
        positions['y'] = np.ones(self.num_initial)*self.initial_position[1]
        
        return positions

    def move(self, constraints):
        
        self.step +=1
        
        # make move and check alive ants
        moves = self.possible_moves[np.random.choice(4, self.alive[self.step-1])]
        self.positions += moves
        is_alive = self.positions.apply(lambda pos: constraints(pos['x'], pos['y']), axis=1)
        self.positions = self.positions[is_alive]
        self.position_summary = self.positions.value_counts()
        # calculate metrics
        self.dead[self.step] = (~is_alive).astype(int).sum()
        self.alive[self.step] = self.alive[self.step-1] - self.dead[self.step]
        self.alive_perc[self.step] = self.alive[self.step]/self.num_initial
        self.dead_perc[self.step] = 1 - self.alive_perc[self.step]
        metrics = self.calculate_metrics(constraints)
        
        return self.dead[self.step], metrics
    
    
    def plot_alive_history_plot(self, max_steps:int=None, ax=None, **plt_kwargs):
        
        if ax is None:
            ax = plt.gca()

        # percentage of alive ants per step
        perc_history = np.array(list(self.alive.values()))/self.num_initial

        ax.plot(perc_history, **plt_kwargs)

        ax.set_title('Percentage of alive ants', fontdict=self.font_plots)
        ax.set_xlabel('Step', fontdict=self.font_plots)
        ax.set_ylabel('% Ants', fontdict=self.font_plots)
        if max_steps!=None:
            ax.set_xlim(right=max_steps)
        
        return ax

    def plot_death_history(self, max_steps:int=None, ax=None, **plt_kwargs):

        if ax is None:
            ax = plt.gca()
        
        # percentage of ants that die per turn
        perc_history = np.array(list(self.dead.values()))/self.num_initial

        ax.clear()


        ax.plot(perc_history, **plt_kwargs)
        
        ax.set_title('Percentage of ants that reached the food', fontdict=self.font_plots)
        ax.set_xlabel('Step', fontdict=self.font_plots)
        ax.set_ylabel('% Ants', fontdict=self.font_plots)
        if max_steps!=None:
            ax.set_xlim(right=max_steps)
        
        return ax
    
    
    def avg_distance2boundary(self, constraints):
        if self.position_summary.shape[0] == 0:
            return 0
        aux = self.position_summary.copy()
        aux = aux.reset_index()
        aux['dist'] = aux.apply(
            lambda z: constraints.closest_boundary[(z['x'], z['y'])][1]*z[0], 
            axis=1
            )

        return aux['dist'].sum()/self.alive[self.step]
    
    def calculate_lower_bound(self, constraints):
        # simple lower bound with +1
        # return self.mu[self.step] + (self.step+1-self.mu[self.step])*self.alive[self.step]/self.num_initial
        # more precise lower bound with the distance to the closest boundary point
        aux = self.step + self.avg_distance2boundary(constraints) - self.mu[self.step]
        return self.mu[self.step] + aux*self.alive[self.step]/self.num_initial
    
    
    def calculate_metrics(self, constraints):
        """
        Calculates, stores and returns the metrics: mu, sigma, upper_bound, lower_bound
        """

        total_dead = self.num_initial - self.alive[self.step]
        # create metrics only if the sample size of the dead ants is large enough
        if total_dead < 10:
            self.mu[self.step] = np.nan
            self.sigma[self.step] = np.nan
            self.lower_bound[self.step] = np.nan
            self.upper_bound[self.step] = np.nan
        else:
            total_dead = self.num_initial - self.alive[self.step]
            aux = [self.dead[t]*t/total_dead for t in self.dead.keys()]
            self.mu[self.step] = np.sum(aux)
            aux = [(self.dead[t]*(t-self.mu[self.step])**2)/(total_dead*(total_dead-1)) for t in self.dead.keys()] 
            self.sigma[self.step] = np.sqrt(np.sum(aux))
            self.lower_bound[self.step] = self.calculate_lower_bound(constraints)
            self.upper_bound[self.step] = self.mu[self.step] + self.step*self.alive[self.step]/total_dead
        metrics = {
            'step': self.step, 
            'mu': self.mu[self.step], 
            'sigma': self.sigma[self.step], 
            'lower_bound': self.lower_bound[self.step],
            'upper_bound': self.upper_bound[self.step]
            }
        return metrics

    def get_info(self, step:int=None, decimals:int=3):
        """
        Returns all the useful metadata at a specific time step with a specific precision
        """
        if step==None:
            step = self.step
        assert 0 <= step <= self.step, "Selected step out of range"
        info = {
            'step': step,
            'total': self.num_initial,
            'alive': int(self.alive[step]), 
            'alive%': np.round(self.alive_perc[step], decimals),
            'death_now': int(self.dead[step]),
            'death%': np.round(self.dead_perc[step], decimals),
            'mu': np.round(self.mu[step], decimals),
            'sigma': np.round(self.sigma[step], decimals),
            'lower_bound': np.round(self.lower_bound[step], decimals),
            'upper_bound': np.round(self.upper_bound[step], decimals)
            }
        
        return info
    
    def get_history(self):
        """
        Returns the whole historical data regarding the useful metadata
        """
        history = pd.DataFrame(index=self.dead.keys())
        history['alive'] = self.alive.values()
        history['alive_perc'] = self.alive_perc.values()
        history['dead'] = self.dead.values()
        history['dead_perc'] = self.dead_perc.values()
        history['mu'] = self.mu.values()
        history['sigma'] = self.sigma.values()
        history['lower_bound'] = self.lower_bound.values()
        history['upper_bound'] = self.upper_bound.values()

        return history


