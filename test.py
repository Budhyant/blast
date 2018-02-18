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

'''
    get Is F(I) for Air
'''

obj_is_f1 = {
    'sc_dist': sc_dist,
    'log_sc_dist': log_sc_dist,
    'const_u_air': [
        2.34723921354,
        3.24299066475
    ],
    'const_u_surface': [
        2.06761908721,
        3.0760329666
    ],

    'list_slope_u_air': [
        -0.443749377691,
        0.168825414684,
        0.0348138030308,
        -0.010435192824
    ],

    'list_slope_u_surface': [
        -0.502992763686,
        0.171335645235,
        0.0450176963051,
        -0.0118964626402
    ],

    'const_y': [
        2.38830516757,
        2.52455620925
    ],

    'limits': [
        {
            'lower_limit': 0.0531,
            'upper_limit': 0.792
        },
        {
            'lower_limit': 0.0674,
            'upper_limit': 0.955
        }
    ]
}

is_f1 = Param(obj_is_f1)
is_f1_ft_result = is_f1.get_ft_result()
print('is_f1 ft result', is_f1_ft_result)


# ps_anti_log = None
# for y in ps_ys:
#     if y == 0:
#         raise SystemExit("filtered result: 0")
#     else:
#         p_s = math.pow(10, y)
#         print('Ps: ', p_s)

'''
    get Is F(II) for Air
'''
obj_is_f2 = {
    'sc_dist': sc_dist,
    'log_sc_dist': log_sc_dist,
    'const_u_air': [
        -1.75305660315,
        2.30629231803
    ],
    'const_u_surface': [
        -1.94708846747,
        2.40697745406
    ],

    'list_slope_u_air': [
        -0.40463292088,
        -0.0142721946082,
        0.00912366316617,
        -0.0006750681404,
        -0.00800863718901,
        0.00314819515931,
        0.00152044783382,
        -0.0007470265899
    ],

    'list_slope_u_surface': [
        -0.384519026965,
        -0.0260816706301,
        0.00595798753822,
        0.0145445261077,
        -0.00663289334734,
        -0.00284189327204,
        0.0013644816227
    ],

    'const_y': [
        1.55197227115,
        1.67281645863
    ],

    'limits': [
        {
            'lower_limit': 0.792,
            'upper_limit': 40
        },
        {
            'lower_limit': 0.955,
            'upper_limit': 40
        }
    ]
}

is_f2 = Param(obj_is_f2)
is_f2_ft_result = is_f2.get_ft_result()
print('is_f2 ft result', is_f2_ft_result)

'''
    get Pr
'''

obj_pr = {
    'sc_dist': sc_dist,
    'log_sc_dist': log_sc_dist,
    'const_u_air': [
        -0.214362789151,
        1.35034249993
    ],
    'const_u_surface': [
        -0.240657322658,
        1.3663771922
    ],

    'list_slope_u_air': [
        -2.21400538997,
        0.035119031446,
        0.657599992109,
        0.0141818951887,
        -0.243076636231,
        -0.0158699803158,
        0.0492741184234,
        0.00227639644004,
        -0.00397126276058
    ],

    'list_slope_u_surface': [
        -2.21030870597,
        -0.218536586295,
        0.895319589372,
        0.24989009775,
        -0.569249436807,
        -0.11791682383,
        0.224131161411,
        0.0245620259375,
        -0.0455116002694,
        -0.0019093073888,
        0.00361471193389
    ],

    'const_y': [
        3.22958031387,
        3.40283217581
    ],

    'limits': [
        {
            'lower_limit': 0.0531,
            'upper_limit': 40
        },
        {
            'lower_limit': 0.0674,
            'upper_limit': 40
        }
    ]
}

pr = Param(obj_pr)
pr_ft_result = pr.get_ft_result()
print('pr ft result', pr_ft_result)

'''
    get Ir
'''

obj_ir = {
    'sc_dist': sc_dist,
    'log_sc_dist': log_sc_dist,
    'const_u_air': [
        -0.204004553231,
        1.37882996018
    ],
    'const_u_surface': [
        -0.246208804814,
        1.33422049854
    ],

    'list_slope_u_air': [
        -0.903118886091,
        0.101771877942,
        -0.0242139751146
    ],

    'list_slope_u_surface': [
        -0.949516092853,
        0.112136118689,
        -0.0250659183287
    ],

    'const_y': [
        2.55875660396,
        2.70588058103
    ],

    'limits': [
        {
            'lower_limit': 0.0531,
            'upper_limit': 40
        },
        {
            'lower_limit': 0.0674,
            'upper_limit': 40
        }
    ]
}

ir = Param(obj_ir)
ir_ft_result = ir.get_ft_result()
print('ir_ft_result', ir_ft_result)
