from cosapp.drivers import NonLinearSolver, RungeKutta, RunSingleCase
from cosapp.recorders import DataFrameRecorder

def run_sequences(sys, sequences):
    rk = sys.add_driver(RungeKutta('rk'))
    rk.add_recorder(DataFrameRecorder(hold = True))

    for seq in sequences:
        print('sequence ', seq['name'])

        if seq['type'] == 'transient':
            sys.drivers.clear()
            rk.children.clear()

            sys.add_driver(rk)
            run = rk.add_driver(NonLinearSolver('nls', tol=1e-6))
            rk.time_interval=(rk.time, rk.time + 10000)

            if 'dt' in seq:
                rk.dt = seq['dt']

            if 'stop' in seq:
                rk.set_scenario(stop = seq['stop'])

        if seq['type'] == 'static':
            sys.drivers.clear()
            run = sys.add_driver(NonLinearSolver('nls', tol=1e-6))
            
        if 'init' in seq:
            for key, val in seq['init'].items():
                sys[key] = val
        if 'Tf' in seq:
            rk.time_interval = (rk.time, rk.time + seq['Tf'])
        if 'unknown' in seq:
            for uk in seq['unknown']:
                run.add_unknown(uk, max_rel_step=0.9)
        if 'equation' in seq:
            for eq in seq['equation']:
                run.add_equation(eq)
        if 'target' in seq:
            for var, tar in seq['target'].items():
                sys[var] = tar
        if 'design_method' in seq:
            for dm in seq['design_method']:
                run.runner.design.extend(sys.design_methods[dm])

        sys.run_drivers()

def run_endpoint(sys, sequence):

    solver = sys.add_driver(NonLinearSolver('solver', factor=0.9, tol=1e-5))
    target = solver.add_child(RunSingleCase('target'))
    driver = target.add_child(RungeKutta('rk', order=4))

    if 'dt' in sequence:
        driver.dt = sequence['dt']
    if 'Tf' in sequence:
        driver.time_interval = (0, sequence['Tf'])
    if 'init' in sequence:
        for key, val in sequence['init'].items():
            sys[key] = val
    if 'unknown' in sequence:
        target.design.add_unknown()
