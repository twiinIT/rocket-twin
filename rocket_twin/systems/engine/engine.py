from cosapp.base import System

from rocket_twin.systems.engine import EngineGeom, EnginePerfo


class Engine(System):
    """Simple model of an engine.

    Inputs
    ------
    w_out [kg/s]: float,
        fuel consumption rate

    Outputs
    ------
    force [N]: float,
        thrust force
    shape: TopoDS_Solid,
        pyoccad model
    props: GProp_GProps,
        model properties
    """

    def setup(self):

        self.add_child(EngineGeom("geom"), pulling=["shape", "props"])
        self.add_child(EnginePerfo("perfo"), pulling=["w_out", "force"])
