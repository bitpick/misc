#!/bin/env python

import sys
import libvirt

libvirt_states = {
	libvirt.VIR_DOMAIN_NOSTATE: 'no state',
	libvirt.VIR_DOMAIN_RUNNING: 'running',
	libvirt.VIR_DOMAIN_BLOCKED: 'blocked on resource',
	libvirt.VIR_DOMAIN_PAUSED:  'paused by user',
	libvirt.VIR_DOMAIN_SHUTDOWN: 'being shut down',
	libvirt.VIR_DOMAIN_SHUTOFF: 'shut off',
	libvirt.VIR_DOMAIN_CRASHED: 'crashed',
}

NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2
NAGIOS_UNKNOWN = 3

nagios_states = {
	NAGIOS_OK: 'OK',
	NAGIOS_WARNING: 'WARNING',
	NAGIOS_CRITICAL: 'CRITICAL',
	NAGIOS_UNKNOWN: 'UNKNOWN',
}


domain_stat = {}

for key in libvirt_states.keys():
	domain_stat[key] = 0


def libvirt_health(domain_stats):
	if domain_stats[libvirt.VIR_DOMAIN_CRASHED] > 0:
		return NAGIOS_CRITICAL
	elif (domain_stats[libvirt.VIR_DOMAIN_BLOCKED] > 0)	| (domain_stats[libvirt.VIR_DOMAIN_NOSTATE] > 0):
		return NAGIOS_WARNING
	else:
		return NAGIOS_OK

try:
	conn = libvirt.openReadOnly("qemu:///system")
except Exception as e:
	print("%s - Failed to open connection (%s)" % (nagios_states.get(NAGIOS_CRITICAL), e.message))
	sys.exit(NAGIOS_CRITICAL)

domains = conn.listAllDomains(0)
domain_count = len(domains)

if domain_count == 0:
	print("%s - No domains found" % (nagios_states,get(NAGIOS_UNKNOWN)))
	sys.exit(NAGIOS_UNKNOWN)

domain_states_str = []

for dom in domains:
	domain_stat[dom.state(0)[0]] += 1
	domain_states_str.append("%s (%s), " % (dom.name(), libvirt_states.get(dom.state(0)[0])))

nagios_ret = libvirt_health(domain_stat)

print(nagios_states.get(nagios_ret) + ' - ' + ''.join([s for s in domain_states_str]))

sys.exit(nagios_ret)


