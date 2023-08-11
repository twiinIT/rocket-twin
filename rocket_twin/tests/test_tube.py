import numpy as np

from rocket_twin.systems import TubeGeom


class TestTube:
    """Tests for the tube model."""

    def test_run_once(self):
        sys =TubeGeom('sys')

        sys.run_once()
        
    def test_geometry(self):
        sys = TubeGeom("sys")

        sys.radius = 5.0
        sys.length = 9.0
        sys.rho = 10.0
        sys.pos = 0.0

        sys.run_once()

        np.testing.assert_allclose(sys.props.Mass(), 2250 * np.pi, atol=10 ** (-2))

        np.testing.assert_allclose(sys.props.CentreOfMass().X(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Y(), 0.0, atol=10 ** (-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Z(), 4.5, atol=10 ** (-2))

        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().X(), 13 * 2250 * np.pi, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Y(), 13 * 2250 * np.pi, atol=10 ** (-2)
        )
        np.testing.assert_allclose(
            sys.props.MatrixOfInertia().Diagonal().Z(), 12.5 * 2250 * np.pi, atol=10 ** (-2)
        )
