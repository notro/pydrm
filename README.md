pydrm
=====

pydrm is a pure python [drm](https://dri.freedesktop.org/docs/drm/gpu/drm-uapi.html) library which can present the framebuffer as a [PIL.Image](https://pillow.readthedocs.io/en/latest/reference/Image.html) object.

Obvious shortcomings:
- DrmImageFramebuffer only supports XR24
- Only enum property type implemented
- Only tested with tinydrm
- API is not stable
- No documentation
- Still missing a lot to be on par with [libdrm](https://cgit.freedesktop.org/mesa/drm)

The code was made public (too) early since it makes it easy to test some monochrome e-ink panels.

Example (needs Python Imaging Library):
```
>>> from pydrm import *
>>> drm = SimpleDrm(format='XR24')
>>> drm.draw.line([(0,0), (drm.framebuffer.width -1, drm.framebuffer.height -1)], fill='white')
>>> drm.flush()
>>> print(drm.inspect())
SimpleDrm(0)
  version = DrmVersion(repaper)
  connector = DrmConnector(25)
  mode = DrmMode(264x176)
  crtc = DrmCrtc(27)
  plane = DrmPlane(26)
  format = DrmFormat(XR24)
  framebuffer = DrmImageFramebuffer(32)
  image = <PIL.Image.Image image mode=RGBX size=264x176 at 0xB6AFEB48>
  draw = <PIL.ImageDraw.ImageDraw instance at 0xb680dc88>

>>>

```

Dump info about the first drm device (doesn't need PIL):
```
>>> from pydrm import *
>>> drm = Drm()
>>> print(drm.inspect())
DrmVersion(repaper)
  name = repaper
  major = 1
  minor = 0
  date = 20170405
  patchlevel = 0
  desc = Pervasive Displays RePaper e-ink panels
Capabilities:
  DRM_CAP_DUMB_PREFER_SHADOW = 0
  DRM_PRIME_CAP_EXPORT = 1
  DRM_CAP_TIMESTAMP_MONOTONIC = 1
  DRM_CAP_PRIME = 3
  DRM_CAP_ASYNC_PAGE_FLIP = 0
  DRM_CAP_CURSOR_HEIGHT = 64
  DRM_CAP_DUMB_BUFFER = 1
  DRM_CAP_DUMB_PREFERRED_DEPTH = 16
  DRM_PRIME_CAP_IMPORT = 1
  DRM_CAP_ADDFB2_MODIFIERS = 0
  DRM_CAP_PAGE_FLIP_TARGET = 0
  DRM_CAP_CURSOR_WIDTH = 64
  DRM_CAP_VBLANK_HIGH_CRTC = 1
DrmEncoder(28)
  possible_clones = 0
  type_name = none
  possible_crtcs = 1
  crtc_id = 0
  crtc = None
  type = 0
DrmConnector(25)
  status = 1
  modes = [DrmMode(264x176)]
  type_id = 1
  subpixel = 0
  mm_height = 38
  DPMS = 3
  encoder = None
  props = ['DPMS']
  encoders = [DrmEncoder(28)]
  mm_width = 57
  type = 15
  name = Virtual-1
DrmCrtc(27)
  mode_valid = False
  mode = None
  props = []
  y = 0
  x = 0
  gamma_size = 0
DrmPlane(26)
  crtc = DrmCrtc(27)
  possible_crtcs = 1
  props = ['type']
  type = 1
  fb = None
  formats = [DrmFormat(RG16), DrmFormat(XR24)]
  gamma_size = 0
  preferred_format = DrmFormat(RG16)

>>>

```

Alternative projects:

- C++ library with python bindings: https://github.com/tomba/kmsxx
