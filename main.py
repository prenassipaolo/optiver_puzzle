import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import boundary_func
from utils import neighbors, dict2keys_values, read_yaml
from ants import Ants
from  constraints import Constraint
from grid import Grid


CONFIG_PATH = 'config.yaml'


def calculate_exact_solution(constraints, starting_point:tuple=(0.,0.)):
    """
    Calculates the exact average time to reach the food starting from starting_point
    """
    assert len(starting_point)==2
    # create transition matrix
    M = pd.DataFrame(
        data = 0., 
        index = list(constraints.inside_points), 
        columns = list(constraints.inside_points)
        )
    for x,y in constraints.inside_points:
        ngbr = neighbors(x, y)
        ngbr = {n for n in ngbr if n in constraints.inside_points}
        for n in ngbr:
            M.at[(x, y), n] = 0.25
    # calculate the inverse of (1-M)
    inverse = np.linalg.inv(np.identity(len(constraints.inside_points))-M)
    inverse = pd.DataFrame(
        data = inverse, 
        index = list(constraints.inside_points), 
        columns = list(constraints.inside_points)
        )
    # calculate solution for a specific starting point
    solution = inverse.sum()[starting_point]
    return solution


def base_track():
    """
    Tracks the random movements of the ants.
    The metrics calculations are displayed every TRACK_INTERVAL steps
    """
    
    info = ants.get_info()
    text = '\t'.join(['{}']*len(info))
    text = text.format(*info.keys())
    print(text)

    while ants.step<=cfg['tracking']['MAX_STEPS']-1 and ants.alive[ants.step]>0:
        
        ants.move(constraints)
        #grid.update_grid(changes=ants.position_summary)

        if ants.step%cfg['tracking']['BASE_TRACK_INTERVAL']==0 or \
            ants.step==cfg['tracking']['MAX_STEPS'] or \
            ants.alive_perc==0:
            info = ants.get_info()
            text = '\t'.join(['{}']*len(info))
            text = text.format(*info.values())
            print(text)

    return 


def animated_track():
    """
    Tracks and plots the random movements of the ants.
    """
    # CREATE FIGURE
    gs_kw = dict(width_ratios=[2, 1], height_ratios=[1, 1])
    fig, axd = plt.subplot_mosaic(
        [['left', 'upper right'], ['left', 'lower right']],
        gridspec_kw=gs_kw, figsize=(22, 11),
        constrained_layout=False
    )
    plt.subplots_adjust(wspace=1, hspace=0.2)
    # ANIMATION
    animation = FuncAnimation(
        fig=fig, 
        func=animation_frame, 
        frames=cfg['tracking']['MAX_STEPS']-1, 
        fargs=[axd], 
        interval=cfg['tracking']['WAIT_TIME'],
        blit=False,  
        repeat=False
        )
    plt.show()

    return 

def animation_frame(i, axd):
    """
    Performs one step of the random movements of the ants, 
    plots their posistions and calculates the metrics 
    """

    ants.move(constraints)
    grid.update_grid(changes=ants.position_summary)

    info = ants.get_info()

    text = '\n'.join(['{}:\t{}']*len(info))
    text = text.format(*dict2keys_values(info))
    text = text.expandtabs()

    # clear what we have plot before
    # this function avoids that the overlapping of the lines using different colours
    for pos in axd:
        axd[pos].clear()

    # CREATE PLOTS
    # FuncAnimation recreates the heatmap's cbar multiple times,
    # then we need to plot it only during the first cycle
    global first_cycle
    first_cycle = True
    if first_cycle:
        grid.plot(
            vmax=ants.num_initial, 
            masked=True, 
            text=text, 
            ax = axd['left'], 
            show_cbar=False
            )
        first_cycle = False   # turn off first_cycle
    else:
        grid.plot(
            vmax=ants.num_initial, 
            masked=True, 
            text=text, 
            ax = axd['left'], 
            show_cbar=False
            )
    ants.plot_death_history(
        cfg['tracking']['MAX_STEPS'], 
        ax = axd['upper right']
        )
    ants.plot_alive_history_plot(
        cfg['tracking']['MAX_STEPS'], 
        ax = axd['lower right']
        )

    #if ants.step%1==0 or ants.step>max_steps or ants.num_alive<=0:
    text = '\t'.join(['{}:\t{}']*len(info))
    text = text.format(*dict2keys_values(info))
    print(text)

    return ants, grid


def setup():
    """
    Loads the configuaration parameters and setups all the core variables.
    """
    # config
    global cfg
    cfg = read_yaml(CONFIG_PATH)
    # seed
    np.random.seed(cfg['ants']['SEED'])
    # ants
    global ants
    ants = Ants(
        n = cfg['ants']['NUM_ANTS'], 
        initial_position = cfg['ants']['INITIAL_POSITION']
        )
    # contraints
    global constraints
    constraints = Constraint(
        getattr(boundary_func, cfg['constraints']['FUNCTION'])
        )
    constraints.evaluate_points(
        start_points = {cfg['ants']['INITIAL_POSITION']}, 
        max_iter = cfg['solution']['MAX_POINTS'], 
        print_iter = None
        )
    constraints.find_closest_boundary()
    # grid
    if cfg['tracking']['SHOW_ANIMATION']:
        global grid
        grid = Grid(cfg['grid']['HEIGHT'], cfg['grid']['WIDTH'])
        start_change = pd.Series(
            data = [cfg['ants']['NUM_ANTS']], 
            index=[cfg['ants']['INITIAL_POSITION']]
            )
        grid.update_grid(changes=start_change)
        grid.initialize_mask(constraints=constraints)

    return cfg



def main():
    
    setup()
    

    if cfg['solution']['FIND_EXACT']:
        solution = calculate_exact_solution(
            constraints = constraints, 
            starting_point = cfg['ants']['INITIAL_POSITION']
            )
        print(f'\nExact solution: {np.round(solution, 3)}\n')
    else:
        solution = None

    if cfg['tracking']['DO_TRACKING']:
        if cfg['tracking']['SHOW_ANIMATION']:
            animated_track()
        else:
            base_track()
        # create dataframe with historical data
        history = ants.get_history()
        # save
        if cfg['tracking']['PATH']:
            history.to_csv(cfg['tracking']['PATH'])
    else:
        history = None

    return solution, history


if __name__=="__main__":
    
    main()