import numpy as np
from rocket_twin.systems import Engine
from cosapp.drivers import RungeKutta

class TestEngine:

    def test_geom(self):
        sys = Engine('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"geom.base_radius" : 3.,
                "geom.top_radius" : 1.,
                "geom.height" : 2.,
                "geom.rho" : 15/(13*np.pi),
                "geom.pos" : 0.}

        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.props.Mass(), 10., atol=10 ** (-2))

        np.testing.assert_allclose(sys.props.CentreOfMass().X(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Y(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Z(), 0.692, atol=10 ** (-2))

        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().X(), 16.553, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Y(), 16.553, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Z(), 27.923, atol=10 ** (-2)
        )

    def test_perfo(self):
        sys = Engine('sys')
        driver = sys.add_driver(RungeKutta(order=4, dt=0.1))
        driver.time_interval = (0, 5)

        init = {"perfo.w_out" : 10.,
                "perfo.isp" : 20.,
                "perfo.g_0" : 10.}
        
        driver.set_scenario(init=init)

        sys.run_drivers()

        np.testing.assert_allclose(sys.force, 2000., atol=10**(-5))