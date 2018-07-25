from detector import LclsDetector
from ophyd.sim import SynAxis
from ophyd import Device, Component as Cpt
import bluesky.plans as bp
from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback
from databroker import Broker
import matplotlib.pyplot as plt
plt.switch_backend('agg') #so that matplotlib doesnot look for display environment
import os

RE = RunEngine({})

# prepare live visualization
bec = BestEffortCallback()
# Send all metadata/data captured to the BestEffortCallback.
RE.subscribe(bec)
# temporary sqlite backend
db = Broker.named('temp')

# Insert all metadata/data captured into db.
RE.subscribe(db.insert)

class Slit(Device):
    xmotor = Cpt(SynAxis)
    ymotor = Cpt(SynAxis)
# import pdb; pdb.set_trace()
slit = Slit(name = 'slit')
# hence, the name of motors will be slit_xmotor and slit_ymotor respectively

detector = LclsDetector('slitdetector', slit.xmotor, 'slit_xmotor', slit.ymotor, 'slit_ymotor', sim_id = 'idlHfxmh')
# detector.trigger()
# print(detector.read())
# print(detector.hints)
detector.read_attrs = ['maxim']

# center position of mirror goes from 0 to 1 mm on both axes
RE(bp.grid_scan([detector], slit.xmotor, 0, 1, 2, slit.ymotor, 0, 1, 2, True))

plt.savefig("scanimage.png")

# header = db[-1]
# import pandas as pd
# header.table().to_csv("scan_data.csv")



