import numpy as np
import matplotlib.pyplot as plt

capacity=1000#KWh
client_use=80#MWh
cost_installation=80000#$

#power produce with standar desviation 10 MWh/year
p=10
power=p.std()
power_annual=client_use*power


"""The annual loss in efficiency is normally dis-
tributed with a mean of 1% and a standard deviation
of 0.2% and will apply after the first year."""
annual_loss= np.append(0, np.repeat(0.03, 9))
loss_efficiency = capacity * (annual_loss+ 1).cumprod()


"""tarifa"""
rate=0.109#$/kWh
total_cliente_rate=power_annual*rate

"""the annual cost of electricity is
expected to increase following a triangular distribu-
tion with most likely value of 3%, min of 2.5%,and
max of 4%, beginning with the first year"""

annual_cost= np.append(0, np.repeat(0.03, 9))
cost= total_cliente_rate * (annual_cost).cumprod()-loss_efficiency

cost_capital=0.05*12

total=cost_installation-cost_capital*cost
"""Develop a simulation model to find the net present 
value of the technology over a 10-year period"""

#%
annual_lost = market_size = np.random.normal(0.01, 0.002, 10000)
annual_cost = np.random.triangular(0.025, 0.03, 0.04, 10000)