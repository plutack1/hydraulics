import math


# constants
AREA = 1500.0  # float(input("research area of sprikler ="))
# This is the remote test area
LENGTH = 67.3  # float(input("Enter length and breadth of sprikler ="))
WIDTH = 47.6  # float(input("Enter breadth of sprikler ="))

# This is the sesign area for density area graph
MAX_COVERAGE = 120  # int(input("max_coverage of sprikler ="))
# the maximum area that can be covered by a sprinkler
# MAX_COVERAGE = int(input("max_coverage of sprikler ="))

MAX_SPACING = 12
# the maximum spacing basd of nfpa standard

# MIN_DISTANCE = int(input("min_spacing of sprikler ="))
c_pipe = 120  # int(input("coefficent of pipe"))
# this is the coefficient of the type of pipe used
br_line_int_dia = 1.682  # float(input("branch line diameter"))
# the internal diameter of the branch line pipes
br2_line_int_dia = 2.157
cr_line_int_dia = 3.260
int_dia_sch40_1_5inch = 1.610  # float(input("cross line diameter"))
int_dia_sch40_2inch = 2.067  # float(input("cross line diameter"))
int_dia_sch40_3inch = 3.068  # float(input("cross line diameter"))
# the internal diameter of the crossmain line pipes
t_fitt_sch40_3inch = 15
t_fitt_sch40_2inch = 10
t_fitt_sch40_1_5inch = 8
l_equiv_main = 18.31  # float(input("equivaleth of cross main fitting"))
l_equiv_branch = 30.66  # float(input("equivaleth of branch fitting"))
k = 8  # int(input("sprinkler coefficient"))

no_of_branch_lines = math.ceil(WIDTH / MAX_SPACING)
dist_between_branch_lines = WIDTH / no_of_branch_lines
no_of_sprinkler_on_branch_lines = math.ceil(LENGTH / MAX_SPACING)
DIST_OF_SPRINKLER_ON_BRANCH_LINES = LENGTH / no_of_sprinkler_on_branch_lines
# spacing_between_sprinklers =
calc_coverage_area = dist_between_branch_lines * DIST_OF_SPRINKLER_ON_BRANCH_LINES
# variables
# density = (0.1 * (DESIGN_AREA - 2500) / 2500) + 0.2
density = 0.2
calc_coverage_area_check = True
calc_design_area_check = True
addition = False

while calc_coverage_area_check is True:
    if calc_coverage_area < MAX_COVERAGE:
        branch_line_wall_dist = (
            WIDTH - (no_of_branch_lines * dist_between_branch_lines / 2)
        ) / 2
        last_sprinkler_wall_dist = (
            LENGTH
            - (
                (no_of_sprinkler_on_branch_lines - 1)
                * DIST_OF_SPRINKLER_ON_BRANCH_LINES
            )
        ) / 2
        largest_area = (
            branch_line_wall_dist
            + (dist_between_branch_lines / 2)
            + last_sprinkler_wall_dist
            + (DIST_OF_SPRINKLER_ON_BRANCH_LINES / 2)
        )
        if dist_between_branch_lines * DIST_OF_SPRINKLER_ON_BRANCH_LINES > largest_area:
            largest_area = dist_between_branch_lines * DIST_OF_SPRINKLER_ON_BRANCH_LINES
        if largest_area < MAX_COVERAGE:
            min_length = 1.2 * AREA ** (1 / 2)
            min_sprinkler_on_branch = math.ceil(
                (min_length / DIST_OF_SPRINKLER_ON_BRANCH_LINES)
            )
            actual_length = (
                min_sprinkler_on_branch - 0.5
            ) * DIST_OF_SPRINKLER_ON_BRANCH_LINES + last_sprinkler_wall_dist
            width = AREA / actual_length
            sprinkler_across_branch = math.ceil((width / dist_between_branch_lines))
            calc_design_area = actual_length * width
            add_node = 0
            while calc_design_area_check is True:
                if calc_design_area < AREA:
                    calc_design_area += calc_coverage_area
                    add_node += 1
                else:
                    calc_design_area_check = False
            no_of_sprinkler = (
                min_sprinkler_on_branch * sprinkler_across_branch
            ) + add_node
        calc_coverage_area_check = False
    else:
        no_of_branch_lines += 1
        dist_between_branch_lines = WIDTH / no_of_branch_lines
        calc_coverage_area = (
            dist_between_branch_lines * DIST_OF_SPRINKLER_ON_BRANCH_LINES
        )


all_discharge_rate = []
flow_rate_end = 0
all_flowrate = []
all_pressure = []
inverted_pressure_add = []
inverted_discharge_add = []
inverted_flowrate = []
pressure_add = 0
og_flowrate_end = 0
v = 0


def pressure(q, k=k):
    pressure = (q / k) ** 2
    return pressure


def discharge_rate(p, k=k):
    discharge_rate = k * p ** (1 / 2)
    return discharge_rate


node1_discharge_rate = calc_coverage_area * density
node1_pressure = pressure(q=node1_discharge_rate)


