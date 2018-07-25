import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))+'/radiosoft_srw_python')
import uti_plot_com

def extract_simulation_data(filename):
    # usage:
    # data = extract_simulation_data('filename.txt')
    data, mode, allrange, arLabels, arUnits = uti_plot_com.file_load(filename)
    # data, allrange, arLabels, arUnits are list
    return {'initial_photon_energy' : allrange[0],
            'final_photon_energy' : allrange[1],
            'x_range' : allrange[3:5],
            'y_range' : allrange[6:8],
            'data_shape' : (allrange[8], allrange[5]),
            'mean_intensity' : np.mean(data),
            'photon_energy_unit' : arUnits[0],
            'position_unit' : arUnits[1],
            'photon_intensity_unit' : arUnits[3],
            'data' : np.array(data).reshape((allrange[8], allrange[5]), order = 'C')}