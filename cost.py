def cost_calc(x_final, y_final, x, y, init_g_cost):
    """Determines the F, G, and H cost of a node"""

    g_cost = init_g_cost + 1
    h_cost_x = abs(x_final - x)
    h_cost_y = abs(y_final - y)
    h_cost = h_cost_x + h_cost_y
    f_cost = g_cost + h_cost
    return h_cost, f_cost
