import math
# from math import exp, expm1

# soDistance = input("please enter the actual stand-off distance (D) [m]: ")
# neQuantity = input("please enter the net explosive quantity (Q) [kg]: ")

soDist = 25
neQty = 25
TNT_EQ_FIGURE = 1

TNT_EQ_Fig = None
while True:
    TNT_EQ_FigInput = input("select explosive type:\n1. TNT\n2.RDX (Cyclonite)\n3. HMX \n4. Nitroglycerin (liquid)\n"
                            "5. Compund B (60% RDX 40% TNT)\n6. Semtex\n7. 60% Nitroglycerin dynamite\n\n"
                            "your selected type: ")
    if TNT_EQ_FigInput == '1':
        TNT_EQ_Fig = 1
        break
    elif TNT_EQ_FigInput == '2':
        TNT_EQ_Fig = 1.185
        break
    elif TNT_EQ_FigInput == '3':
        TNT_EQ_Fig = 1.256
        break
    elif TNT_EQ_FigInput == '4':
        TNT_EQ_Fig = 1.481
        break
    elif TNT_EQ_FigInput == '5':
        TNT_EQ_Fig = 1.148
        break
    elif TNT_EQ_FigInput == '6':
        TNT_EQ_Fig = 1.25
        break
    elif TNT_EQ_FigInput == '7':
        TNT_EQ_Fig = 0.6
        break
    else:
        raise SystemExit("you should select from the options")

TNT_EQ_WT = neQty * TNT_EQ_Fig
scDist = soDist / math.pow(TNT_EQ_WT, 0.3333)
logScaledDist = math.log(scDist, 10)

# ----------------------------------------------------
# get Ps


def get_fn_u_pow(ps_u, slope, pow):
    return slope * math.pow(ps_u, pow)


def get_list_fn_u(u, list_slop_u):
    storage = []
    for idx, item in enumerate(list_slop_u):
        storage.append(get_fn_u_pow(u, item, idx + 1))
    return storage

ps_u = -0.214362789151 + 1.35034249993 * logScaledDist
# print(ps_u)

list_slope_ps_u_air = [
    -1.69012801396,
    0.00804973591951,
    0.336743114941,
    -0.00516226351334,
    -0.0809228619888,
    -0.00478507266747,
    0.00793030472242,
    0.0007684469735
]

list_slope_ps_u_surface = [
    -1.6958988741,
    -0.154159376846,
    0.514060730593,
    0.0988534365274,
    -0.293912623038,
    -0.0268112345019,
    0.109097496421,
    0.00162846756311,
    - 0.0214631030242,
    0.0001456723382,
    0.00167847752266,
]

list_slope_ps_u = [
    list_slope_ps_u_air,
    list_slope_ps_u_surface
]

arr_const_y_p_s = [
    2.611368669,
    2.78076916577
]

for idx, slopes in enumerate(list_slope_ps_u):
    list_fn_ps_u = get_list_fn_u(ps_u, slopes)
    # print('idx: ', idx, 'list_fn_ps_u', list_fn_ps_u)

    ps_y = arr_const_y_p_s[idx] + sum(list_fn_ps_u)
    # print('ps_y', ps_y)

    appl_lower_rng_filter = None
    appl_upper_rng_filter = None

    if scDist < 0.0531:
        appl_lower_rng_filter = 0
    else:
        appl_lower_rng_filter = ps_y
    # print(appl_lower_rng_filter)

    if scDist > 40:
        appl_upper_rng_filter = 0
    else:
        appl_upper_rng_filter = ps_y
    ps_checksum = appl_lower_rng_filter + appl_upper_rng_filter

    filtered_result = None
    if ps_checksum == 2 * ps_y:
        filtered_result = ps_y
    else:
        filtered_result = 0

    ps_anti_log_y = None
    if filtered_result == 0:
        ps_anti_log_y = 0
    else:
        ps_anti_log_y = 10 ** ps_y

    # print(ps_anti_log_y)

    if filtered_result == 0:
        raise SystemExit("filtered result = 0")
    else:
        p_s = ps_anti_log_y

    print('Ps: ', p_s)

