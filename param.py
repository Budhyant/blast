import math

class Param:
    def __init__(self, sc_dist, const_u, logScaledDist, list_slope_u_air, list_slope_u_surface, limit, const_y):
        self.sc_dist = sc_dist
        self.u = const_u[0] + const_u[1] * logScaledDist
        self.list_slope_u = [
            list_slope_u_air,
            list_slope_u_surface
        ]
        self.limit = limit
        self.const_y = const_y

    def get_fn_u_pow(self, slope, pow):
        return slope * math.pow(self.u, pow)

    def get_list_fn_u(self, slopes):
        storage = []
        for idx, item in enumerate(slopes):
            storage.append(self.get_fn_u_pow(item, idx + 1))
        return storage

    def get_filtered_result(self):
        for idx, slopes in enumerate(self.list_slope_u):
            list_fn = self.get_list_fn_u(slopes)

            y = self.const_y[idx] + sum(list_fn)
            if self.sc_dist < self.limit['lower_limit']:
                appl_lower_rng_filter = 0
            else:
                appl_lower_rng_filter = y

            if self.sc_dist > self.limit['upper_limit']:
                appl_upper_rng_filter = 0
            else:
                appl_upper_rng_filter = y
            checksum = appl_lower_rng_filter + appl_upper_rng_filter

            if checksum == 2 * y:
                # return y
                print(y)
            else:
                # return 0
                print(0)