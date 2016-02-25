import openmoc
import openmoc.materialize as mat

###############################################################################
#                          Main Simulation Parameters
###############################################################################

options = openmoc.options.Options()

num_threads = options.getNumThreads()
track_spacing = options.getTrackSpacing()
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()
max_iters = options.getMaxIterations()

openmoc.log.set_log_level('NORMAL')

###############################################################################
#                            Creating Materials
###############################################################################

openmoc.log.py_printf('NORMAL', 'Importing materials data from HDF5...')
materials = openmoc.materialize.load_from_hdf5('materials-data.h5', '')

moderator = materials['water']
fuel = materials['fuel']


###############################################################################
#                            Creating Surfaces
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating surfaces...')

left = openmoc.XPlane(x=-2.0, name='left')
right = openmoc.XPlane(x=2.0, name='right')
top = openmoc.YPlane(y=2.0, name='top')
bottom = openmoc.YPlane(y=-2.0, name='bottom')

cell_left = openmoc.XPlane(x=-1.0/9.0, name='cell left')
cell_right = openmoc.XPlane(x=1.0/9.0, name='cell right')
cell_top = openmoc.YPlane(y=1.0/9.0, name='cell top')
cell_bottom = openmoc.YPlane(y=-1.0/9.0, name='cell bottom')
cell_left.setBoundaryType(openmoc.VACUUM)
cell_right.setBoundaryType(openmoc.VACUUM)
cell_top.setBoundaryType(openmoc.VACUUM)
cell_bottom.setBoundaryType(openmoc.VACUUM)

left.setBoundaryType(openmoc.VACUUM)
right.setBoundaryType(openmoc.VACUUM)
top.setBoundaryType(openmoc.VACUUM)
bottom.setBoundaryType(openmoc.VACUUM)


###############################################################################
#                             Creating Cells
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating cells...')

root_cell = openmoc.Cell(name='root cell')
root_cell.addSurface(halfspace=+1, surface=left)
root_cell.addSurface(halfspace=-1, surface=right)
root_cell.addSurface(halfspace=+1, surface=bottom)
root_cell.addSurface(halfspace=-1, surface=top)

fuel_cell = openmoc.Cell(name='fuel cell')
fuel_cell.setFill(fuel)
fuel_cell.addSurface(halfspace=+1, surface=cell_left)
fuel_cell.addSurface(halfspace=-1, surface=cell_right)
fuel_cell.addSurface(halfspace=+1, surface=cell_bottom)
fuel_cell.addSurface(halfspace=-1, surface=cell_top)

moderator_cell = openmoc.Cell(name='moderator cell')
moderator_cell.setFill(moderator)
moderator_cell.addSurface(halfspace=+1, surface=cell_left)
moderator_cell.addSurface(halfspace=-1, surface=cell_right)
moderator_cell.addSurface(halfspace=+1, surface=cell_bottom)
moderator_cell.addSurface(halfspace=-1, surface=cell_top)

###############################################################################
#                            Creating Universes
###############################################################################

openmoc.log.py_printf('NORMAL', 'Creating universes...')

root_universe = openmoc.Universe(name='root universe')
root_universe.addCell(root_cell)

fuel_univ = openmoc.Universe(name='fuel universe')
mod_univ = openmoc.Universe(name='moderator universe')
fuel_univ.addCell(fuel_cell)
mod_univ.addCell(moderator_cell)


###############################################################################
#                         Creating the Geometry
###############################################################################


openmoc.log.py_printf('NORMAL', 'Creating geometry...')

geometry = openmoc.Geometry()
geometry.setRootUniverse(root_universe)


###############################################################################
#                          Creating the TrackGenerator
###############################################################################

openmoc.log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = openmoc.TrackGenerator(geometry, num_azim, track_spacing)
track_generator.setNumThreads(num_threads)
track_generator.generateTracks()


###############################################################################
#                            Running a Simulation
###############################################################################

solver = openmoc.CPUSolver(track_generator)
solver.setNumThreads(num_threads)
solver.setConvergenceThreshold(tolerance)
solver.computeEigenvalue(max_iters)
solver.printTimerReport()


###############################################################################
#                             Generating Plots
###############################################################################

openmoc.log.py_printf('NORMAL', 'Plotting data...')

openmoc.plotter.plot_quadrature(solver)
openmoc.plotter.plot_tracks(track_generator)
openmoc.plotter.plot_segments(track_generator)
openmoc.plotter.plot_materials(geometry)
openmoc.plotter.plot_cells(geometry)
openmoc.plotter.plot_flat_source_regions(geometry)
openmoc.plotter.plot_spatial_fluxes(solver, energy_groups=[1,2])
openmoc.plotter.plot_energy_fluxes(solver, fsrs=range(geometry.getNumFSRs()))

openmoc.log.py_printf('TITLE', 'Finished')

###############################################################################
#                             Creating Lattice
###############################################################################

lattice = openmoc.Lattice(name='9x9 lattice')
lattice.setWidth(width_x=2.0/9.0, width_y=2.0/9.0)

# assign each lattice cell a universe ID
lattice.setUniverses([
        [mod_univ, mod_univ, mod_univ, mod_univ, mod_univ,
                mod_univ, mod_univ, mod_univ, mod_univ],
        [mod_univ, mod_univ, mod_univ, mod_univ, mod_univ,
                mod_univ, mod_univ, mod_univ, mod_univ],
        [mod_univ, mod_univ, mod_univ, mod_univ, mod_univ,
                mod_univ, mod_univ, mod_univ, mod_univ],
        [mod_univ, mod_univ, mod_univ, fuel_univ, fuel_univ,
                fuel_univ, mod_univ, mod_univ, mod_univ],
        [mod_univ, mod_univ, mod_univ, fuel_univ, fuel_univ,
                fuel_univ, mod_univ, mod_univ, mod_univ],
        [mod_univ, mod_univ, mod_univ, fuel_univ, fuel_univ,
                fuel_univ, mod_univ, mod_univ, mod_univ],
        [mod_univ, mod_univ, mod_univ, mod_univ, mod_univ,
                mod_univ, mod_univ, mod_univ, mod_univ],
        [mod_univ, mod_univ, mod_univ, mod_univ, mod_univ,
                mod_univ, mod_univ, mod_univ, mod_univ],
        [mod_univ, mod_univ, mod_univ, mod_univ, mod_univ,
                mod_univ, mod_univ, mod_univ, mod_univ]
        ])

root_cell.setFill(lattice)
