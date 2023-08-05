import math as m
import random as r
import numpy as np

import continuous_distributions as st

class norm_hyp(st.Norm_rv):

    def __init__(self, mean, variance, H0, HA, type):

        # might not want a mean if that's what we're testing,
        # we wouldn't know the mean in advance
        super().__init__(mean, variance)

        #new values of subclass
        self.std_dev = m.sqrt(variance)
        self.H0 = H0
        self.HA = HA
        self.type = type # simple or compound test

    def z_score(self, x):

        """calculate a z score"""

        self.z = (x - self.mean) / (self.variance)
        return self.z

# based on example on p. 2 of hyp testing notes
# based on example on p. 2 of hyp testing notes
class gen_test:

        def __init__(self, data, H0):
            self.data = list(data)
            self.H0 = H0

        def run_test(self, n, counter, accept_left, accept_right):

            sample = r.sample(self.data, n)
            acceptance_region = {accept_left, accept_right}
            rejection_region = (set(i for i in range(1, len(data)))
                                .symmetric_difference(acceptance_region))
            sample_count = sample.count(counter)

            if sample_count in acceptance_region:
                decision = f'Do not reject H0. Count is {sample_count}'
            if sample_count in rejection_region:
                decision = f'Reject the H0. Count is {sample_count}'

            return decision
