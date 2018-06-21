# Function designed to take a nominal TF1 from a fit
# and the associated fit results and produce a
# shaded TGraph that can be plotted to show the
# +/- 1 sigma shifts associated with fit result


import ROOT
from array import array

def getShadedMaxAndMinTGraph( f1, fit_result, x_min=0, x_max=500, verbose=False ) :

    # For storing the extreme shifts
    x_vals = array('d', [])
    y_min = array('d', [])
    y_max = array('d', [])

    # Create new function to manipulate based off of previously fit function
    f2 = f1.Clone()
    for i in range( 0, f1.GetNpar() ) :
        f2.SetParameter( i, f1.GetParameter(i) )
    
    # Initial pass through based on nominal fit
    for x in range( x_min, x_max+1 ) :
        x_vals.append( x )
        y_min.append( f2.Eval( x ) )
        y_max.append( f2.Eval( x ) )

    # Now repeat for each uncer shifted to +/- 1 sigma and see if it
    # is > or < the min/max
    for param_index in range( 0, f1.GetNpar() ) :

        # Each needs to shift up
        shift_up = f1.GetParameter(param_index) + fit_result.ParError(param_index)
        f2.SetParameter( param_index, shift_up )
        if verbose : print "Shift: ",param_index, f1.GetParameter(param_index), shift_up

        for x in range( x_min, x_max ) :
            i = x - x_min
            val = f2.Eval( x )
            if val > y_max[ i ] : 
                if verbose : print param_index, "Up", x, " initial: ", y_max[ i ], " new: " , val, " delta: ", (y_max[ i ] - val)/y_max[ i ]
                y_max[ i ] = val
            if val < y_min[ i ] : 
                if verbose : print param_index, "Up", x, " initial: ", y_min[ i ], " new: " , val, " delta: ", (y_min[ i ] - val)/y_min[ i ]
                y_min[ i ] = val

        # and each needs to shift down
        shift_down = f1.GetParameter(param_index) - fit_result.ParError(param_index)
        f2.SetParameter( param_index, shift_down )
        if verbose : print "Shift: ",param_index, f1.GetParameter(param_index), shift_down

        for x in range( x_min, x_max ) :
            i = x - x_min
            val = f2.Eval( x )
            if val > y_max[ i ] : 
                if verbose : print param_index, "Down", x, " initial: ", y_max[ i ], " new: " , val, " delta: ", (y_max[ i ] - val)/y_max[ i ]
                y_max[ i ] = val
            if val < y_min[ i ] : 
                if verbose : print param_index, "Down", x, " initial: ", y_min[ i ], " new: " , val, " delta: ", (y_min[ i ] - val)/y_min[ i ]
                y_min[ i ] = val

        # Reset to baseline before next round
        for i in range( 0, f1.GetNpar() ) :
            f2.SetParameter( i, f1.GetParameter(i) )

    # Now construct the TGraph which will be shaded
    # For this see Rene Brun's tutorial here: https://root.cern.ch/root/html/tutorials/graphics/graphShade.C.html
    x_vals_loop = array('d', [])
    y_vals_loop = array('d', [])
    for i in range( 0, len( x_vals ) ) :
        x_vals_loop.append( x_vals[i] )
        y_vals_loop.append( y_max[i] )
    for i in range( 0, len( x_vals ) ) :
        grab = len( x_vals ) - 1 - i
        x_vals_loop.append( x_vals[grab] )
        y_vals_loop.append( y_min[grab] )

    if verbose :
        for i in range( 0, len( x_vals_loop ) ) :
            print x_vals_loop[i], y_vals_loop[i]
    
    g_shade = ROOT.TGraph( 2*len( x_vals ), x_vals_loop, y_vals_loop )
    g_shade.SetFillStyle(3013)
    g_shade.SetFillColor(16)
    return g_shade
        

