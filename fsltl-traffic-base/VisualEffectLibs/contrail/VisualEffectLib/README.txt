The Ribbon.spb file is used for generating FSLTL contrails. It generates a contrail according to the visibility value in the local METAR. 
This is a workaround because it is not possible to retrieve humidity values from the sim. The less the visibily value is, the longer the trails. 
This only works properly when using real-time weather. 
When using weather presets, the trails will be very short.
When you use preset weather a lot, and want longer trails, static contrail lifetime versions are available in this folder:

Copy the one you like to use to 'Ribbon.spb' so you keep the original ones as backup. Default is RibbonV.spb.

RibbonV.spb    - variable particle lifetime, up to 250 sec. depending on local METAR.
Ribbon150.spb - particle lifetime of 150 sec. - medium long trails.
Ribbon250.spb - particle lifetime of 250 sec. - long trails.

FSLTL