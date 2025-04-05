import numpy as _np
import matplotlib.pyplot as _plt
import math as _m
import func_guesser as _fg


sign = _fg.sign


def lognorm(sigma):
    z = _np.random.normal(0, sigma)
    return _np.exp(z)


class Simulator:
    def __init__(self, max_speed, max_accel, drag, noise):
        self.max_speed = max_speed
        self.max_accel = max_accel
        self.dt = 3 / 1000
        self.drag = drag
        self.noise = noise


    def sim(self, power, max_t=10, v_init=0):
        t = _np.arange(0, max_t, self.dt)
        x, v, a, p = _np.zeros_like(t), _np.zeros_like(t), _np.zeros_like(t), _np.zeros_like(t)

        for i in range(t.size):
            if i == 0:
                x[i] = 0
                v[i] = v_init
                a[i] = 0
            else:
                x[i] = x[i - 1] + v[i - 1] * self.dt
                v[i] = v[i - 1] + a[i - 1] * self.dt

                p[i] = power(t[i], x[i - 1], v[i - 1], a[i - 1])
                p[i] = min(max(p[i], -1), 1)

                back_emf = -self.max_accel * v[i - 1] / self.max_speed
                ad = p[i] * self.max_accel + back_emf
                d = -self.drag * sign(v[i])

                stopped = sign(v[i - 1]) * sign(v[i]) != 1
                if stopped and abs(ad) < abs(self.drag):
                    a[i] = 0
                    v[i] = 0
                else:
                    err = lognorm(self.noise * _np.sqrt(self.dt))
                    a[i] = (ad + d) * err

        return t, x, v, a, p
    

    def plot_curves(self, all_arrays, tgt_x=None):
        t, x, v, a, p = all_arrays
        _plt.figure(figsize=(20, 12))
        _plt.subplot(411)
        if tgt_x is not None:
            _plt.hlines(tgt_x, t.min(), t.max(), colors='orange')
        _plt.plot(t, x, label='x')
        _plt.legend()
        _plt.subplot(412)
        _plt.plot(t, v, label='v')
        _plt.legend()
        _plt.subplot(413)
        _plt.plot(t, a, label='a')
        _plt.legend()
        _plt.subplot(414)
        _plt.plot(t, p, label='p')
        _plt.legend()
        _plt.show()


def fit_ks_and_kv(sim:Simulator):
    # determine ks and kv
    trial_pow = _np.linspace(0, 0.25, 10)
    term_vel = _np.ones_like(trial_pow)
    for i in range(trial_pow.size):
        ac = sim.sim(lambda *args: trial_pow[i])
        t, x, v, a, p = ac
        term_vel[i] = v[-1]

    m = term_vel > 0.5
    kv, ks = _np.polyfit(term_vel[m], trial_pow[m], 1)

    return float(ks), float(kv)


def fit_ka(sim, ks, kv):
    # determine ka
    ka_accel = 1
    ka_dist = 2

    sim_time = _m.sqrt(2 * ka_dist / ka_accel)

    def ka_trial(ka):
        def f(t, *args):
            v = ka_accel * t        
            return ks + kv * v + ka * ka_accel

        ac = sim.sim(f, sim_time)
        x = ac[1]
        return x[-1]
    
    fg = _fg.FuncGuesser(ka_dist, 0.01, False)

    p0, p1 = 0.05, 4

    fg.eval(p0, ka_trial(p0))
    fg.eval(p1, ka_trial(p1))
    while not fg.has_result():
        ka = fg.guess()
        fg.eval(ka, ka_trial(ka))

    ka = fg.result().x
    
    return ka