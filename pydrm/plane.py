import ctypes
import fcntl

from .base import DrmObject
from .drm_h import DRM_IOCTL_MODE_GETPLANERESOURCES, DRM_IOCTL_MODE_GETPLANE
from .drm_mode_h import DrmModeGetPlaneResC, DrmModeGetPlaneC, DRM_MODE_OBJECT_PLANE
from .format import DrmFormat


#                ("plane_id_ptr", c_uint64),
#                ("count_planes", c_uint32),


#                ("plane_id", c_uint32),
#
#                ("crtc_id", c_uint32),
#                ("fb_id", c_uint32),
#
#                ("possible_crtcs", c_uint32),
#                ("gamma_size", c_uint32),
#
#                ("count_format_types", c_uint32),
#                ("format_type_ptr", c_uint64),


class DrmPlane(DrmObject):
    def __init__(self, drm, id_):
        self._drm = drm
        self.id = int(id_)
        self.fetch()

    def fetch(self):
        arg = DrmModeGetPlaneC()
        arg.plane_id = self.id

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETPLANE, arg)

        formats = (ctypes.c_uint32*arg.count_format_types)()
        arg.format_type_ptr = ctypes.cast(ctypes.pointer(formats), ctypes.c_void_p).value

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETPLANE, arg)

        self._arg = arg

        if (arg.crtc_id):
            self.crtc = self._drm.get_crtc(arg.crtc_id)
        else:
            self.crtc = None

        if (arg.fb_id):
            self.fb = self._drm.get_framebuffer(arg.fb_id)
        else:
            self.fb = None

        self.possible_crtcs = arg.possible_crtcs
        self.gamma_size = int(arg.gamma_size)

        self.formats = []
        for i in range(arg.count_format_types):
            self.formats.append(DrmFormat(int(formats[i])))

        self.get_props(DRM_MODE_OBJECT_PLANE)

        self.preferred_format = None
        depth = self._drm.cap.DRM_CAP_DUMB_PREFERRED_DEPTH
        if depth == 32 and DrmFormat('AR24') in self.formats:
            self.preferred_format = DrmFormat('AR24')
        elif depth == 24 and DrmFormat('XR24') in self.formats:
            self.preferred_format = DrmFormat('XR24')
        elif depth == 16 and DrmFormat('RG16') in self.formats:
            self.preferred_format = DrmFormat('RG16')
        elif depth == 8 and DrmFormat('C8') in self.formats:
            self.preferred_format = DrmFormat('C8')
        elif depth:
            for format_ in self.formats:
                if format_.depth == depth:
                    self.preferred_format = format_
                    break
        if self.preferred_format is None:
            self.preferred_format = self.formats[0]


    @classmethod
    def get_planes(cls, drm):
        planes = []
        arg = DrmModeGetPlaneResC()

        fcntl.ioctl(drm.fd, DRM_IOCTL_MODE_GETPLANERESOURCES, arg)

        plane_ids = (ctypes.c_uint32*arg.count_planes)()
        arg.plane_id_ptr = ctypes.cast(ctypes.pointer(plane_ids), ctypes.c_void_p).value

        fcntl.ioctl(drm.fd, DRM_IOCTL_MODE_GETPLANERESOURCES, arg)

        for i in range(arg.count_planes):
            planes.append(drm.get_plane(plane_ids[i]))
        return planes
