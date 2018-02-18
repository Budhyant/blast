import math
from param import Param
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
sc_dist = soDist / math.pow(TNT_EQ_WT, 0.3333)
log_sc_dist = math.log(sc_dist, 10)


"""
    get Ps
"""
obj_ps = {
    'sc_dist': sc_dist,
    'log_sc_dist': log_sc_dist,
    'const_u_air': [
        -0.214362789151,
        1.35034249993
    ],
    'const_u_surface': [
        -0.214362789151,
        1.35034249993
    ],

    'list_slope_u_air': [
        -1.69012801396,
        0.00804973591951,
        0.336743114941,
        -0.00516226351334,
        -0.0809228619888,
        -0.00478507266747,
        0.00793030472242,
        0.0007684469735
    ],

    'list_slope_u_surface': [
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
    ],

    'const_y': [
        2.611368669,
        2.78076916577
    ],

    'limits': [
        {
            'lower_limit': 0.0531,
            'upper_limit': 40
        },
        {
            'lower_limit': 0.064,
            'upper_limit': 40
        }
    ]
}
# const_ps_u_air = [
#     -0.214362789151,
#     1.35034249993
# ]
# const_ps_u_surface = const_ps_u_air

# list_slope_ps_u_air = [
#     -1.69012801396,
#     0.00804973591951,
#     0.336743114941,
#     -0.00516226351334,
#     -0.0809228619888,
#     -0.00478507266747,
#     0.00793030472242,
#     0.0007684469735
# ]

# list_slope_ps_u_surface = [
#     -1.6958988741,
#     -0.154159376846,
#     0.514060730593,
#     0.0988534365274,
#     -0.293912623038,
#     -0.0268112345019,
#     0.109097496421,
#     0.00162846756311,
#     - 0.0214631030242,
#     0.0001456723382,
#     0.00167847752266,
# ]

# list_slope_ps_u = [
#     list_slope_ps_u_air,
#     list_slope_ps_u_surface
# ]

# const_y_p_s = [
#     2.611368669,
#     2.78076916577
# ]

# limits_ps = [
#     {
#         'lower_limit': 0.0531,
#         'upper_limit': 40
#     },
#     {
#         'lower_limit': 0.064,
#         'upper_limit': 40
#     }
# ]


ps = Param(obj_ps)
# ps_ys = ps.get_y()
# print('Y for air and surface', ps_ys)
ps_ft_result = ps.get_ft_result()
print('ps ft result', ps_ft_result)

# ps_anti_log = None
# for y in ps_ys:
#     if y == 0:
#         raise SystemExit("filtered result: 0")
#     else:
#         p_s = math.pow(10, y)
#         print('Ps: ', p_s)

# """
#     get Is F(I) for Air
# """

# const_is_u_air = [
#     2.34723921354,
#     3.24299066475
# ]

# const_is_u_surface = [
#     2.06761908721,
#     3.0760329666
# ]

# list_slope_is_u_air = [
#     -0.443749377691,
#     0.168825414684,
#     0.0348138030308,
#     -0.010435192824,
# ]

# list_slope_is_u_surface = [
#     -0.502992763686,
#     0.171335645235,
#     0.0450176963051,
#     -0.0118964626402
# ]

# limits_is = [
#     {
#         'lower_limit': 0.0531,
#         'upper_limit': 40
#     },
#     {
#         'lower_limit': 0.064,
#         'upper_limit': 40
#     }
# ]

# const_y_i_s = [
#     2.611368669,
#     2.78076916577
# ]

# is_f1 = Param(sc_dist, const_is_u_air, const_is_u_surface, logScaledDist, list_slope_is_u_air, list_slope_is_u_surface, limits_is, const_y_i_s)

# is_ys = is_f1.get_y()
# print('Y for air and surface', is_ys)


# ps_anti_log = None
# for y in ps_ys:
#     if y == 0:
#         raise SystemExit("filtered result: 0")
#     else:
#         p_s = math.pow(10, y)
#         print('Ps: ', p_s)
