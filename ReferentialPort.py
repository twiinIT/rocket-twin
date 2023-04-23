from cosapp.base import Port, BaseConnector
import numpy as np


class ReferentialPort(Port):
    """Referential Port """
    def setup(self):
        self.add_variable('vector', np.zeros(2, dtype=float))

    class Connector(BaseConnector):
        """Custom connector for `ReferentialPort` objects
        """
        def __init__(self, name: str, sink: Port, source: Port, *args, **kwargs):
            super().__init__(name, sink, source)

        def transfer(self) -> None:
            sink = self.sink 
            source = self.source 

            # Going from earth referential to rocket referential 
            if source.owner.referential == 'Earth' and sink.owner.referential == 'Rocket': 
                theta = source.owner.theta
                sink.vector = np.array([source.vector[1]*np.cos(theta) - source.vector[0]*np.sin(theta),
                                        - source.vector[0]*np.cos(theta) - source.vector[1]*np.sin(theta)])
                return
                                        
            # Going from rocket referential to earth referential
            if sink.owner.referential == 'Earth' and source.owner.referential == 'Rocket': 
                # If there is no theta in sink.owner (i.e. we are in Dynamics), then we take the theta from the parent Earth
                try:
                    theta = sink.owner.theta
                except AttributeError:
                    theta = sink.owner.parent.theta
                sink.vector = np.array([ - source.vector[1]*np.cos(theta) - source.vector[0]*np.sin(theta),
                                        source.vector[0]*np.cos(theta) - source.vector[1]*np.sin(theta)])
                return
            sink.vector = source.vector

