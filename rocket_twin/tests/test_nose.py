import numpy as np

from rocket_twin.systems import NoseGeom


class TestNose:
    """Tests for the nose model."""

    def test_run_once(self):
        sys = NoseGeom("sys")

        sys.run_once()

    def test_geometry(self):
        sys = NoseGeom("sys")

        sys.radius = 5.0
        sys.height = 9.0
        sys.rho = 10.0
        sys.pos = 0.0

        sys.run_once()

        np.testing.assert_allclose(sys.props.Mass(), 750 * np.pi, atol=10 ** (-2))

        np.testing.assert_allclose(sys.props.CentreOfMass().X(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Y(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Z(), 2.25, atol=10 ** (-2))

        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().X(), 6.7875 * 750 * np.pi, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Y(), 6.7875 * 750 * np.pi, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Z(), 7.5 * 750 * np.pi, atol=10 ** (-2)
        )
