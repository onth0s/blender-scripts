# ------------------------   bpy.context.mode   ------------------------ #

from math import pi
import re
import os

OBJ = "OBJECT"

MHE = "EDIT_MESH"
MHS = "SCULPT"
MHT = "PAINT_TEXTURE"
MHW = "PAINT_WEIGHT"
MHV = "PAINT_VERTEX"

ARE = "EDIT_ARMATURE"
ARP = "POSE"

SFE = "EDIT_SURFACE"

CVE = "EDIT_CURVE"

GPE = "EDIT_GPENCIL"
GPS = "SCULPT_GPENCIL"
GPW = "WEIGHT_GPENCIL"
GPP = "PAINT_GPENCIL"

MBE = "EDIT_METABALL"

LCE = "EDIT_LATTICE"

PTC = "PARTICLE"

TXE = "EDIT_TEXT"


ALL = (
    OBJ,
    MHE,
    MHS,
    MHT,
    MHW,
    MHV,
    ARE,
    ARP,
    SFE,
    CVE,
    GPE,
    GPS,
    GPW,
    GPP,
    MBE,
    LCE,
    PTC,
    TXE,
)

# ------------------------   context.object.type   ------------------------ #

TMH = "MESH"
TCV = "CURVE"
TSF = "SURFACE"
TMB = "META"
TTX = "FONT"
TAR = "ARMATURE"
TLC = "LATTICE"
TET = "EMPTY"
TGP = "GPENCIL"
TCM = "CAMERA"
TLT = "LIGHT"
TLP = "LIGHT_PROBE"
TSK = "SPEAKER"


def is_mode(context, *modes):
    return context.mode in modes


def is_active_type(context, *types):
    active = context.active_object
    return active and active.type in types


def get_active_mesh(context):
    active = context.active_object
    if active and active.type == "MESH":
        return active.data
    return None


def resolve_incremented_path(currentblend):
    path = os.path.dirname(currentblend)
    filename = os.path.basename(currentblend)

    filenameRegex = re.compile(r"(.+)\.blend\d*$")
    mo = filenameRegex.match(filename)

    if mo:
        name = mo.group(1)
        numberendRegex = re.compile(r"(.*?)(\d+)$")
        mo = numberendRegex.match(name)

        if mo:
            basename = mo.group(1)
            numberstr = mo.group(2)
        else:
            basename = name + "_"
            numberstr = "000"

        number = int(numberstr)
        incr = number + 1
        incrstr = str(incr).zfill(len(numberstr))
        incrname = basename + incrstr + ".blend"

        return os.path.join(path, incrname)
    return currentblend


def add_to_recent_files(path):
    try:
        import bpy  # type: ignore

        recent_path = bpy.utils.user_resource("CONFIG", "recent-files.txt")
        with open(recent_path, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            f.write(path.rstrip("\r\n") + "\n" + content)
    except (IOError, OSError, FileNotFoundError, ImportError):
        pass


def to_degrees(radians):
    return radians * (180 / pi)


def to_360_degrees(radians):
    return radians * (180 / pi)


def register():
    pass


def unregister():
    pass
