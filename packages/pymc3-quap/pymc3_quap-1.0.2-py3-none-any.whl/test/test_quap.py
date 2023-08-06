import unittest

import arviz as az
import numpy as np

import pymc3 as pm

from quap import quap


class TestQuap(unittest.TestCase):
    def test_recovers_analytical_quadratic_approximation_in_normal_with_unknown_mean_and_variance(self):
        y = np.array([2642, 3503, 4358], dtype=np.float64)
        n = y.size

        with pm.Model() as m:
            logsigma = pm.Uniform("logsigma", -100, 100)
            mu = pm.Uniform("mu", -10000, 10000)
            yobs = pm.Normal("y", mu=mu, sigma=pm.math.exp(logsigma), observed=y)
            idata, posterior = quap([mu, logsigma])

        # BDA 3 sec. 4.1 - analytical solution
        bda_map = [y.mean(), np.log(y.std())]
        bda_cov = np.array([[y.var() / n, 0], [0, 1 / (2 * n)]])

        assert np.allclose(posterior.mean, bda_map)
        assert np.allclose(posterior.cov, bda_cov, atol=1e-4)

    def test_hdi_contains_parameters_in_linear_regression(self):
        np.random.seed(1234)
        N = 100
        M = 2
        sigma = 0.2
        X = np.random.randn(N, M)
        A = np.random.randn(M)
        noise = sigma * np.random.randn(N)
        y = X @ A + noise

        with pm.Model() as lm:
            weights = pm.Normal("weights", mu=0, sigma=1, shape=M)
            noise = pm.Exponential("noise", lam=1)
            y_observed = pm.Normal("y_observed", mu=X @ weights, sigma=noise, observed=y)

            idata, _ = quap([weights, noise])

        hdi = az.hdi(idata)
        weight_hdi = hdi.weights.values
        assert np.all(np.bitwise_and(weight_hdi[:, 0] < A, A < weight_hdi[:, 1]))
        assert hdi.noise.values[0] < sigma < hdi.noise.values[1]

    def test_works_with_single_parameter_models(self):
        np.random.seed(1234)
        N = 983
        k = 19

        with pm.Model() as m:
            p = pm.Beta("p", 1, 3)
            y = pm.Binomial("y", p=p, n=N, observed=k)
            idata, _ = quap([p])

        hdi = az.hdi(idata).p.values
        assert np.allclose(hdi, np.array([0.01093989, 0.02734075]))


if __name__ == '__main__':
    unittest.main()
