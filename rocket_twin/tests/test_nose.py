import numpy as np
from rocket_twin.systems import Nose

class TestNose:
    """Tests for the nose model."""

    def test_geometry(self):
        sys = Nose('sys')

        sys.radius = 5.
        sys.height = 9.
        sys.rho = 10.
        sys.pos = 0.

        sys.run_once()

        np.testing.assert_allclose(sys.props.Mass(), 750*np.pi, atol=10**(-2))

        np.testing.assert_allclose(sys.props.CentreOfMass().X(), 0., atol=10**(-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Y(), 0., atol=10**(-2))
        np.testing.assert_allclose(sys.props.CentreOfMass().Z(), 2.25, atol=10**(-2))

        np.testing.assert_allclose(sys.props.MatrixOfInertia().Diagonal().X(), 6.7875*750*np.pi, atol=10**(-2))
        np.testing.assert_allclose(sys.props.MatrixOfInertia().Diagonal().Y(), 6.7875*750*np.pi, atol=10**(-2))
        np.testing.assert_allclose(sys.props.MatrixOfInertia().Diagonal().Z(), 7.5 *750*np.pi, atol=10**(-2))