"""
Several reinforcement learning algorthimns.  

If they begin with a 'b_' they were implemented allow fitting of behavoiral 
accuracy data.  If they begin with a 's_' there were desinged to simulate 
'online' learning (e.g. an computational agent learning an N-armed bandit 
task).
"""

def b_delta(rewards,states,alpha):
	"""
	Implements the Resorla-Wagner (delta) learning rule. Of course,
	if multiple states are chain together (in reality) they are 
	treated as independent; use td_0() or similar for state-spaces of
	order 1 or larger.  V_intial is 0. 
	
	Note: Null states are silently skipped.
	
		Returns seperate dicts for Qs and RPEs, in that order.
	"""

	# Init
	s_names = set(states)
	V_dict = {}
	RPE_dict = {}
	for s in s_names:
		V_dict[s] = [0.]
		RPE_dict[s] = []
	
	for r,s in zip(rewards,states):
		
		## Skip terminal states
		if (s == 0) | (s == '0'):
			continue

		V = V_dict[s][-1]

		## the Delta rule:
		RPE = r - V
		V_new = V + alpha * RPE

		## Store and shift V_new to
		## V for next iter	
		V_dict[s].append(V_new) 
			
		## Store RPE 
		RPE_dict[s].append(RPE)

	return V_dict, RPE_dict


def b_td_0(rewards,states,alpha):
	"""
	UNTESTED

	Implements Sutton and Barto's temporal differnce alorithmn, assuming 
	gamma is 1. All V (values) intialized at zero.
	
	Arbitrary numbers of states are allowed; to simplify it was assumed 
	that once started the markov process continues until the terminal state 
	is achieved.
	
	Each trial is composed of one set of states which are contiguosly 
	packed seperated only by null (0), that is to say terminal, states, the 
	(empty) terminal state. 
	
		Returns Qs a dict of lists and RPEs (list), in that order.
	"""
	
	## From: 
	## Sutton And Barto, Reinforcement Learning: An Introduction, MIT Press, 1998.
	##
	## Intializa V(s) and pi (policy)
	## Repeat (for each trial)
	## 	Intializa s
	##  Repeat (for each step/state)
	##    a is the action given by pi for s
	##    Take a; observe reward (r) and the next state (s')
	##    V(s) <- V(s) + alpha * (r + gamma * V(s') - V(s))
	##    s <- s'
	##  until s is terminal

	gamma = 1

	## Init V_dict, and RPE_list
	## Start V_intial as 0. RPE is empty
	## so V and RPE are in sink
	s_names = set(states)
	V_dict = {}
	RPE_dict = {}
	for n in s_names:
		V_dict[n] = [0.]
		RPE_dict[n] = []

	for step in range(size(states)-1):
		r = rewards[step]
		s = states[step]
		s_plus = states[step+1]
		
		## There is nothing to calculate for the 
		## state before the terminal so go to next 
		## step
		if (s_plus == 0) | (s_plus == '0'):
			print('Skipping 0.')
			continue

		V_s = V_dict[s]
		V_s_plus = V_dict[s_plus]

		RPE = r + gamma * V_s_plus - V_s
		V_s = V_s + alpha * RPE

		V_dict[s] = V_dict[s].append(V_s)
		RPE_dict[s] = RPE_dict[s].append(RPE)

	return V_dict, RPE_dict


def b_rc(actions,rewards,beta):
	"""
	UNTESTED.

	Inplements Sutton And Barto's (1998) 'reinforcement comparison' 
	algorithmn. Returning P(action) for each action at each timestep in a 
	dict and the accompanying accumulative reference reward (i.e. the 
	inline reward average) and reference predicion error (RPE).

	Beta is the step size (0-1).  Rewards in this model may be any real
	number (unlike sat most td implementations who are bound between 0-1).
	"""

	## In simulation action selection policy is set by softmax:
	## In this example there are three possible actions, extends to N
	## P(a_t = a) = e^P_t(a) / sum( e^P_t(b) + e^P_r(c) + ...) 
	## Will display probability matching....
	
	ref_reward = 0
	P_dict = {}
	ref_reward_dict = {}
	RPE_dict = {}  # the reference prediction error (RPE)
	for a in set(actions):
		## Init P_dict, and the rest.
		## Start P_intial and ref_reward_dict as 0;
		## RPE is empty, keeping them in sink.
		P_dict[a] = [0]
		ref_reward_dict[a] = [0]
		RPE_dict[a] = []

	for a,r in actions,rewards:
		## Do calcs, then update dicts
		ref_reward = ref_reward_dict[a][-1]
		RPE = r - ref_reward
		P_a_tminus = P_dict[a][-1]
		P_a_t = P_a_tminus + (beta * RPE)

		P_dict[a] = P_dict[a].append(P_a_t)
		ref_reward_dict[a] = ref_reward_dict[a].\
				append((ref_reward + r) / 2)
		RPE_dict[a] = RPE_dict[a].append(RPE)

	return P_dict, ref_reward_dict, RPE_dict
