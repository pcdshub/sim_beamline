import datetime
from ophyd import Device, Signal, Component
from ophyd.sim import NullStatus, new_uid
from simulate import Simulate
from functions import extract_simulation_data
import os
import numpy as np
import happi

class LclsDetector(Device):

	maxim = Component(Signal)

	def __init__(self, name, x_motor, x_field, y_motor, y_field, sim_id, sirepo_sim_address='http://10.10.10.10:8000', **kwargs):
		super().__init__(name=name, **kwargs)
		self._x_motor = x_motor
		self._y_motor = y_motor
		self._x_field = x_field
		self._y_field = y_field
		self._sim_id = sim_id
		self._sirepo_sim_address = sirepo_sim_address

	@property
	def hints(self):
		return {'fields':[self.maxim.name]}
		# this is what is being plotted during scan

	def trigger(self):
		super().trigger()

		uid = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		sim_id = self._sim_id
		sim = Simulate(self._sirepo_sim_address)
		data = sim.auth('srw', sim_id)

		# all simulated componets
		sim_fee_m1h = sim.find_element(data['models']['beamline'], 'title', 'fee_m1h')
		sim_fee_m2h = sim.find_element(data['models']['beamline'], 'title', 'fee_m2h')
		sim_hx2_slits = sim.find_element(data['models']['beamline'], 'title', 'hx2_slits')
		sim_um6_slits = sim.find_element(data['models']['beamline'], 'title', 'um6_slits')
		sim_xrt_m1h = sim.find_element(data['models']['beamline'], 'title', 'xrt_m1h')
		sim_xrt_m2h = sim.find_element(data['models']['beamline'], 'title', 'xrt_m2h')
		sim_hdx_dg2_slits = sim.find_element(data['models']['beamline'], 'title', 'hxd_dg2_slits')

		# reading current value of motors
		x = self._x_motor.read()[self._x_field]['value']
		y = self._y_motor.read()[self._y_field]['value']
		# set value of motor to change x and y position of slit at each scan
		sim_um6_slits['horizontalOffset'] = x
		sim_um6_slits['verticalOffset'] = y

		# setting values of devices in beamline according to current beamline value
		client = happi.Client(path = './happi_db.json')	
		# all devices from happi database
		fee_m1h = client.find_device(name = 'fee_m1h')
		fee_m2h = client.find_device(name = 'fee_m2h')
		hx2_slits = client.find_device(name = 'hx2_slits')
		um6_slits = client.find_device(name = "um6_slits")
		xrt_m1h = client.find_device(name = 'xrt_m1h')
		xrt_m2h = client.find_device(name = 'xrt_m2h')
		hxd_dg2_slits = client.find_device(name = 'hxd_dg2_slits')
		# getting value from these devices and set to simulated ones
		sim_fee_m1h['position'] = fee_m1h.z
		sim_fee_m2h['position'] = fee_m2h.z
		sim_hx2_slits['position'] = hx2_slits.z
		sim_um6_slits['position'] = um6_slits.z
		sim_xrt_m1h['position'] = xrt_m1h.z
		sim_xrt_m2h['position'] = xrt_m2h.z		
		sim_hdx_dg2_slits['position'] = hxd_dg2_slits.z

		watch = sim.find_element(data['models']['beamline'], 'title', 'Watchpoint')
		data['report'] = 'watchpointReport{}'.format(watch['id'])
		sim.run_simulation()

		#did this vecause cannot write data to shared folder on windows vagrant
		directory = os.path.abspath('../..') + '/data' 
		if not os.path.exists(directory):
			os.makedirs(directory)
		data_file_path = os.path.abspath('../..') + '/data/%s.txt' %uid

		# also creat this directory if it doesnot exists
		# data_file_path = os.path.dirname(os.path.realpath(__file__)) + '/data/%s.txt' %uid
		dec = sim.get_datafile().decode('UTF-8')
		datafile = open(data_file_path, "w+")
		datafile.write(dec)
		datafile.close()
		data_dict = extract_simulation_data(data_file_path)

		self.maxim.put(np.amax(data_dict['data']))

		return NullStatus()

	def unstage(self):
		super().unstage()