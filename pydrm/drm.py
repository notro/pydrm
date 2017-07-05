import os
from ctypes import *
import fcntl

from .version import DrmVersion

from .drm_h import *

from .connector import DrmConnector
from .encoder import DrmEncoder
from .crtc import DrmCrtc
from .plane import DrmPlane
from .framebuffer import DrmFramebuffer
from .format import DrmFormat


def drm_set_client_cap(fd, capability, value):
    c = DrmSetClientCapC()
    c.capability = capability
    c.value = value
    fcntl.ioctl(fd, DRM_IOCTL_SET_CLIENT_CAP, c)


class DrmCapabilities(object):
    def __init__(self, drm):
        self._drm = drm
        self._caps = {}
        self._caps['DRM_CAP_DUMB_BUFFER'] = DRM_CAP_DUMB_BUFFER
        self._caps['DRM_CAP_VBLANK_HIGH_CRTC'] = DRM_CAP_VBLANK_HIGH_CRTC
        self._caps['DRM_CAP_DUMB_PREFERRED_DEPTH'] = DRM_CAP_DUMB_PREFERRED_DEPTH
        self._caps['DRM_CAP_DUMB_PREFER_SHADOW'] = DRM_CAP_DUMB_PREFER_SHADOW
        self._caps['DRM_CAP_PRIME'] = DRM_CAP_PRIME
        self._caps['DRM_PRIME_CAP_IMPORT'] = DRM_PRIME_CAP_IMPORT
        self._caps['DRM_PRIME_CAP_EXPORT'] = DRM_PRIME_CAP_EXPORT
        self._caps['DRM_CAP_TIMESTAMP_MONOTONIC'] = DRM_CAP_TIMESTAMP_MONOTONIC
        self._caps['DRM_CAP_ASYNC_PAGE_FLIP'] = DRM_CAP_ASYNC_PAGE_FLIP
        self._caps['DRM_CAP_CURSOR_WIDTH'] = DRM_CAP_CURSOR_WIDTH
        self._caps['DRM_CAP_CURSOR_HEIGHT'] = DRM_CAP_CURSOR_HEIGHT
        self._caps['DRM_CAP_ADDFB2_MODIFIERS'] = DRM_CAP_ADDFB2_MODIFIERS
        self._caps['DRM_CAP_PAGE_FLIP_TARGET'] = DRM_CAP_PAGE_FLIP_TARGET

    def get(self, capability):
        arg = DrmGetCapC()
        arg.capability = capability
        fcntl.ioctl(self._drm.fd, DRM_IOCTL_GET_CAP, arg)
        return int(arg.value)

    def __getattr__(self, attr):
        if attr in self._caps.keys():
            return self.get(self._caps[attr])
        else:
            return object.__getattr__(self, attr)

    def inspect(self, detailed=False):
        s = "Capabilities:\n"
        for name, cap in self._caps.items():
            try:
                val = self.get(cap)
            except:
                val = "n/a"
            s += "  %s = %s\n" % (name, val)
        return s


#                ("fb_id_ptr", c_uint64),
#                ("crtc_id_ptr", c_uint64),
#                ("connector_id_ptr", c_uint64),
#                ("encoder_id_ptr", c_uint64),
#                ("count_fbs", c_uint32),
#                ("count_crtcs", c_uint32),
#                ("count_connectors", c_uint32),
#                ("count_encoders", c_uint32),
#                ("min_width", c_uint32),
#                ("max_width", c_uint32),
#                ("min_height", c_uint32),
#                ("max_height", c_uint32)


