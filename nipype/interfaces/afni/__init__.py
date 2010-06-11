"""The afni module provides classes for interfacing with the `AFNI
<http://www.fmrib.ox.ac.uk/afni/index.html>`_ command line tools.  This
was written to work with AFNI version 4.1.4.

Top-level namespace for afni.  Perhaps should just make afni a package!
"""

"""XXX: This is an temporary warning for the 0.3 release to let users know that the afni interface is under construction and unstable."""
import warnings
warnings.warn('AFNI interface unstable.  Use at own risk.')


from nipype.interfaces.afni.base import Info, AFNICommand, AFNITraitedSpec
from nipype.interfaces.afni.preprocess import (Threedrefit, Threedresample, ThreedTstat, ThreedAutomask, Threedvolreg, Threedmerge, ThreedZcutup)
