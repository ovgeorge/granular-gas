import sphere
import numpy
### EXPERIMENT SETUP ###
rendering      = True
plots          = True

# Number of particles
np = 5e2

# Common simulation id
sim_id = "gas-test"

### INITIALIZATION ###

# New class
init = sphere.sim(np = np, nd = 3, nw = 0, sid = sim_id + "-init")

# Save radii
init.generateRadii(mean = 0.02)

# Use default params
init.defaultParams(gamma_n = 100.0, mu_s = 0.6, mu_d = 0.6)

# Add gravity
# init.g[2] = -9.81

# Periodic x and y boundaries
init.periodicBoundariesXY()

# Initialize positions in random grid (also sets world size)
hcells = np**(1.0/3.0)
init.initRandomGridPos(gridnum = [hcells, hcells, 1e9])

# Set duration of simulation
init.initTemporal(total = 0.01)

# Run sphere
init.run(dry = True)
init.run()

if (plots == True):
    # Make a graph of energies
    init.visualize('energy')

init.writeVTKall()

if (rendering == True):
    # Render images with raytracer
    init.render(method = "angvel", max_val = 0.3, verbose = False)


# For each normal stress, consolidate and subsequently shear the material
wvel = 20.0
cons = sphere.sim(np = init.np, nw = 1, sid = sim_id + "main")
lastf = sphere.status(sim_id + "-init")
cons.readbin("../output/" + sim_id + "-init.output{:0=5}.bin".format(lastf), verbose=False)
cons.periodicBoundariesXY()
for _t in range(1000):
    # New class
    wvel = wvel * -1.0
    cons.w_vel = numpy.array([wvel])

    cons.initTemporal(total = 0.1)

    cons.run(dry = True) # show values, don't run
    cons.run() # run

    if (plots == True):
        # Make a graph of energies
        cons.visualize('energy')
        #cons.visualize('walls')

    cons.writeVTKall()

    if (rendering == True):
        # Render images with raytracer
        cons.render()
