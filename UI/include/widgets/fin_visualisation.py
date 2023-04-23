import matplotlib.pyplot as plt


def draw(C_t,C_r,X_t,s):
    """Draw the fin shape along with some important
    information. These being, the center line, the
    quarter line and the center of pressure position.
    Parameters
    ----------
    None
    Returns
    -------
    None
    """
    marge_y = min(C_r/5, (C_t+X_t)/5)
    y_max = C_t + X_t + marge_y
    y_min = -marge_y if C_t+X_t>C_r else C_t+X_t-C_r - marge_y

    # Fin
    rocket_side = plt.Line2D((0,0), (y_min,y_max), color = '#000000')
    leading_edge = plt.Line2D((0, s),(C_t + X_t, C_t),color = 'r')
    tip = plt.Line2D((s, s),(C_t, 0), color='r')
    trailing_edge = plt.Line2D((s,0), (0, X_t + C_t - C_r), color = 'r')

    # # Plotting
    fig3 = plt.figure(figsize=(4, 4))
    with plt.style.context("bmh"):
        ax1 = fig3.add_subplot(111)

    # # Fin
    ax1.add_line(leading_edge)
    ax1.add_line(tip)
    ax1.add_line(trailing_edge)
    ax1.add_line(rocket_side)


    ax1.set_xlim(-s/5, s + s/5)
    ax1.set_ylim(y_min, y_max)
    ax1.set_xlabel("Span")
    ax1.set_ylabel("Root Chord")
    ax1.set_title("Trapezoidal Fin")
    ax1.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

    plt.show()
    return None



draw(2,10,16,30)