import sys
import json
import numpy
import scipy.integrate

# Read the name of the input file from the command line, and read options from
# the file:
assert len(sys.argv) == 2, 'Please provide an input file.'
with open(sys.argv[1], 'r') as f:
    settings = json.loads(f.read())

# Then retrieve the various parameters from what we just read:
D = settings['spring constant']
L = settings['spring rest length']
m = settings['masses']
[x1_0, x2_0] = settings['initial position']
[v1_0, v2_0] = settings['initial velocity']

# describe the differential equation as a first order ODE:
y0 = [x1_0[0], x1_0[1], x1_0[2], x2_0[0], x2_0[1], x2_0[2],
      v1_0[0], v1_0[1], v1_0[2], v2_0[0], v2_0[1], v2_0[2]]

def f(t, y):
    p1 = y[0:3]
    p2 = y[3:6]
    v1 = y[6:9]
    v2 = y[9:12]

    g = [0., 0., -9.81]

    dist = numpy.linalg.norm(p2-p1)
    a1 = g - D*(dist-L) * (p1-p2)/dist/m[0]
    a2 = g - D*(dist-L) * (p2-p1)/dist/m[1]
    return numpy.concatenate([v1, v2, a1, a2])


# Next create an object that can integrate the ODE numerically:
start_time = 0.
end_time   = 5
integrator = scipy.integrate.ode(f)
integrator.set_integrator('vode', rtol=1e-6)
integrator.set_initial_value(y0, start_time)

# With this, do the integration step by step, appending values to an array in
# each step:
t_values = [start_time]
y_values = numpy.array([y0])
while integrator.successful() and integrator.t < end_time:
    integrator.integrate(end_time, step=True)
    t_values.append(integrator.t)
    y_values = numpy.vstack((y_values, integrator.y))

# Having done so, output the number of time steps and the final positions:
print "time steps:", len(t_values)
print "final position:", y_values[-1,0:3], y_values[-1,3:6]
