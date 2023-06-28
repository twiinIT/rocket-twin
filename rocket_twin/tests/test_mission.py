import numpy as np

from rocket_twin.drivers.mission import Mission
from rocket_twin.systems import Ground


class TestMission:
    def test_run_once(self):
        sys = Ground("sys")
        sys.g_tank.weight_p = sys.g_tank.weight_max
        sys.rocket.tank.weight_p = 0.0
        w_in = 3.0
        w_out = 3.0
        dt = 0.1

        sys.add_driver(Mission("mission", w_in=w_in, w_out=w_out, dt=dt, owner=sys))

        sys.run_drivers()

        data = sys.drivers["mission"].data
        data = data.drop(["Section", "Status", "Error code"], axis=1)

        np.testing.assert_allclose(sys.rocket.dyn.a, 40.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.rocket.tank.weight_p, 0.0, atol=10 ** (-10))
        np.testing.assert_allclose(sys.g_tank.weight_p, 5.0, atol=10 ** (-10))


test_mission = TestMission()
test_mission.test_run_once()
print("Mission complete!")
