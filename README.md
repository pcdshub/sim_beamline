Install sirepo on machine and import one of the zip file to simulate on the browser.

SSH to sirepo server using the command
```
export SIREPO_SERVER_ENABLE_BLUESKY=1
```
can also export this to bashrc of vagrant server so its not needed to do this everytime. Then,
```
sirepo http server 
```

The weblink has 8 digit id which is the simulation to be used for simulation.

To run the scan run scan.py file
```
python scan.py -xi 0 -xf 1 -xs 4 -yi 0 -yf 1 -ys 4 -id stciNEX4
```
the center of slit moves from (0,0) to (1,1) mm with 4 steps on each axes

results of simulation will be saved on images folder and looks like this

![scan](./images/scan.png)

![scan](./images/scan_intensities.png)
