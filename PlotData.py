import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams

dams = ['IDUKKI', 'PAMBA', 'KAKKI', 'SHOLAYAR', 'IDAMALAYAR', 'KUNDALA', 'MADUPPATTY', 'KUTTIADI', 'THARIODE', 'ANAYIRANKAL', 'PONMUDI', 'NERIAMANGALAM', 'PORINGAL', 'SENGULAM (SBR)', 'LOWER PERIYAR', 'KAKKAD']
for dam in dams:
	damData = pd.read_csv(dam+'.csv')
	damData = damData[damData.Day != 0]
	#print(damData)
	level = damData['Level (m)'].values
	storage = damData['Effective Storage (mcm)']
	rain = damData['RainFall(mm)']
	spill = damData['Spill(mcm/day)']
	inflow = damData['Inflow(mu)']
	days = damData['Day'].values
	print(level)

	fig, ax1 = plt.subplots()

	color = 'tab:red'
	ax1.set_xlabel('Day')
	lns1 = ax1.plot(days, level, color=color,label='Level(m)')
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
	color = 'tab:blue'
	lns2 = ax2.plot(days, storage, color=color,label='Storage(mcm)')
	ax2.tick_params(axis='y', labelcolor=color)

	ax3 = ax1.twinx()
	color = 'tab:green'
	lns3 = ax3.plot(days, rain, color=color,label='RainFall(mm)')
	ax3.tick_params(axis='y', labelcolor=color)

	ax4 = ax2.twinx()
	color = 'tab:orange'
	lns4 = ax4.plot(days, spill, color=color,label='Spill(mcm/day)')
	ax4.tick_params(axis='y', labelcolor=color)

	ax5 = ax2.twinx()
	color = 'tab:brown'
	lns5 = ax5.plot(days, inflow, color=color,label='Inflow(mu)')
	ax5.tick_params(axis='y', labelcolor=color)

	lns = lns1+lns2+lns3+lns4+lns5
	labs = [l.get_label() for l in lns]
	ax1.legend(lns, labs, loc=0)

	fig.tight_layout()  
	plt.savefig(dam+'.png')