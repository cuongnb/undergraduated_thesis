"""
Created : 10/04/2017
@author : Cuong Nguyen Ba
"""

import math

import numpy as n
from scipy.special import gammaln, psi


# n.random.seed(100000001)
class VbObtm(object):
    def __init__(self, num_term, num_topic, alpha, beta,
                 stepCount, stepPower, stepOffset, r_drop):
        self._W = num_term
        self._K = num_topic

        self._r_drop = r_drop

        self._alpha = alpha
        self._beta = beta

        self._stepCount = stepCount
        self._stepPower = stepPower
        self._stepOffset = stepOffset

        self._phi = 1 * n.random.gamma(100.0, 1.0 / 100.0, (self._K, self._W))
        self._theta = 1 * n.random.gamma(100.0, 1.0 / 100.0, (1, self._K))

        # normalize phi
        _phi_norm = self._phi.sum(axis=1)
        self._phi /= _phi_norm[:, n.newaxis]
        # normalize theta
        self._theta /= sum(self._theta)

        self._thetaSS = n.zeros(self._K)
        self._phiSS = n.zeros((self._K, self._W))

        self._alphaVec = n.ones(self._K) * alpha
        self._betaMat = n.ones((self._K, self._W)) * beta

    def fitMiniBatch(self, biterm1ids, biterm2ids):
        self._stepCount += 1
        c_thetaSS = n.zeros(self._K)
        t_nk = n.zeros(self._K)
        c_phiSS = n.zeros((self._K, self._W))

        n_biterm = len(biterm1ids)
        # if self._r_drop == 0:
        for i in range(0, n_biterm):
            # print biterm1ids[i]
            t_nk[:] = self._theta * self._phi[:, biterm1ids[i]] * self._phi[:, biterm2ids[i]]
            t_nk /= sum(t_nk)

            c_thetaSS += t_nk
            c_phiSS[:, biterm1ids[i]] += t_nk
            c_phiSS[:, biterm2ids[i]] += t_nk

        c_thetaSS /= n_biterm
        c_phiSS /= n_biterm

        if self._stepCount == 1:
            self._thetaSS = c_thetaSS
            self._phiSS = c_phiSS
        else:
            stepSize = math.pow(self._stepCount + self._stepOffset, - self._stepPower)
            self._thetaSS = (1 - stepSize) * self._thetaSS + stepSize * c_thetaSS
            self._phiSS = (1 - stepSize) * self._phiSS + stepSize * c_phiSS

        # update and norm theta
        self._theta = self._thetaSS + self._alpha
        self._theta /= sum(self._theta)
        # update and norm phi
        self._phi = self._phiSS + self._betaMat
        # normalize phi
        _phi_norm = self._phi.sum(axis=1)
        self._phi /= _phi_norm[:, n.newaxis]
        return (self._phi, self._theta)
