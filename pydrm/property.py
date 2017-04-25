import ctypes
import fcntl

from .base import DrmObject
from .drm_h import DRM_IOCTL_MODE_OBJ_GETPROPERTIES, DRM_IOCTL_MODE_GETPROPERTY, DRM_IOCTL_MODE_OBJ_SETPROPERTY
from .drm_mode_h import DrmModeObjGetPropertiesC, DrmModeObjGetPropertyC, DrmModePropertyEnumC, DrmModeObjSetPropertyC
from .drm_mode_h import DRM_MODE_PROP_PENDING, DRM_MODE_PROP_RANGE, DRM_MODE_PROP_IMMUTABLE, DRM_MODE_PROP_ENUM, DRM_MODE_PROP_BLOB, DRM_MODE_PROP_BITMASK


class DrmProperty(DrmObject):
    def __init__(self, drm, id, obj_id, obj_type):
        self._drm = drm
        self.id = int(id)
        self.obj_id = obj_id
        self.obj_type = obj_type
        self.fetch()

    @property
    def value(self):
        return self.decode(self.get())

    @value.setter
    def value(self, value):
        self.set(self.encode(value))

    def decode(self, value):
        return value

    def encode(self, value):
        return value

    def get(self):
        arg = DrmModeObjGetPropertiesC()
        arg.obj_id = self.obj_id
        arg.obj_type = self.obj_type

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_OBJ_GETPROPERTIES, arg)

        prop_ids = (ctypes.c_uint32*arg.count_props)()
        arg.props_ptr = ctypes.cast(ctypes.pointer(prop_ids), ctypes.c_void_p).value

        prop_values = (ctypes.c_uint32*arg.count_props)()
        arg.prop_values_ptr = ctypes.cast(ctypes.pointer(prop_values), ctypes.c_void_p).value

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_OBJ_GETPROPERTIES, arg)
        self._arg = arg

        vals = [v for i, v in zip(prop_ids, prop_values) if i == self.id]

        return vals[0]

    def set(self, value):
        arg = DrmModeObjSetPropertyC()
        arg.value = value
        arg.prop_id = self.id
        arg.obj_id = self.obj_id
        arg.obj_type = self.obj_type
        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_OBJ_SETPROPERTY, arg)
        self._arg = arg


class DrmPropertyEnum(DrmProperty):
    def fetch(self):
        self.type_name = "enum"
        arg = DrmModeObjGetPropertyC()
        arg.prop_id = self.id

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETPROPERTY, arg)

        if not (arg.count_enum_blobs and (arg.flags & DRM_MODE_PROP_ENUM)):
            raise ValueError("not an enum property")

        if arg.count_values != arg.count_enum_blobs:
            raise ValueError("count_values != count_enum_blobs")

        values = (ctypes.c_uint64*arg.count_values)()
        arg.values_ptr = ctypes.cast(ctypes.pointer(values), ctypes.c_void_p).value

        enum_blobs = (DrmModePropertyEnumC*arg.count_enum_blobs)()
        arg.enum_blob_ptr = ctypes.cast(ctypes.pointer(enum_blobs), ctypes.c_void_p).value

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETPROPERTY, arg)

        self.enum = {}
        for i in range(arg.count_enum_blobs):
            self.enum[int(values[i])] = enum_blobs[i].name

        self._arg = arg
        self.name = arg.name
        self.flags = arg.flags
        self.immutable = True if (arg.flags & DRM_MODE_PROP_IMMUTABLE) else False


class DrmPropertyBitmask(DrmProperty):
    def fetch(self):
        self.type_name = "bitmask"
        raise NotImplementedError


class DrmPropertyBlob(DrmProperty):
    def fetch(self):
        self.type_name = "blob"
        raise NotImplementedError

#    if (prop->flags & DRM_MODE_PROP_PENDING)
#        printf(" pending");
#    if (prop->flags & DRM_MODE_PROP_IMMUTABLE)
#        printf(" immutable");
#    if (drm_property_type_is(prop, DRM_MODE_PROP_SIGNED_RANGE))
#        printf(" signed range");
#    if (drm_property_type_is(prop, DRM_MODE_PROP_RANGE))
#        printf(" range");
#    if (drm_property_type_is(prop, DRM_MODE_PROP_ENUM))
#        printf(" enum");
#    if (drm_property_type_is(prop, DRM_MODE_PROP_BITMASK))
#        printf(" bitmask");
#    if (drm_property_type_is(prop, DRM_MODE_PROP_BLOB))
#        printf(" blob");
#    if (drm_property_type_is(prop, DRM_MODE_PROP_OBJECT))
#        printf(" object");


class DrmProperties(DrmObject):
    def __init__(self, drm, id_, type_):
        self._drm = drm
        self.id = id_
        self.type = type_
        self.props = []

        arg = DrmModeObjGetPropertiesC()
        arg.obj_id = self.id
        arg.obj_type = self.type

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_OBJ_GETPROPERTIES, arg)

        prop_ids = (ctypes.c_uint32*arg.count_props)()
        arg.props_ptr = ctypes.cast(ctypes.pointer(prop_ids), ctypes.c_void_p).value

        prop_values = (ctypes.c_uint32*arg.count_props)()
        arg.prop_values_ptr = ctypes.cast(ctypes.pointer(prop_values), ctypes.c_void_p).value

        fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_OBJ_GETPROPERTIES, arg)

        self._arg = arg

        for i in range(arg.count_props):
            propid = int(prop_ids[i])
            propc = DrmModeObjGetPropertyC()
            propc.prop_id = propid

            fcntl.ioctl(self._drm.fd, DRM_IOCTL_MODE_GETPROPERTY, propc)

            if propc.count_enum_blobs:
                if propc.flags & DRM_MODE_PROP_ENUM:
                    prop = DrmPropertyEnum(self._drm, propid, self.id, self.type)
                elif propc.flags & DRM_MODE_PROP_BITMASK:
                    prop = DrmPropertyBitmask(self._drm, propid, self.id, self.type)
                elif propc.flags & DRM_MODE_PROP_BLOB:
                    prop = DrmPropertyBlob(self._drm, propid, self.id, self.type)
                else:
                    raise ValueError("count_enum_blobs")
            else:
                raise ValueError("not count_enum_blobs")

            self.props.append(prop)

    def __iter__(self):
        return self.props.__iter__()

    def get(self, name):
        for prop in self.props:
            if prop.name == name:
                return prop
        raise AttributeError("no such property: %s" % name)

    def __repr__(self):
        return "%s" % [prop.name for prop in self.props]
