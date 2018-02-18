import math


class Param:
    big_y_air = None
    big_y_surface = None
    ft_result_air = None
    ft_result_surface = None

    sc_dist = 0
    const_u_air = 0
    const_u_surface = 0
    log_scale_dist = 0
    list_slope_u = []
    limits = []
    const_y = []

    def __init__(self, obj):
        self.sc_dist = obj['sc_dist']
        self.u_air = obj['const_u_air'][0] + obj['const_u_air'][1] * obj['log_sc_dist']
        self.u_surface = obj['const_u_surface'][0] + obj['const_u_surface'][1] * obj['log_sc_dist']
        self.list_slope_u = [
            obj['list_slope_u_air'],
            obj['list_slope_u_surface']
        ]
        self.limits = obj['limits']
        self.const_y = obj['const_y']

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
        # print('self.list_slope_u', self.list_slope_u)
        for idx, slopes in enumerate(self.list_slope_u):
            list_fn = self.get_list_fn_u(slopes, idx)
            # print('slopes', idx, slopes)
            y = self.const_y[idx] + sum(list_fn)
            # print('idx', idx, 'y', y)
            if idx == 0:
                self.big_y_air = y
            else:
                self.big_y_surface = y
        return [
            self.big_y_air,
            self.big_y_surface
        ]

    def get_ft_result(self):
        ys = self.get_y()
        # print('ys', ys)
        limits = self.limits
        # print('limits', limits)
        sc_dist = self.sc_dist
        storage_ft_result = []
        for idx, y in enumerate(ys):
            limit = limits[idx]
            if sc_dist < limit['lower_limit']:
                application_low_rng_filter = 0
            else:
                application_low_rng_filter = y
            if sc_dist > limit['upper_limit']:
                application_up_rng_filter = 0
            else:
                application_up_rng_filter = y
            checksum = application_low_rng_filter + application_up_rng_filter
            if checksum == 2 * y:
                storage_ft_result.append(y)
            else:
                storage_ft_result.append(0)
        return storage_ft_result
