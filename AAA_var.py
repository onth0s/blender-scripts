# ------------------------   bpy.context.mode   ------------------------ #

OBJ = 'OBJECT'

MHE = 'EDIT_MESH' 
MHS = 'SCULPT' 
MHT = 'PAINT_TEXTURE' 
MHW = 'PAINT_WEIGHT' 
MHV = 'PAINT_VERTEX' 

ARE = 'EDIT_ARMATURE' 
ARP = 'POSE' 

SFE = 'EDIT_SURFACE' 

CVE = 'EDIT_CURVE' 

GPE = 'EDIT_GPENCIL' 
GPS = 'SCULPT_GPENCIL' 
GPW = 'WEIGHT_GPENCIL' 
GPP = 'PAINT_GPENCIL' 

MBE = 'EDIT_METABALL' 

LCE = 'EDIT_LATTICE'

PTC = 'PARTICLE'

TXE = 'EDIT_TEXT'


ALL = (OBJ,
    MHE, MHS, MHT, MHW, MHV,
    ARE, ARP,
    SFE,
    CVE,
    GPE, GPS, GPW, GPP,
    MBE,
    LCE,
    PTC,
    TXE)

# ------------------------   context.object.type   ------------------------ #

TMH = 'MESH'
TCV = 'CURVE'
TSF = 'SURFACE'
TMB = 'META'
TTX = 'FONT'
TAR = 'ARMATURE'
TLC = 'LATTICE'
TET = 'EMPTY'
TGP = 'GPENCIL'
TCM = 'CAMERA'
TLT = 'LIGHT'
TLP = 'LIGHT_PROBE'
TSK = 'SPEAKER'

def register():
    pass
def unregister():
    pass