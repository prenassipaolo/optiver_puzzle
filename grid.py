import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Grid():
    def __init__(self, height:int, width:int, default_value=np.nan, constraints=None) -> None:
        
        assert height>0
        assert width>0
        self.height = height
        self.width = width
        self.index = np.flip(np.arange(self.height)) - self.height//2
        self.columns = np.arange(self.width) - self.width//2
        self.default_value = default_value
        
        self.default_grid = None
        self.initialize_grid()
        self.grid = self.default_grid
        #self.update_grid(changes)
        self.mask = None
        self.mask = self.initialize_mask(constraints)


    def initialize_grid(self):
        grid = np.full([self.height, self.width], self.default_value)
        grid = pd.DataFrame(data=grid, index=self.index, columns=self.columns)
        self.default_grid = grid
        return grid

    def update_grid(self, changes, from_default=True):
        #if changes!=None:
        # if from_default=True it starts the changes form the default grid, otherise fromt the actual one
        if from_default:
            self.grid = self.default_grid.copy()
        # update the grid
        if changes.size>=1:
            
            for x,y in changes.index:
                # the grid could be smaller than the indeces in 'changes'
                if x in set(self.columns) and y in set(self.index):
                    self.grid.at[y,x] = changes[x,y]

        return self.grid

    def initialize_mask(self, constraints):
        if constraints!=None:
            # create every possible combination between 2 arrays
            mask = pd.DataFrame(index = pd.MultiIndex.from_product([self.index, self.columns]))
            mask.index.set_names(['y', 'x'], inplace=True)
            # evaluate the constraint function in each point
            mask['mask'] = mask.reset_index().apply(lambda pos: not constraints(pos['x'], pos['y']), axis=1).values
            # tranform from 1D to 2D
            mask = mask.unstack(level=1) # level=1 means that the indeces would be the y
            # drop the name "mask" from the columns
            mask = mask.droplevel(level=0, axis=1)
            # unstack changes th order of the indexes, so we have to sorte them again
            mask = mask.sort_index(ascending=False, axis=0)
            mask = mask.sort_index(ascending=True, axis=1)
            # update the mask
            self.mask = mask
            return mask
        return None
    
    def plot(self, vmax=None, text:str=None, masked:bool=False):
        
        # add mask
        if masked:
            sns.heatmap(
                data = self.mask, 
                vmin = 0, 
                vmax = 10, 
                cmap = 'Blues', 
                annot = False,
                linewidths = 0.5,
                cbar = False
                )
        ax = sns.heatmap(
            data = self.grid, 
            vmin = 0, 
            vmax = vmax, 
            cmap = 'rocket_r', 
            annot = True,
            linecolor='white',
            linewidths = 0.5, 
            xticklabels=True, 
            yticklabels=True
            )
        
        plt.text(self.width + self.width//2, self.height//2, text, fontsize=12)
        plt.show()
        return ax