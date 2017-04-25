import ctypes
import fcntl

from .base import DrmObject, DrmMode
from .drm_h import DRM_IOCTL_MODE_GETCRTC, DRM_IOCTL_MODE_SETCRTC
from .drm_mode_h import DrmModeCrtcC, DRM_MODE_OBJECT_CRTC


#                ("set_connectors_ptr", c_uint64),
#                ("count_connectors", c_uint32),
#                ("crtc_id", c_uint32),
#                ("fb_id", c_uint32),
#                ("x", c_uint32),
#                ("y", c_uint32),
#                ("gamma_size", c_uint32),
#                ("mode_valid", c_uint32),
#                ("mode", DrmModeModeinfoC)


class DrmCrtc(DrmObject):
    def __init__(self, drm, id):
        self._drm = drm
        self.id = int(id)
        self.fetch()
        self.get_props(DRM_MODE_OBJECT_CRTC)

    def fetch(self):
        arg = DrmModeCrtcC()
        arg.crtc_id = self.id

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETCRTC, arg)

        self._arg = arg
        if arg.fb_id:
            self.fb = self._drm.get_framebuffer(arg.fb_id)
        else:
            self.fb = None
        self.x = int(arg.x)
        self.y = int(arg.y)
        self.gamma_size = int(arg.gamma_size)
        self.mode_valid = bool(arg.mode_valid)
        if self.mode_valid:
            self.mode = DrmMode(arg.mode)
            self.width = self.mode.hdisplay
            self.height = self.mode.vdisplay
        else:
            self.mode = None
            self.width = 0
            self.height = 0

    def set(self, fb, x, y, mode, *conns):
        arg = DrmModeCrtcC()
        arg.crtc_id = self.id
        arg.fb_id = fb.id
        arg.x = x
        arg.y = y
        arg.mode_valid = 1
        arg.mode = mode._arg

        connector_ids = (ctypes.c_uint32 * len(conns))(*[conn.id for conn in conns])
        arg.set_connectors_ptr = ctypes.cast(ctypes.pointer(connector_ids), ctypes.c_void_p).value
        arg.count_connectors = len(conns)

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_SETCRTC, arg)

        self.fetch()
