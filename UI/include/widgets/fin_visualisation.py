import matplotlib.pyplot as plt


def draw_fin(C_t,C_r,X_t,s, save = None):
    """Draw the fin shape along with some important
    information. These being, the center line, the
    quarter line and the center of pressure position.
    Parameters
    ----------
    save (string): specify if you want to save the plot in the specified file name
    Returns
    -------
    None
    """
    marge_y = min(C_r/5, (C_t+X_t)/5)
    y_max = C_t + X_t + marge_y
    y_min = -marge_y if C_t+X_t>C_r else C_t+X_t-C_r - marge_y

    # Fin
    rocket_side = plt.Line2D((0,0), (y_min,y_max), color = '#000000', label='Rocket side')
    leading_edge = plt.Line2D((0, s),(C_t + X_t, C_t),color = 'r', label='Leading edge')
    tip = plt.Line2D((s, s),(C_t, 0), color='r', label='Tip')
    trailing_edge = plt.Line2D((s,0), (0, X_t + C_t - C_r), color = 'r', label='Trailing edge')


    # # Plotting
    fig = plt.figure(figsize=(4, 4))
    ax1 = fig.add_subplot(111)

    # # Fin
    ax1.add_line(leading_edge)
    ax1.add_line(tip)
    ax1.add_line(trailing_edge)
    ax1.add_line(rocket_side)


    ax1.set_xlim(-s/5, s + s/5)
    ax1.set_ylim(y_min, y_max)
    ax1.set_xlabel("Span")
    ax1.set_ylabel("Root Chord")
    ax1.set_title("Your Trapezoidal Fin")

    if save is not None:
        fig.savefig(save,bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()


    return None