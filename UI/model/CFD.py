import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

# import_filename = examples.download_file("mixing_elbow.pmdb", "pyfluent/mixing_elbow")
import_filename = "Example"

meshing = pyfluent.launch_fluent(precision="double", processor_count=4, mode="meshing")

meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

meshing.workflow.TaskObject["Import Geometry"].Arguments = {
    "FileName": import_filename,
    "LengthUnit": "mm",
}

# Import geometry
# ~~~~~~~~~~~~~~~
# Import the geometry.

meshing.workflow.TaskObject["Import Geometry"].Execute()

meshing.workflow.TaskObject["Add Local Sizing"].Arguments.set_state(
    {
        r"AddChild": r"yes",
        r"BOIFaceLabelList": [r"wall"],
    }
)
meshing.workflow.TaskObject["Add Local Sizing"].AddChildAndUpdate()
meshing.workflow.TaskObject["Generate the Surface Mesh"].Execute()
meshing.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(
    SetupTypeChanged=False
)
meshing.workflow.TaskObject["Describe Geometry"].Arguments.set_state(
    {
        r"SetupType": r"The geometry consists of both fluid and solid regions and/or voids",
    }
)
meshing.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=True)
meshing.workflow.TaskObject["Describe Geometry"].Arguments.set_state(
    {
        r"CappingRequired": r"No",
        r"InvokeShareTopology": r"Yes",
        r"SetupType": r"The geometry consists of both fluid and solid regions and/or voids",
    }
)
meshing.workflow.TaskObject["Describe Geometry"].Execute()
meshing.workflow.TaskObject["Apply Share Topology"].Execute()
meshing.workflow.TaskObject["Update Boundaries"].Execute()
meshing.workflow.TaskObject["Create Regions"].Execute()
meshing.workflow.TaskObject["Update Regions"].Execute()
meshing.workflow.TaskObject["Add Boundary Layers"].Arguments.set_state(
    {
        r"LocalPrismPreferences": {
            r"Continuous": r"Stair Step",
        },
    }
)
meshing.workflow.TaskObject["Add Boundary Layers"].AddChildAndUpdate()
meshing.workflow.TaskObject["Generate the Volume Mesh"].Arguments.set_state(
    {
        r"VolumeFill": r"poly-hexcore",
    }
)
meshing.workflow.TaskObject["Generate the Volume Mesh"].Execute()
