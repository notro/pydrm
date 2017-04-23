import ctypes
import fcntl
import mmap

from .base import DrmObject
from .drm_h import DRM_IOCTL_MODE_CREATE_DUMB, DRM_IOCTL_MODE_MAP_DUMB, DRM_IOCTL_MODE_DESTROY_DUMB
from .drm_mode_h import DrmModeCreateDumbC, DrmModeMapDumbC, DrmModeDestroyDumbC



#                ("height", c_uint32),
#                ("width", c_uint32),
#                ("bpp", c_uint32),
#                ("flags", c_uint32),
#
#                ("handle", c_uint32),
#                ("pitch", c_uint32),
#                ("size", c_uint32),


class DrmBuffer(DrmObject):
    def __init__(self, drm, format_, width, height):
        self._drm = drm
        self.format = format_
        self.width = width
        self.height = height
        self.handles=[ 0, 0, 0 ]
        self.pitches=[ 0, 0, 0 ]
        self.offsets=[ 0, 0, 0 ]
        self.planes= [ 0, 0, 0 ]
        self.map = None


class DrmDumbBuffer(DrmBuffer):
    def __init__(self, drm, format_, width, height):
        super(DrmDumbBuffer, self).__init__(drm, format_, width, height)

        arg = DrmModeCreateDumbC()
        arg.bpp = self.format.cpp[0] * 8;
        arg.width = self.width;
        arg.height = self.height;

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_CREATE_DUMB, arg)

        #self.handle = arg.handle
        self.id = int(arg.handle)
        self.len = int(arg.size)
        self.pitch = int(arg.pitch)
        self._arg = arg

        self.handles[0] = self.id
        self.pitches[0] = self.pitch
        self.offsets[0] = 0

        if self.format.planes > 1:
            raise NotImplementedError("support for format %s is not implemented yet\n" % self.format.name)

    def destroy(self):
        arg = DrmModeDestroyDumbC()
        arg.handle = self.id
        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_DESTROY_DUMB, arg)

#                ("handle", c_uint32),
#                ("pad", c_uint32),
#                ("offset", c_uint64),

    def mmap(self):
        arg = DrmModeMapDumbC()
        arg.handle = self.id
        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_MAP_DUMB, arg)
        self.map = mmap.mmap(self._drm.fd.fileno(), self.len, offset=arg.offset)
        return self.map

    def munmap(self):
        self.map.close()
        self.map = None


