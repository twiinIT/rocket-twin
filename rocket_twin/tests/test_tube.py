import numpy as np
from rocket_twin.systems import Tube

class TestTube:
    """Tests for the tube model."""

    def test_geometry(self):
        sys = Tube('sys')

        sys.radius = 5.
        sys.length = 9.
        sys.rho = 10.
        sys.pos = 0.

        sys.run_once()

        np.testing.assert_allclose(sys.props.Mass(), 2250*np.pi, atol=10**(-2))

        np.testing.assert_allclose(sys.props.CentreOfMass().X(), 0., atol=10**(-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Y(), 0., atol=10**(-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Z(), 4.5, atol=10**(-2))

        np.testing.assert_allclose(sys.props.MatrixOfInertia().Diagonal().X(), 13*2250*np.pi, atol=10**(-2))
        np.testing.assert_allclose(sys.props.MatrixOfInertia().Diagonal().Y(), 13*2250*np.pi, atol=10**(-2))
        np.testing.assert_allclose(sys.props.MatrixOfInertia().Diagonal().Z(), 12.5*2250*np.pi, atol=10**(-2))