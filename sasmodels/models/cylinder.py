# cylinder model
# Note: model title and parameter table are inserted automatically
r"""
The form factor is normalized by the particle volume.

For information about polarised and magnetic scattering, click here_.

Definition
----------

The output of the 2D scattering intensity function for oriented cylinders is
given by (Guinier, 1955)

.. math::

    P(Q,\alpha) = {\text{scale} \over V} F^2(Q) + \text{background}

where

.. math::

    F(Q) = 2 (\Delta \rho) V
           {\sin \left(Q\tfrac12 L\cos\alpha \right)
               \over Q\tfrac12 L \cos \alpha}
           {J_1 \left(Q R \sin \alpha\right) \over Q R \sin \alpha}

and $\alpha$ is the angle between the axis of the cylinder and $\vec q$, $V$
is the volume of the cylinder, $L$ is the length of the cylinder, $R$ is the
radius of the cylinder, and $\Delta\rho$ (contrast) is the scattering length
density difference between the scatterer and the solvent. $J_1$ is the
first order Bessel function.

To provide easy access to the orientation of the cylinder, we define the
axis of the cylinder using two angles $\theta$ and $\phi$. Those angles
are defined in :num:`figure #cylinder-orientation`.

.. _cylinder-orientation:

.. figure:: img/orientation.jpg

    Definition of the angles for oriented cylinders.

.. figure:: img/orientation2.jpg

    Examples of the angles for oriented cylinders against the detector plane.

NB: The 2nd virial coefficient of the cylinder is calculated based on the
radius and length values, and used as the effective radius for $S(Q)$
when $P(Q) \cdot S(Q)$ is applied.

The output of the 1D scattering intensity function for randomly oriented
cylinders is then given by

.. math::

    P(Q) = {\text{scale} \over V}
        \int_0^{\pi/2} F^2(Q,\alpha) \sin \alpha\ d\alpha + \text{background}

The *theta* and *phi* parameters are not used for the 1D output. Our
implementation of the scattering kernel and the 1D scattering intensity
use the c-library from NIST.

Validation
----------

Validation of our code was done by comparing the output of the 1D model
to the output of the software provided by the NIST (Kline, 2006).
:num:`Figure #cylinder-compare` shows a comparison of
the 1D output of our model and the output of the NIST software.

.. _cylinder-compare:

.. figure:: img/cylinder_compare.jpg

    Comparison of the SasView scattering intensity for a cylinder with the
    output of the NIST SANS analysis software.
    The parameters were set to: *scale* = 1.0, *radius* = 20 |Ang|,
    *length* = 400 |Ang|, *contrast* = 3e-6 |Ang^-2|, and
    *background* = 0.01 |cm^-1|.

In general, averaging over a distribution of orientations is done by
evaluating the following

.. math::

    P(Q) = \int_0^{\pi/2} d\phi
        \int_0^\pi p(\theta, \phi) P_0(Q,\alpha) \sin \theta\ d\theta


where $p(\theta,\phi)$ is the probability distribution for the orientation
and $P_0(Q,\alpha)$ is the scattering intensity for the fully oriented
system. Since we have no other software to compare the implementation of
the intensity for fully oriented cylinders, we can compare the result of
averaging our 2D output using a uniform distribution $p(\theta, \phi) = 1.0$.
:num:`Figure #cylinder-crosscheck` shows the result of
such a cross-check.

.. _cylinder-crosscheck:

.. figure:: img/cylinder_crosscheck.jpg

    Comparison of the intensity for uniformly distributed cylinders
    calculated from our 2D model and the intensity from the NIST SANS
    analysis software.
    The parameters used were: *scale* = 1.0, *radius* = 20 |Ang|,
    *length* = 400 |Ang|, *contrast* = 3e-6 |Ang^-2|, and
    *background* = 0.0 |cm^-1|.
"""

import numpy as np
from numpy import pi, inf

name = "cylinder"
title = "Right circular cylinder with uniform scattering length density."
description = """
     f(q,alpha) = 2*(sld - solvent_sld)*V*sin(qLcos(alpha/2))
                /[qLcos(alpha/2)]*J1(qRsin(alpha/2))/[qRsin(alpha)]

            P(q,alpha)= scale/V*f(q,alpha)^(2)+background
            V: Volume of the cylinder
            R: Radius of the cylinder
            L: Length of the cylinder
            J1: The bessel function
            alpha: angle between the axis of the
            cylinder and the q-vector for 1D
            :the ouput is P(q)=scale/V*integral
            from pi/2 to zero of...
            f(q,alpha)^(2)*sin(alpha)*dalpha + background
"""
category = "shape:cylinder"

parameters = [
#   [ "name", "units", default, [lower, upper], "type",
#     "description" ],
    [ "sld", "1e-6/Ang^2", 4, [-inf,inf], "",
      "Cylinder scattering length density" ],
    [ "solvent_sld", "1e-6/Ang^2", 1, [-inf,inf], "",
      "Solvent scattering length density" ],
    [ "radius", "Ang",  20, [0, inf], "volume",
      "Cylinder radius" ],
    [ "length", "Ang",  400, [0, inf], "volume",
      "Cylinder length" ],
    [ "theta", "degrees", 60, [-inf, inf], "orientation",
      "In plane angle" ],
    [ "phi", "degrees", 60, [-inf, inf], "orientation",
      "Out of plane angle" ],
    ]

source = [ "lib/J1.c", "lib/gauss76.c", "cylinder.c" ]

def ER(radius, length):
    ddd = 0.75*radius*(2*radius*length + (length+radius)*(length+pi*radius))
    return 0.5 * (ddd)**(1./3.)

# parameters for demo
demo = dict(
    scale=1, background=0,
    sld=6, solvent_sld=1,
    #radius=5, length=20,
    radius=20, length=300,
    theta=60, phi=60,
    radius_pd=.2, radius_pd_n=9,
    length_pd=.2,length_pd_n=10,
    theta_pd=10, theta_pd_n=5,
    phi_pd=10, phi_pd_n=5,
    )

# For testing against the old sasview models, include the converted parameter
# names and the target sasview model name.
oldname='CylinderModel'
oldpars=dict(theta='cyl_theta', phi='cyl_phi', sld='sldCyl', solvent_sld='sldSolv')


qx,qy = 0.2*np.cos(2.5), 0.2*np.sin(2.5)
tests = [
    [{},  0.2, 0.041761386790780453],
    [{}, [0.2], [0.041761386790780453]],
    [{'theta':10.0, 'phi':10.0}, (qx, qy), 0.03414647218513852],
    [{'theta':10.0, 'phi':10.0}, [(qx, qy)], [0.03414647218513852]],
    ]
del qx,qy  # not necessary to delete, but cleaner
