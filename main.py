from docplex.mp.model import Model
from datetime import timedelta

# --- CONSTANTS ---
HOURS = 24
MINUTES_IN_DAY = 1440
MinUtilTime = 300
MinUtilTime_2 = 800
MaxUtilTime = 1440

vehicle_fixed_cost = 1000
freq_penalty = 1000

nvehicle = 20
K = range(nvehicle)
H = range(HOURS)

bigM = 1440

freq1 = [0, 0, 0, 0, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 4, 5, 6, 2, 0, 0]
freq2 = [0, 0, 0, 0, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 4, 5, 6, 4, 0, 0]
# freq1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 5, 6, 2, 0, 0]  # ATB freq per hour
# freq2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 5, 6, 4, 0, 0] 

arc_data = {
    ("X", "X"): (0, 150),
    ("X", "HSK"): (10, 150),
    ("X", "ATB"): (40, 150),
    ("HSK", "HSK"): (200, 150),
    ("ATB", "ATB"): (200, 150),
    ("HSK", "ATB"): (110, 1),
    ("ATB", "HSK"): (110, 1),
    ("HSK", "X"): (10, 150),
    ("ATB", "X"): (40, 150)
}

transitions = {"ATB": "HSK", "HSK": "ATB"}
travel_time = {
    ("ATB", "HSK"): arc_data[("ATB", "HSK")][0],
    ("HSK", "ATB"): arc_data[("HSK", "ATB")][0]
}

# --- NODES ---
nodes = []
node_id = 1
nodes.append({'id': node_id, 'time': 0, 'loc': 'X'})
start_node_id = node_id
node_id += 1

for hour in H:
    for i in range(freq1[hour]):
        time_val = hour * 60 + (i * 60 // max(freq1[hour], 1))
        nodes.append({'id': node_id, 'time': time_val, 'loc': 'ATB'})
        node_id += 1
    for i in range(freq2[hour]):
        time_val = hour * 60 + (i * 60 // max(freq2[hour], 1))
        nodes.append({'id': node_id, 'time': time_val, 'loc': 'HSK'})
        node_id += 1

nodes.append({'id': node_id, 'time': MINUTES_IN_DAY, 'loc': 'X'})
end_node_id = node_id
node_id += 1

nodes.sort(key=lambda x: x['time'])
V = nodes.copy()

# --- ARCS ---
E = []
synthetic_id = node_id
synthetic_nodes = []

for node in nodes:
    loc = node['loc']
    dst_time = node['time']
    if loc in ['ATB', 'HSK']:
        cost, N_bus = arc_data[('X', loc)]
        if dst_time >= cost:
            E.append({
                'src': {'id': start_node_id, 'time': 0, 'loc': 'X'},
                'dst': {'id': node['id'], 'time': dst_time, 'loc': loc},
                'cost': cost,
                'N_bus': N_bus
            })

for node in nodes:
    loc = node['loc']
    time = node['time']
    src_id = node['id']

    if loc not in transitions:
        continue

    total_time = 0
    curr_loc = loc
    curr_time = time
    curr_src_id = src_id

    while total_time + travel_time[(curr_loc, transitions[curr_loc])] <= MinUtilTime_2:
        next_loc = transitions[curr_loc]
        cost = travel_time[(curr_loc, next_loc)]
        next_time = curr_time + cost

        if next_time > MINUTES_IN_DAY:
            break

        dst = {'id': synthetic_id, 'time': next_time, 'loc': next_loc}
        synthetic_nodes.append(dst)

        E.append({
            'src': {'id': curr_src_id, 'time': curr_time, 'loc': curr_loc},
            'dst': dst,
            'cost': cost,
            'N_bus': 1
        })

        curr_src_id = synthetic_id
        curr_time = next_time
        curr_loc = next_loc
        synthetic_id += 1
        total_time += cost

    if curr_time <= MINUTES_IN_DAY:
        cost_to_X, N_bus_to_X = arc_data[(curr_loc, 'X')]
        E.append({
            'src': {'id': curr_src_id, 'time': curr_time, 'loc': curr_loc},
            'dst': {'id': end_node_id, 'time': MINUTES_IN_DAY, 'loc': 'X'},
            'cost': cost_to_X,
            'N_bus': N_bus_to_X
        })

V.extend(synthetic_nodes)

# Additional arcs from synthetic nodes to end node X (if not already in E)
for node in synthetic_nodes:
    loc = node['loc']
    time = node['time']
    cost_to_end, N_bus_to_end = arc_data[(loc, 'X')]
    if time + cost_to_end <= MINUTES_IN_DAY:
        arc_exists = any(
            e['src']['id'] == node['id'] and e['dst']['id'] == end_node_id for e in E
        )
        if not arc_exists:
            E.append({
                'src': node,
                'dst': {'id': end_node_id, 'time': MINUTES_IN_DAY, 'loc': 'X'},
                'cost': cost_to_end,
                'N_bus': N_bus_to_end
            })

# Additional arcs from X to synthetic nodes
for node in synthetic_nodes:
    if node['time'] >= arc_data[('X', node['loc'])][0]:
        E.append({
            'src': {'id': start_node_id, 'time': 0, 'loc': 'X'},
            'dst': node,
            'cost': arc_data[('X', node['loc'])][0],
            'N_bus': arc_data[('X', node['loc'])][1]
        })



# # Add readable time format
# for node in V:
#     node['hhmm'] = str(timedelta(minutes=node['time']))[:-3]

# # Output all nodes in V
# count = 0
# for node in V:
#     print(node)
#     count += 1
# print(f"Total nodes in V: {count}")

# # Output arcs
# print(f"Total generated arcs: {len(E)}")
# for arc in E[:]:
#     print(f"From node {arc['src']['id']} ({arc['src']['loc']} @ {arc['src']['time']}) "
#           f"to node {arc['dst']['id']} ({arc['dst']['loc']} @ {arc['dst']['time']}) "
#           f"cost: {arc['cost']}")

# --- MODEL ---
mdl = Model("VehicleScheduling")
mdl.context.cplex_parameters.lpmethod = 3

x = mdl.binary_var_dict(((e['src']['id'], e['dst']['id'], k) for e in E for k in K), name='x')
z = mdl.binary_var_dict(K, name='z')
T = mdl.continuous_var_dict(K, name='T', lb=0)

node_ids_in_arcs = set()
for e in E:
    node_ids_in_arcs.add(e['src']['id'])
    node_ids_in_arcs.add(e['dst']['id'])

arrival_time = mdl.continuous_var_dict(((k, nid) for k in K for nid in node_ids_in_arcs), name='arr', lb=0, ub=MINUTES_IN_DAY)
freq_slack_ATB = mdl.continuous_var_dict(H, name='freq_slack_ATB', lb=0)
freq_slack_HSK = mdl.continuous_var_dict(H, name='freq_slack_HSK', lb=0)

mdl.minimize(
    mdl.sum(e['cost'] * x[e['src']['id'], e['dst']['id'], k] for e in E for k in K) +
    mdl.sum(vehicle_fixed_cost * z[k] for k in K) 
)
# mdl.sum(freq_penalty * (freq_slack_ATB[h] + freq_slack_HSK[h]) for h in H)
for k in K:
    mdl.add_constraint(mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0) for e in E) <= bigM * z[k])
    mdl.add_constraint(z[k] <= mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0) for e in E))

    mdl.add_constraint(mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0) for e in E if e['src']['id'] == start_node_id) == z[k])
    mdl.add_constraint(mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0) for e in E if e['dst']['id'] == end_node_id) == z[k])

    for node in V:
        i = node['id']
        if i != start_node_id and i != end_node_id:
            mdl.add_constraint(
                mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0) for e in E if e['src']['id'] == i) ==
                mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0) for e in E if e['dst']['id'] == i)
            )

