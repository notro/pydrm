import os, sys, mmap
from time import sleep
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))) # use pydrm from parent dir
from pydrm import Drm
from pydrm.buffer import DrmDumbBuffer, DrmBuffer
from pydrm.image import DrmImageFramebuffer
from pydrm.property import DrmPropertyEnum
from pydrm.format import DrmFormat
from utils import *

# for Python 2
try:
   input = raw_input
except NameError:
   pass


parser = argparse.ArgumentParser(description='Test PRIME')
parser.add_argument('scanout', help='minor to scanout buffer on', type=int)
parser.add_argument('source', nargs='?', help='optional source minor', type=int)
parser.add_argument('--verbose', '-v', action='count')
args = parser.parse_args()


if args.verbose:
    print("Scanout on:")

minor = args.scanout

drm = Drm(minor)

if args.verbose == 1:
    print(drm.version.inspect())
elif args.verbose:
    print(drm.inspect(args.verbose > 2))

conns = drm.find_connectors()[:1]
connector = conns[0]

mode = connector.find_mode()
width = mode.hdisplay
height = mode.vdisplay
#print(mode.inspect(True))

crtcs = drm.find_crtcs(connector)
crtc = crtcs[0]

planes = drm.find_planes(crtc)
plane = planes[0]

#format_ = plane.preferred_format
format_ = DrmFormat('XR24')

if args.source is None:
    print("Using dumb buffer from scanout:")
    bo = DrmDumbBuffer(drm, format_, width, height)
else:
    print("Using dumb buffer from source:")
    source = Drm(args.source)

    if args.verbose == 1:
        print(source.version.inspect())
    elif args.verbose:
        print(source.inspect(args.verbose > 2))

    bo = DrmDumbBuffer(source, format_, width, height)

if args.verbose:
    print(bo.inspect(args.verbose > 1))

sleep(1)

fd = bo.prime_export()
print("dmabuf fd = %d" % fd)

sleep(1)

#bo.sync_start()

#b = mmap.mmap(fd, bo.len, offset=bo.offsets[0])
b = mmap.mmap(fd, bo.len)

for i in range(160):
    b[i] = '\xff'

#bo.sync_end()

bo2 = DrmBuffer.prime_import(drm, fd, format_, width, height)

if args.verbose:
    print(bo2.inspect(args.verbose > 1))

fb = DrmImageFramebuffer(bo=bo2)

crtc.set(fb, 0, 0, mode, connector)

input("Press enter to draw pattern")


from PIL import ImageDraw
draw = ImageDraw.Draw(fb.image)

draw_smpte_pattern(draw)
fb.flush()
sleep(2)
draw_mono_pattern(draw)
fb.flush()

input("Press enter to stop")