class Drm(object):
    def __init__(self, minor=None):
        self._connectors = []
        self._encoders = []
        self._crtcs = []
        self._framebuffers = []
        self._planes = []
        if minor is None:
            minor = self.find_first()
        if minor is None:
            raise RuntimeError("couldn't find a drm device\n")
        self.minor = minor
        self.filename = "/dev/dri/card%d" % minor
        self._version = None

        self.fd = open(self.filename, 'r+b', buffering=0)
        self.cap = DrmCapabilities(self)

        drm_set_client_cap(self.fd, DRM_CLIENT_CAP_UNIVERSAL_PLANES, 1)
        self.fetch()

    def find_first(self):
        for i in range(64):
            if os.path.exists("/dev/dri/card%d" % i):
                return i
        return None

    def fetch(self):
        fd = self.fd
        arg = DrmModeCardResC()
        u32_128 = c_uint32 * 128

        fb_ids = u32_128()
        arg.fb_id_ptr = cast(pointer(fb_ids), c_void_p).value
        arg.count_fbs = 128

        crtc_ids = u32_128()
        arg.crtc_id_ptr = cast(pointer(crtc_ids), c_void_p).value
        arg.count_crtcs = 128

        connector_ids = u32_128()
        arg.connector_id_ptr = cast(pointer(connector_ids), c_void_p).value
        arg.count_connectors = 128

        encoder_ids = u32_128()
        arg.encoder_id_ptr = cast(pointer(encoder_ids), c_void_p).value
        arg.count_encoders = 128

        try:
            fcntl.ioctl(fd, DRM_IOCTL_MODE_GETRESOURCES, arg)
        except IOError as e:
            if e.errno == 22: # EINVAL: no DRIVER_MODESET (VGEM)
                return
            else:
                raise

        for i in range(arg.count_fbs):
            self.get_framebuffer(fb_ids[i])

        for i in range(arg.count_connectors):
            self.get_connector(connector_ids[i])

        for i in range(arg.count_encoders):
            self.get_encoder(encoder_ids[i])

        for i in range(arg.count_crtcs):
            self.get_crtc(crtc_ids[i])

        DrmPlane.get_planes(self)


    @property
    def version(self):
        if self._version is None:
            self._version = DrmVersion(self)
        return self._version

    @property
    def connectors(self):
        return list(self._connectors)

    def get_connector(self, id_):
        for conn in self._connectors:
            if conn.id == id_:
                return conn
        conn = DrmConnector(self, id_)
        self._connectors.append(conn)
        return conn

    def find_connectors(self):
        return [conn for conn in self._connectors if conn.status == 1]
        #for conn in self._connectors:
        #    if conn.status == 1:
        #        return conn
        #return None

    @property
    def encoders(self):
        return list(self._encoders)

    def get_encoder(self, id_):
        for enc in self._encoders:
            if enc.id == id_:
                return enc
        enc = DrmEncoder(self, id_)
        self._encoders.append(enc)
        return enc

    @property
    def crtcs(self):
        return list(self._crtcs)

    def get_crtc(self, id_):
        for crtc in self._crtcs:
            if crtc.id == id_:
                return crtc
        crtc = DrmCrtc(self, id_)
        self._crtcs.append(crtc)
        return crtc

    def find_crtcs(self, *connectors):
        possible_crtcs = set(self.crtcs)
        active_crtcs = set()
        for connector in connectors:
            for encoder in connector.encoders:
                possible_crtcs &= set(encoder.possible_crtcs)
                if encoder.crtc:
                    active_crtcs.add(encoder.crtc)

        return list(active_crtcs) + list(possible_crtcs - active_crtcs)

    @property
    def framebuffers(self):
        return list(self._framebuffers)

    def get_framebuffer(self, id_):
        for fb in self._framebuffers:
            if fb.id == id_:
                return fb
        fb = DrmFramebuffer.from_id(self, id_)
        self._framebuffers.append(fb)
        return fb

    @property
    def planes(self):
        return list(self._planes)

    def get_plane(self, id_):
        for plane in self._planes:
            if plane.id == id_:
                return plane
        plane = DrmPlane(self, id_)
        self._planes.append(plane)
        return plane

    def find_planes(self, *crtcs):
        return [plane for plane in self.planes if set(plane.possible_crtcs) & set(crtcs)]

    def __repr__(self):
        return "Drm(%s)" % self.minor

    def inspect(self, detailed=False):
        s = ""
        s += self.version.inspect(detailed)
        s += self.cap.inspect(detailed)
        for encoder in self.encoders:
            s += encoder.inspect(detailed)
        for connector in self.connectors:
            s += connector.inspect(detailed)
        for crtc in self.crtcs:
            s += crtc.inspect(detailed)
        for plane in self.planes:
            s += plane.inspect(detailed)
        for framebuffer in self.framebuffers:
            s += framebuffer.inspect(detailed)
        return s


class SimpleDrm(object):
    def __init__(self, minor=None, conn=None, mode="", vrefresh=0, format=None):
        self.drm = Drm(minor)
        self.connector = None
        self.crtc = None
        self.plane = None
        self.format = None
        self.framebuffer = None
        self.image = None
        self._draw = None
        self._setup(conn, mode, vrefresh, format)

    def _setup(self, conn=None, mode="", vrefresh=0, format=None):
        from .image import DrmImageFramebuffer
        if conn is None:
            conns = self.drm.find_connectors()[:1]
        else:
            if type(conn) == str:
                conns = [conn for conn in self.drm.connectors if conn.name.lower() in conn.lower()]
            else:
                conns = [conn for conn in self.drm.connectors if conn.id == int(conn)]
        if not conns:
            raise ValueError("could not find a connector")
        self.connector = conns[0]

        self.mode = self.connector.find_mode(mode, vrefresh)
        if not self.mode:
            raise ValueError("mode not found: %s %s" % (mode, vrefresh if vrefresh else ""))

        crtcs = self.drm.find_crtcs(self.connector)
        if not crtcs:
            raise ValueError("could not find a crtc for connector: %s" % self.connector.name)
        self.crtc = crtcs[0]

        planes = self.drm.find_planes(self.crtc)
        if not planes:
            raise ValueError("couldn't find plane for crtc %s\n" % self.crtc.id)
        self.plane = planes[0]

        if format:
            try:
                self.format = DrmFormat(format)
            except NotImplementedError:
                raise ValueError("format '%s' is not supported\n" % format)
            if not self.format in self.plane.formats:
                raise ValueError("format '%s' is not supported by the plane\n" % format)
        else:
            self.format = self.plane.preferred_format

        self.framebuffer = DrmImageFramebuffer(self.drm, self.format, self.mode.hdisplay, self.mode.vdisplay)
        self.image = self.framebuffer.image

        self.crtc.set(self.framebuffer, 0, 0, self.mode, self.connector)

    @property
    def draw(self):
        if self._draw is None:
            from PIL import ImageDraw
            self._draw = ImageDraw.Draw(self.image)
        return self._draw

    def enable(self):
        self.connector.DPMS = 0

    def disable(self):
        self.connector.DPMS = 3

    def flush(self):
        self.framebuffer.flush()

    def inspect(self, detailed=False):
        s = "SimpleDrm(%s)\n" % self.drm.minor
        if detailed:
            s += self.drm.version.inspect()
        else:
            s += "  version = %s\n" % self.drm.version

        for attr in ['connector', 'mode', 'crtc', 'plane', 'format', 'framebuffer']:
            obj = getattr(self, attr)
            if detailed:
                s += obj.inspect()
            else:
                s += "  %s = %s\n" % (attr, obj)
        if not detailed:
            s += "  image = %s\n" % self.image
            s += "  draw = %s\n" % self.draw
        return s
