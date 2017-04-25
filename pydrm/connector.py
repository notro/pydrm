import fcntl
import ctypes

from .base import DrmObject, DrmMode
from .drm_h import DRM_IOCTL_MODE_GETCONNECTOR
from .drm_mode_h import DrmModeGetConnectorC, DrmModeModeinfoC, drm_connector_type_id_name, DRM_MODE_OBJECT_CONNECTOR


#                ("encoders_ptr", c_uint64),
#                ("modes_ptr", c_uint64),
#                ("props_ptr", c_uint64),
#                ("prop_values_ptr", c_uint64),
#
#                ("count_modes", c_uint32),
#                ("count_props", c_uint32),
#                ("count_encoders", c_uint32),
#
#                ("encoder_id", c_uint32),
#                ("connector_id", c_uint32),
#                ("connector_type", c_uint32),
#                ("connector_type_id", c_uint32),
#
#                ("connection", c_uint32),
#                ("mm_width", c_uint32),
#                ("mm_height", c_uint32),
#                ("subpixel", c_uint32),

class DrmConnector(DrmObject):
    def __init__(self, drm, id):
        self._drm = drm
        self.id = int(id)
        self._encoders = []
        self.fetch()

    def fetch(self):
        arg = DrmModeGetConnectorC()
        arg.connector_id = self.id

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETCONNECTOR, arg)

        encoder_ids = (ctypes.c_uint32*arg.count_encoders)()
        arg.encoders_ptr = ctypes.cast(ctypes.pointer(encoder_ids), ctypes.c_void_p).value

        modes_c = (DrmModeModeinfoC*arg.count_modes)()
        arg.modes_ptr = ctypes.cast(ctypes.pointer(modes_c), ctypes.c_void_p).value

        # Use get_props() instead
        arg.count_props = 0

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETCONNECTOR, arg)

        self._arg = arg
        self.type = arg.connector_type
        self.type_id = arg.connector_type_id
        self.status = arg.connection

        self.mm_width = arg.mm_width
        self.mm_height = arg.mm_height
        self.subpixel = arg.subpixel

        for i in range(arg.count_encoders):
            self._encoders.append(self._drm.get_encoder(encoder_ids[i]))

        if (arg.encoder_id):
            self.encoder = self._drm.get_encoder(res.encoder_id)
        else:
            self.encoder = None

        self.modes = [DrmMode(modes_c[i]) for i in range(arg.count_modes)]

        self.name = "%s-%s" %(drm_connector_type_id_name(self.type), self.type_id)

        self.get_props(DRM_MODE_OBJECT_CONNECTOR)

    @property
    def encoders(self):
        return list(self._encoders)

    @property
    def preferred_mode(self):
        for mode in self.modes:
            if mode.preferred:
                return mode
        return None

    def find_mode(self, modestr=None, vrefresh=None):
        #print "find_modes(%s,%s)\n" % (modestr, vrefresh)
        mode = None
        if modestr:
            for m in self.modes:
                if m.name == modestr:
                    if vrefresh is None or m.vrefresh == vrefresh:
                        mode = m
                        break
        else:
            mode = self.preferred_mode
        return mode