for e in E:
    if e['N_bus'] == 1:
        mdl.add_constraint(mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0) for k in K) <= 1)

for k in K:
    mdl.add_constraint(T[k] == mdl.sum(e['cost'] * x.get((e['src']['id'], e['dst']['id'], k), 0) for e in E if e['N_bus'] == 1))
    mdl.add_constraint(T[k] >= MinUtilTime * z[k])
    mdl.add_constraint(T[k] <= MaxUtilTime * z[k])

for e in E:
    for k in K:
        i, j = e['src']['id'], e['dst']['id']
        cost = e['cost']
        mdl.add_constraint(arrival_time[k, j] >= arrival_time[k, i] + cost - bigM * (1 - x.get((i, j, k), 0)))
        mdl.add_constraint(arrival_time[k, j] <= arrival_time[k, i] + cost + bigM * (1 - x.get((i, j, k), 0)))

# for h in H:
#     mdl.add_constraint(
#         mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0)
#                 for k in K
#                 for e in E if e['N_bus'] == 1 and e['src']['loc'] == 'ATB' and (e['src']['time'] // 60) == h)
#         + freq_slack_ATB[h] >= freq1[h]
#     )
#     mdl.add_constraint(
#         mdl.sum(x.get((e['src']['id'], e['dst']['id'], k), 0)
#                 for k in K
#                 for e in E if e['N_bus'] == 1 and e['src']['loc'] == 'HSK' and (e['src']['time'] // 60) == h)
#         + freq_slack_HSK[h] >= freq2[h]
#     )In this slack frequency is added extra to cover up the vacant frequency and added as the penalty in the minimization function 
for h in H:
    mdl.add_constraint(
        mdl.sum(
            x[e['src']['id'], e['dst']['id'], k]
            for e in E if e['cap'] == 1 and e['src']['loc'] == 'ATB' and (e['src']['time'] // 60) == h
            for k in K
        ) >= freq1[h]
    )
    mdl.add_constraint(
        mdl.sum(
            x[e['src']['id'], e['dst']['id'], k]
            for e in E if e['cap'] == 1 and e['src']['loc'] == 'HSK' and (e['src']['time'] // 60) == h
            for k in K
        ) >= freq2[h]
    )
solution = mdl.solve(log_output=True)

if solution:
    print("Objective:", solution.objective_value)
    used_vehicles = [k for k in K if z[k].solution_value > 0.5]
    print(f"Number of vehicles used: {len(used_vehicles)}\n")

    for k in used_vehicles:
        print(f"Schedule for Vehicle {k + 1}: Utilization time = {T[k].solution_value:.2f}")
        current_node = start_node_id
        while current_node != end_node_id:
            next_arcs = [e for e in E if e['src']['id'] == current_node and x.get((e['src']['id'], e['dst']['id'], k), 0).solution_value > 0.5]
            if not next_arcs:
                print("  ERROR: Route incomplete or disconnected.")
                break
            arc = next_arcs[0]
            src, dst = arc['src'], arc['dst']
            src_h, src_m = divmod(int(src['time']), 60)
            dst_h, dst_m = divmod(int(dst['time']), 60)
            print(f"  ({src['loc']} at {src_h:02d}:{src_m:02d}) --> ({dst['loc']} at {dst_h:02d}:{dst_m:02d}), cost={arc['cost']}")
            current_node = dst['id']
        print()
else:
    print("No feasible solution found.")