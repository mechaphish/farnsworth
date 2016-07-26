#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals


class CBScoreMixin(object):
    @property
    def cqe_performance_score(self):
        """
        Compute perf score from corresponding overheads using CQE formula.
        :return: performance score, [0.0, 1.0]
        """
        # Computed according to the CQE scoring manual
        # https://cgc.darpa.mil/CQE_Scoring.pdf
        perf_score = None
        perf_factor = 1 + max(0.25 * self.size_overhead,
                              self.memory_overhead,
                              self.time_overhead)

        if 0 <= perf_factor < 1.10:
            perf_score = 1
        elif 1.10 <= perf_factor < 1.62:
            perf_score = (perf_factor - 0.1) ** -4
        elif 1.62 <= perf_factor < 2:
            perf_score = (-1 * 0.493 * perf_factor) + 0.986
        else:
            perf_score = 0

        return perf_score

    @property
    def cqe_functionality_score(self):
        """
        Compute functionality score from functionality factor using CQE formula.
        :return: functionality score [0.0, 1.0]
        """
        func_factor = self.success

        func_score = 0.0
        if func_factor == 1:
            func_score = 1.0
        elif 0.40 <= func_factor < 1:
            func_score = (2 - func_factor) ** (-4)
        elif 0 < func_factor < 0.40:
            func_score = 0.381 * func_factor
        else:
            func_score = 0
        return float(func_score)

    @property
    def availability(self):
        return min(self.cqe_performance_score, self.cqe_functionality_score)

    @property
    def cb_score(self):
        return self.availability * self.security
