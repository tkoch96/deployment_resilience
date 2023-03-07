### with anycast, need to measure all catchments when all but one pop is up
### can do one per pop failures with a pop failing

import os, numpy as np
from constants import *
from helpers import *

per_peering_lats = parse_ingress_latencies_mp(os.path.join(CACHE_DIR, 'vultr_ingress_latencies_by_dst.csv'))
per_peering_lats = per_peering_lats['meas_by_ip']
all_ingresses = list(set([popp for ip in per_peering_lats for popp in per_peering_lats[ip]]))

anycast_lats = {}
with open(os.path.join(CACHE_DIR, 'vultr_anycast_latency.csv'),'r') as f:
	for row in f:
		ip,lat,pop = row.strip().split(',')
		if lat == '-1': continue
		lat = float(lat) * 1000
		try:
			anycast_lats[ip].append(lat)
		except KeyError:
			anycast_lats[ip] = [lat]
anycast_lats = {ip:np.min(anycast_lats[ip]) for ip in anycast_lats}
lats_by_pop = {}
with open(os.path.join(CACHE_DIR, 'vultr_oneperpop_adv_latencies.csv'),'r') as f:
	for row in f:
		ip,spop,epop,lat = row.strip().split(',')
		if spop!=epop or epop=='None': continue
		if lat == '-1': continue
		lat = float(lat) * 1000
		try:
			lats_by_pop[ip]
		except KeyError:
			lats_by_pop[ip] = {pop: [] for pop in VULTR_POP_TO_LOC}
		lats_by_pop[ip][epop].append(lat)

NO_MEASURE_LAT = 10000

for ip in lats_by_pop:
	for pop in lats_by_pop[ip]:
		if len(lats_by_pop[ip][pop]) == 0:
			lats_by_pop[ip][pop] = NO_MEASURE_LAT
		lats_by_pop[ip][pop] = np.min(lats_by_pop[ip][pop])

# ips_in_all = get_intersection(lats_by_pop, anycast_lats)
ips_in_all = get_intersection(lats_by_pop, per_peering_lats)
print(len(ips_in_all))

n_pops_by_ip = [sum(1 for pop in lats_by_pop[ip] if lats_by_pop[ip][pop] != NO_MEASURE_LAT) for ip in ips_in_all]
n_popps_by_ip = [len(per_peering_lats[ip]) for ip in ips_in_all]
# print(np.median(n_pops_by_ip))
# print(np.median(n_popps_by_ip))

#### PoP Fails!
one_per_pop_suboptimality, one_per_pop_hits, best_case_suboptimality = [],[],[]
for pop in VULTR_POP_TO_LOC:
	for ip in ips_in_all:
		best_pop_lat = np.min(list(lats_by_pop[ip].values()))
		if best_pop_lat != lats_by_pop[ip][pop]:
			## Only consider this IP if this is it's best pop
			continue
		not_this_pop_intfs = list(per_peering_lats[ip][popp] for popp in \
			per_peering_lats[ip] if popp[0] != pop)
		if len(not_this_pop_intfs) == 0:
			continue
		# best not-failed pop
		best_alternate_lat = np.min(not_this_pop_intfs) 
		# best not-failed ingress
		best_alternate_pop_lat = np.min(list(lats_by_pop[ip][p] for p in lats_by_pop[ip] if p != pop)) 
		if best_alternate_pop_lat == NO_MEASURE_LAT: 
			continue
		one_per_pop_suboptimality.append(np.maximum(best_alternate_pop_lat - best_alternate_lat,0))
		one_per_pop_hits.append(best_alternate_pop_lat - best_pop_lat) # best_pop_lat is failed one
		best_case_suboptimality.append(best_alternate_lat - best_pop_lat)
import matplotlib.pyplot as plt
x,cdf_x = get_cdf_xy(one_per_pop_suboptimality)
# this is how much performance you're giving up by not using per-intf stuff
plt.plot(x,cdf_x,label='One per PoP Suboptimality')
x,cdf_x = get_cdf_xy(one_per_pop_hits)
# compare pop to second best pop (not per-intf)
plt.plot(x,cdf_x,label='One per PoP Failover Performance Hit')

x,cdf_x = get_cdf_xy(best_case_suboptimality)
# compare best case lat to previous one-per-pop lat
plt.plot(x,cdf_x,label='Best Case Failover Lat, Previous One per PoP')

plt.xlabel("Difference (Method - Optimal) (ms)")
plt.ylabel("CDF of UGs")
plt.grid(True)
plt.legend()
plt.xlim([0,100])
plt.savefig('figures/pop_failure_performance_losses.pdf')
plt.clf(); plt.close()

#### PoPP Fails! (assume a 1 per ingress strategy, maximally distributed)
comps, good_at_all_comps = [],[]
for ip in ips_in_all:
	best_ingress_lat = np.min(list(per_peering_lats[ip].values()))
	for popp in all_ingresses:
		try:
			if best_ingress_lat != per_peering_lats[ip][popp]:
				## Only consider this IP if this is it's best ingress
				continue
		except KeyError:
			continue
		not_this_ingress_intfs = list(per_peering_lats[ip][_popp] for _popp in \
			per_peering_lats[ip] if _popp != popp)
		if len(not_this_ingress_intfs) == 0:
			continue
		# best not-failed ingress
		best_alternate_ingress_lat = np.min(not_this_ingress_intfs)
		# compare best (failed) to best alternate (unfailed)
		good_at_all_comps.append(best_alternate_ingress_lat - best_ingress_lat)
import matplotlib.pyplot as plt
# print(len(comps))
# x,cdf_x = get_cdf_xy(comps)
# plt.plot(x,cdf_x,label='Compared to Best Ingress (Unfailed)')
x,cdf_x = get_cdf_xy(good_at_all_comps)
plt.plot(x,cdf_x,label='Compared to Best Ingress (Failed)')
plt.xlabel("Difference (Method - Optimal) (ms)")
plt.ylabel("CDF of Cases")
plt.grid(True)
plt.legend()
plt.xlim([0,100])
plt.savefig('figures/ingress_failure_performance_losses.pdf')
plt.clf(); plt.close()

