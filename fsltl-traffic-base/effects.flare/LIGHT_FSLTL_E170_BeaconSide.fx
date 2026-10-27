[Library Effect]
Lifetime=5
Version=2.0
Radius=-1
Priority=0

[Properties]

[Emitter.0]
Lifetime=0.0, 0.0
Delay=0.0, 0.0
Bounce=0.0
Light=1
No Interpolate=1
Rate=0.67, 0.67
X Emitter Velocity=0.0, 0.0
Y Emitter Velocity=0.0, 0.0
Z Emitter Velocity=0.0, 0.0
Drag=0.0, 0.0
X Particle Velocity=0.0, 0.0
Y Particle Velocity=0.0, 0.0
Z Particle Velocity=0.0, 0.0
X Rotation=0.0, 0.0
Y Rotation=0.0, 0.0
Z Rotation=0.0, 0.0
X Offset=0.0, 0.0
Y Offset=0.0, 0.0
Z Offset=0.0, 0.0

[Particle.0]
Lifetime=0.1, 0.1
Type=19
X Scale=0.2, 0.2
Y Scale=0.2, 0.2
Z Scale=0.0, 0.0
X Scale Rate=0.0, 0.0
Y Scale Rate=0.0, 0.0
Z Scale Rate=0.0, 0.0
Drag=0.0, 0.0
Color Rate=0.0, 0.0
X Offset=0.0, 0.0
Y Offset=0.0, 0.0
Z Offset=0.0, 0.0
Fade In=0.0, 0.0
Fade Out=0.0, 0.0
Rotation=0.0, 0.0
Static=1
Face=1, 1, 1

[ParticleAttributes.0]
Blend Mode=2
Texture=FSLTL-LIGHTnav
Bounce=0.1
Color Start=255, 0, 0, 255
Color End=255, 0, 0, 255
Jitter Distance=0.0
Jitter Time=0.0
uv1=0.0, 0.0
uv2=1.0, 1.0
NearEndFade= 1
NearFade= 1
MinProjSize=0.2

[LightAttributes.0]
Type=spot
Size=0.2
Range=20
Intensity=25
Softness=0.5
SpotInner=0.0
SpotOuter=15.0
Falloff=1.0
Volumetric=1
ScatDir=0.0

; --- Emitter 1: Hot spot flash ---
[Emitter.1]
Lifetime=0.0,0.0
Delay=0.0,0.0
Light=0
Rate=0.67,0.67
No Interpolate=1

[Particle.1]
Lifetime=0.1,0.1
Type=19
X Scale=0.15,0.15
Y Scale=0.15,0.15
Static=1
Face=1,1,1

[ParticleAttributes.1]
Blend Mode=2
Texture=FSLTL-LIGHTnav
Color Start=255,0,0,255
Color End=255,0,0,255
MinProjSize=0.2

; --- Emitter 2: Bloom halo ---
[Emitter.2]
Lifetime=0.0,0.0
Delay=0.0,0.0
Light=0
Rate=0.67,0.67
No Interpolate=1

[Particle.2]
Lifetime=0.2,0.2
Type=19
X Scale=2.5,2.5
Y Scale=2.5,2.5
Static=1
Face=1,1,1

[ParticleAttributes.2]
Blend Mode=2
Texture=FSLTL-ALLO-2
Color Start=15,0,0,100
Color End=15,0,0,100
MinProjSize=