def pressure_drop(q, l_eqv, d, C=c_pipe):
    p_drop = 4.72 * q**1.85 * l_eqv / (C**1.85 * d**4.87)
    return p_drop


def equiv_length_t(l, d_1, d_2, fitt_equiv):
    equiv_length_t = l + ((d_1 / d_2) ** 4.87 * fitt_equiv)
    return equiv_length_t


for m in range(1, no_of_branch_lines + 1):
    if m == 1:
        all_pressure.append(node1_pressure)
        all_discharge_rate.append(node1_discharge_rate)
        pressure = node1_pressure
        flow_rate_end += node1_discharge_rate
        all_flowrate.append(flow_rate_end)
        for n in range(2, no_of_sprinkler_on_branch_lines + 2):
            # if n == 1:
            #     p_drop = pressure_drop(
            #         q=node1_discharge_rate,
            #         l_eqv=DIST_OF_SPRINKLER_ON_BRANCH_LINES,
            #         d=br_line_int_dia,
            #     )
            #     pressure += p_drop
            #     all_pressure.append(pressure)
            #     print(flow_rate_end)

            if n < no_of_sprinkler_on_branch_lines:
                if n < no_of_sprinkler_on_branch_lines - 1:
                    p_drop = pressure_drop(
                        q=flow_rate_end,
                        l_eqv=DIST_OF_SPRINKLER_ON_BRANCH_LINES,
                        d=br_line_int_dia,
                    )
                    pressure += p_drop
                    discharge = discharge_rate(p=pressure)
                    all_discharge_rate.append(discharge)
                    flow_rate_end += discharge
                    all_flowrate.append(flow_rate_end)
                    all_pressure.append(pressure)
                    print(flow_rate_end)
                else:
                    p_drop = pressure_drop(
                        q=flow_rate_end,
                        l_eqv=DIST_OF_SPRINKLER_ON_BRANCH_LINES,
                        d=br2_line_int_dia,
                    )
                    pressure += p_drop
                    discharge = discharge_rate(p=pressure)
                    all_discharge_rate.append(discharge)
                    flow_rate_end += discharge
                    all_flowrate.append(flow_rate_end)
                    all_pressure.append(pressure)
                    print(flow_rate_end)
                # junc_flowrate_end =flow_rate_end

            elif n == no_of_sprinkler_on_branch_lines:
                length = equiv_length_t(
                    l=DIST_OF_SPRINKLER_ON_BRANCH_LINES / 2,
                    d_1=br2_line_int_dia,
                    d_2=int_dia_sch40_2inch,
                    fitt_equiv=t_fitt_sch40_2inch,
                )
                p_drop = pressure_drop(
                    q=flow_rate_end, l_eqv=length, d=br2_line_int_dia
                )
                pressure += p_drop
                all_pressure.append(pressure)
                all_discharge_rate.append(0)
                print(flow_rate_end)
            elif n == no_of_sprinkler_on_branch_lines + 1:
                discharge_last = node1_discharge_rate
                pressure_last = node1_pressure
                length = equiv_length_t(
                    l=DIST_OF_SPRINKLER_ON_BRANCH_LINES / 2,
                    d_1=br_line_int_dia,
                    d_2=int_dia_sch40_1_5inch,
                    fitt_equiv=t_fitt_sch40_1_5inch,
                )
                p_drop = pressure_drop(
                    q=discharge_last, l_eqv=length, d=br_line_int_dia
                )
                discharge_last = (
                    (all_pressure[len(all_pressure) - 1]) ** (1 / 2)
                    * discharge_last
                    / (pressure_last + p_drop) ** (1 / 2)
                )
                all_discharge_rate.append(discharge_last)
                all_flowrate.append(discharge_last)
                p_drop = pressure_drop(
                    q=discharge_last, l_eqv=length, d=br_line_int_dia
                )
                all_pressure.append(all_pressure[len(all_pressure) - 1] - p_drop)
                flow_rate_end += discharge_last  # corrected with 6

        
                main_pressure = all_pressure
                main_discharge_rate = all_discharge_rate

    elif m > 1:
        for n in range(no_of_sprinkler_on_branch_lines, 0, -1):
            if n == no_of_sprinkler_on_branch_lines:
                inverted_discharge_add.append(0)
                # f1 corrected with 5-11 pressure drop
                length = equiv_length_t(
                    l=dist_between_branch_lines,
                    d_1=cr_line_int_dia,
                    d_2=int_dia_sch40_3inch,
                    fitt_equiv=t_fitt_sch40_3inch,
                )
                p_drop = pressure_drop(q=flow_rate_end, l_eqv=length, d=cr_line_int_dia)
                pressure_add = all_pressure[len(all_pressure) - 2] + p_drop
                inverted_pressure_add.append(pressure_add)
                og_flowrate_end += flow_rate_end
                all_flowrate.append(og_flowrate_end)
                og1_flowrate_end = all_flowrate[no_of_sprinkler_on_branch_lines-2]
                # og2_flowrate_end = sum(
                #     all_discharge_rate[v : len(all_discharge_rate) - 3]
                # )
                og2_flow_rate_end_corr = (
                    og1_flowrate_end
                    * ((inverted_pressure_add[len(inverted_pressure_add) - 1]) ** (1 / 2))
                    / (main_pressure[len(main_pressure) - 2]) ** (1 / 2)
                )
                v += 6
                inverted_flowrate.append(og2_flow_rate_end_corr)
                og_flowrate_end += og2_flow_rate_end_corr
            elif n == no_of_sprinkler_on_branch_lines - 1:
                length = equiv_length_t(
                    l=DIST_OF_SPRINKLER_ON_BRANCH_LINES / 2,
                    d_1=br2_line_int_dia,
                    d_2=int_dia_sch40_2inch,
                    fitt_equiv=t_fitt_sch40_2inch,
                )
                p_drop = pressure_drop(
                    q=og2_flow_rate_end_corr, l_eqv=length, d=br2_line_int_dia
                )
                pressure_add = inverted_pressure_add[0] - p_drop
                inverted_pressure_add.append(pressure_add)
                discharge = discharge_rate(p=pressure_add)
                inverted_discharge_add.append(discharge)
                og2_flow_rate_end_corr -= discharge
                inverted_flowrate.append(og2_flow_rate_end_corr)

            elif n <= no_of_sprinkler_on_branch_lines - 2:
                if n == no_of_sprinkler_on_branch_lines - 1:
                    p_drop = pressure_drop(
                        q=og2_flow_rate_end_corr,
                        l_eqv=DIST_OF_SPRINKLER_ON_BRANCH_LINES,
                        d=br2_line_int_dia,
                    )
                    pressure_add = (
                        inverted_pressure_add[len(inverted_pressure_add) - 1] - p_drop
                    )
                    inverted_pressure_add.append(pressure_add)
                    discharge = discharge_rate(p=pressure_add)
                    inverted_discharge_add.append(discharge)
                    og2_flow_rate_end_corr -= discharge
                    inverted_flowrate.append(og2_flow_rate_end_corr)
                else:
                    if n == no_of_sprinkler_on_branch_lines - 2:
                        p_drop = pressure_drop(
                            q=og2_flow_rate_end_corr,
                            l_eqv=DIST_OF_SPRINKLER_ON_BRANCH_LINES,
                            d=br2_line_int_dia,
                        )
                        pressure_add = (
                            inverted_pressure_add[len(inverted_pressure_add) - 1] - p_drop
                        )
                        inverted_pressure_add.append(pressure_add)
                        discharge = discharge_rate(p=pressure_add)
                        inverted_discharge_add.append(discharge)
                        og2_flow_rate_end_corr -= discharge
                        inverted_flowrate.append(og2_flow_rate_end_corr)
                    else:
                        p_drop = pressure_drop(
                            q=og2_flow_rate_end_corr,
                            l_eqv=DIST_OF_SPRINKLER_ON_BRANCH_LINES,
                            d=br_line_int_dia,
                        )
                        pressure_add = (
                            inverted_pressure_add[len(inverted_pressure_add) - 1] - p_drop
                        )
                        inverted_pressure_add.append(pressure_add)
                        discharge = discharge_rate(p=pressure_add)
                        inverted_discharge_add.append(discharge)
                        og2_flow_rate_end_corr -= discharge
                        if n != 1:
                            inverted_flowrate.append(og2_flow_rate_end_corr)
                        if n == 1:
                            length = equiv_length_t(
                                l=DIST_OF_SPRINKLER_ON_BRANCH_LINES/2,
                                d_1=br_line_int_dia,
                                d_2=int_dia_sch40_1_5inch,
                                fitt_equiv=t_fitt_sch40_1_5inch,
                            )
                            p_drop = pressure_drop(
                                q=node1_discharge_rate, l_eqv=length, d=br_line_int_dia
                            )
                            all_pressure.extend(list(reversed(inverted_pressure_add)))
                            all_flowrate.extend(list(reversed(inverted_flowrate)))
                            discharge = (
                                node1_discharge_rate
                                * (all_pressure[len(all_pressure) - 1]) ** (1 / 2)
                                / (node1_pressure + p_drop) ** (1 / 2)
                            )
                            all_discharge_rate.extend(
                                list(reversed(inverted_discharge_add))
                            )
                            all_discharge_rate.append(discharge)
                            all_flowrate.append(discharge)
                            p_drop = pressure_drop(
                                q=discharge, l_eqv=length, d=br_line_int_dia
                            )
                            all_pressure.append(
                                all_pressure[len(all_pressure) - 1] - p_drop
                            )
                            inverted_discharge_add = []
                            inverted_pressure_add = []
                            inverted_flowrate = []
                            og_flowrate_end += all_discharge_rate[
                                len(all_discharge_rate) - 1
                            ]
                            flow_rate_end = og_flowrate_end


print(all_discharge_rate)
print(all_pressure)
print(flow_rate_end)
print(f"no of discharge rate= {len(all_discharge_rate)}")
print(f"no of pressure= {len(all_pressure)}")
print(f"no of sprinklers= {no_of_sprinkler_on_branch_lines *no_of_branch_lines}")
