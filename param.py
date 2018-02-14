import math


class Param:
    big_y_air = None
    big_y_surface = None

    def __init__(self, sc_dist, const_u_air, const_u_surface, log_scale_dist, list_slope_u_air, list_slope_u_surface, limit, const_y):
        self.sc_dist = sc_dist
        self.u_air = const_u_air[0] + const_u_air[1] * log_scale_dist
        self.u_surface = const_u_surface[0] + const_u_surface[1] * log_scale_dist
        self.list_slope_u = [
            list_slope_u_air,
            list_slope_u_surface
        ]
        self.limit = limit
        self.const_y = const_y

    def get_fn_u_pow(self, slope, power, type_idx):
        if type_idx == 0:
            return slope * math.pow(self.u_air, power)
        else:
            return slope * math.pow(self.u_surface, power)

    def get_list_fn_u(self, slopes, type_idx):
        storage = []

        for idx, item in enumerate(slopes):
            storage.append(self.get_fn_u_pow(item, idx + 1, type_idx))
        return storage

    def get_y(self):
        # evaluate result for both air and surface cases
        for idx, slopes in enumerate(self.list_slope_u):
            list_fn = self.get_list_fn_u(slopes, idx)
            # print('slopes', idx, slopes)
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
                if idx == 0:
                    self.big_y_air = y
                else:
                    self.big_y_surface = y
            else:
                if idx == 0:
                    self.big_y_air = 0
                else:
                    self.big_y_surface = 0
        return [
            self.big_y_air,
            self.big_y_surface
        ]