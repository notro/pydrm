from .drm_mode_h import DRM_MODE_TYPE_PREFERRED

class DrmObject(object):
    def get_props(self, type_):
        import pydrm.property
        try:
            self.props = pydrm.property.DrmProperties(self._drm, self.id, type_)
            # make inspect() pick up the properties
            for prop in self.props:
                prop_name = prop.name
                inspect_prop_name = "_%s" % prop_name
                if not hasattr(self, inspect_prop_name):
                    setattr(self, inspect_prop_name, None)
        except IOError as e:
            if e.errno != 22: # EINVAL: no properties
                raise

    def __getattr__(self, name):
        if name == 'props':
            raise AttributeError()
        try:
            return self.props.get(name).value
        except AttributeError:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        try:
            self.props.get(name).value = value
        except AttributeError:
            object.__setattr__(self, name, value)

    def __repr__(self):
        if hasattr(self, "id"):
            return "%s(%s)" % (type(self).__name__, self.id)
        elif hasattr(self, "name"):
            return "%s(%s)" % (type(self).__name__, self.name)
        else:
            return "%s()" % (type(self).__name__)

    def inspect(self, detailed=False):
        s = "%s\n" % self
        for attr in vars(self):
            if not (attr.startswith('_') or attr == 'id'):
                s += "  %s = %s\n" % (attr, getattr(self, attr))
            elif attr.startswith('_'):
                try:
                    v = getattr(self, attr[1:])
                    s += "  %s = %s\n" % (attr[1:], v)
                except:
                    pass

        if not hasattr(self, "_arg") or not detailed:
            return s

        s += "\n  %s:\n" % type(self._arg).__name__
        for attr in type(self._arg)._fields_:
            val = getattr(self._arg, attr[0])
            try:
                s += "    %s = %s\n" % (attr[0], val[:]) # show array content
            except:
                s += "    %s = %s\n" % (attr[0], val)

        return s

class DrmMode(DrmObject):
    def __init__(self, arg):
        self._arg = arg
        for attr in type(arg)._fields_:
            setattr(self, attr[0], getattr(arg, attr[0]))
        self.preferred = bool(self.type & DRM_MODE_TYPE_PREFERRED)
