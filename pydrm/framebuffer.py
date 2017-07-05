import ctypes
import fcntl

from .base import DrmObject
from .drm_h import DRM_IOCTL_MODE_GETFB, DRM_IOCTL_MODE_ADDFB2, DRM_IOCTL_MODE_RMFB, DRM_IOCTL_MODE_DIRTYFB, DrmClipRectC
from .drm_mode_h import DrmModeFbCmdC, DRM_MODE_OBJECT_FB, DrmModeFbCmd2C, DrmModeFbDirtyCmdC
from .buffer import DrmDumbBuffer


class DrmFramebuffer(DrmObject):
    def __init__(self, bo=None):
        if bo:
            self._drm = bo._drm
            self.format = bo.format
            self.width = bo.width
            self.height = bo.height
            self.bo = bo
            self._create()
        else:
            self._drm = None
            self.id = None
            self.format = None
            self.width = None
            self.height = None
            self.bo = None

    def fetch(self):
        arg = DrmModeFbCmdC()
        arg.fb_id = self.id

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETFB, arg)

        self._arg = arg
        self.width = int(arg.width)
        self.height = int(arg.height)
        self.pitch = int(arg.pitch)
        self.bpp = int(arg.bpp)
        self.depth = int(arg.depth)
        self.handle = int(arg.handle)

        self.get_props(DRM_MODE_OBJECT_FB)

    def _create(self):
        arg = DrmModeFbCmd2C()
        arg.width = self.width
        arg.height = self.height
        arg.pixel_format = self.format.fourcc
        arg.handles = (ctypes.c_uint32 * 4)(*self.bo.handles)
        arg.pitches = (ctypes.c_uint32 * 4)(*self.bo.pitches)
        arg.offsets = (ctypes.c_uint32 * 4)(*self.bo.offsets)
        #arg.modifier

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_ADDFB2, arg)

        self.id = int(arg.fb_id)
        self.fetch()
        self._drm._framebuffers.append(self)

    def remove(self):
        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_RMFB, ctypes.c_uint(self.id))
        self._drm._framebuffers.remove(self)

    def flush(self, x1=None, y1=None, x2=None, y2=None):
        if x1 is not None and y1 is None:
            raise TypeError("flush expected zero or 4 arguments")

        arg = DrmModeFbDirtyCmdC()
        arg.fb_id = self.id

        if x1 is not None:
            clip = DrmClipRectC(x1=x1, y1=y1, x2=x2, y2=y2)
            arg.clips_ptr = ctypes.cast(ctypes.pointer(clip), ctypes.c_void_p).value
            arg.num_clips = 1

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_DIRTYFB, arg)

    @classmethod
    def from_id(cls, drm, id):
        self = cls()
        self._drm = drm
        self.id = int(id)
        self.fetch()
        return self


class DrmDumbFramebuffer(DrmFramebuffer):
    def __init__(self, drm, format_, width, height):
        bo = DrmDumbBuffer(drm, format_, width, height)
        super(DrmDumbFramebuffer, self).__init__(bo)
