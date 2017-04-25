#
# This is a clone of libdrm/tests/modetest/modetest.c
#
#  DRM based mode setting test program
#  Copyright 2008 Tungsten Graphics
#    Jakob Bornecrantz <jakob@tungstengraphics.com>
#  Copyright 2008 Intel Corporation
#    Jesse Barnes <jesse.barnes@intel.com>

import sys
import argparse

from pydrm import Drm
from pydrm.property import DrmPropertyEnum
from pydrm.format import DrmFormat

# for Python 2
try:
   input = raw_input
except NameError:
   pass


def fail(msg):
    sys.stderr.write(msg)
    exit(1)

def connector_status_name(status):
    if status == 1:
        return "connected"
    elif status == 2:
        return "disconnected"
    else:
        return "unknown"

mode_type_names = [
    "builtin",
    "clock_c",
    "crtc_c",
    "preferred",
    "default",
    "userdef",
    "driver"]

def mode_type_str(type_):
    s = ""
    sep = ""
    for i in range(len(mode_type_names)):
        if type_ & (1 << i):
            s += "%s%s" % (sep, mode_type_names[i])
            sep = ", "
    return s

mode_flag_names = [
    "phsync",
    "nhsync",
    "pvsync",
    "nvsync",
    "interlace",
    "dblscan",
    "csync",
    "pcsync",
    "ncsync",
    "hskew",
    "bcast",
    "pixmux",
    "dblclk",
    "clkdiv2"]

def mode_flag_str(flags):
    s = ""
    sep = ""
    for i in range(len(mode_flag_names)):
        if flags & (1 << i):
            s += "%s%s" % (sep, mode_flag_names[i])
            sep = ", "
    return s

def dump_mode(mode):
    s = "%s %d %d %d %d %d %d %d %d %d %d" % (
           mode.name,
           mode.vrefresh,
           mode.hdisplay,
           mode.hsync_start,
           mode.hsync_end,
           mode.htotal,
           mode.vdisplay,
           mode.vsync_start,
           mode.vsync_end,
           mode.vtotal,
           mode.clock)

    s += " flags: "
    s += mode_flag_str(mode.flags)
    s += "; type: "
    s += mode_type_str(mode.type)
    s += "\n"

    return s

def dump_prop(prop):
    s = "\t%d" % prop.id
    s += " %s:\n" % prop.name
    s += "\t\tflags: "
    if prop.immutable:
        s += "immutable "
    s += "%s\n" % prop.type_name

#    if (drm_property_type_is(prop, DRM_MODE_PROP_SIGNED_RANGE)) {
#        printf("\t\tvalues:");
#        for (i = 0; i < prop->count_values; i++)
#            printf(" %"PRId64, U642I64(prop->values[i]));
#        printf("\n");
#    }
#
#    if (drm_property_type_is(prop, DRM_MODE_PROP_RANGE)) {
#        printf("\t\tvalues:");
#        for (i = 0; i < prop->count_values; i++)
#            printf(" %"PRIu64, prop->values[i]);
#        printf("\n");
#    }
#
#    if (drm_property_type_is(prop, DRM_MODE_PROP_ENUM)) {
#        printf("\t\tenums:");
#        for (i = 0; i < prop->count_enums; i++)
#            printf(" %s=%llu", prop->enums[i].name,
#                   prop->enums[i].value);
#        printf("\n");
    if isinstance(prop, DrmPropertyEnum):
        s += "\t\tenums:"
        for val, name in prop.enum.items():
            s += " %s=%s" % (name, val)
        s += "\n"
#    } else if (drm_property_type_is(prop, DRM_MODE_PROP_BITMASK)) {
#        printf("\t\tvalues:");
#        for (i = 0; i < prop->count_enums; i++)
#            printf(" %s=0x%llx", prop->enums[i].name,
#                   (1LL << prop->enums[i].value));
#        printf("\n");
    elif isinstance(prop, DrmPropertyBitmask):
        s += "\t\tvalues:"
        for val, name in prop.enum.items():
            s += " %s=0x%x" % (name, 1 << val)
        s += "\n"
#    } else {
#        assert(prop->count_enums == 0);
#    }
#
#    if (drm_property_type_is(prop, DRM_MODE_PROP_BLOB)) {
#        printf("\t\tblobs:\n");
#        for (i = 0; i < prop->count_blobs; i++)
#            dump_blob(dev, prop->blob_ids[i]);
#        printf("\n");
#    } else {
#        assert(prop->count_blobs == 0);
#    }

    s += "\t\tvalue:"
#    if (drm_property_type_is(prop, DRM_MODE_PROP_BLOB))
#        dump_blob(dev, value);
#    else if (drm_property_type_is(prop, DRM_MODE_PROP_SIGNED_RANGE))
#        printf(" %"PRId64"\n", value);
#    else
#        printf(" %"PRIu64"\n", value);
    s += " %s\n" % prop.value

    return s

def dump_props(props):
        if len(props.props):
            s = "  props:\n"
        else:
            return ""

        for prop in props.props:
            s += dump_prop(prop)

        return s

def dump_encoders(drm):
    s = "Encoders:\n"
    s += "id\tcrtc\ttype\tpossible crtcs\tpossible clones\n"
    for encoder in drm.encoders:
        s += "%d\t%d\t%s\t%-15s\t%-15s\n" % (
               encoder.id,
               encoder.crtc.id if encoder.crtc else 0,
               encoder.type_name,
               ', '.join([str(crtc.id) for crtc in encoder.possible_crtcs]),
               ', '.join([str(encoder.id) for encoder in encoder.possible_clones]))
    return s

def dump_connectors(drm):
    s = "Connectors:\n"
    s += "id\tencoder\tstatus\t\tname\t\tsize (mm)\tmodes\tencoders\n"
    for connector in drm.connectors:
        s += "%d\t%d\t%s\t%-15s\t%dx%d\t\t%d\t" %(
               connector.id,
               connector.encoder.id if connector.encoder else 0,
               connector_status_name(connector.status),
               connector.name,
               connector.mm_width, connector.mm_height,
               len(connector.modes))

        for j in range(len(connector.encoders)):
            if j > 0:
                s += ", "
            s += "%d" % connector.encoders[j].id
        s += "\n"

        if len(connector.modes):
            s += "  modes:\n"
            s += "\tname refresh (Hz) hdisp hss hse htot vdisp vss vse vtot)\n"
            for mode in connector.modes:
                s += "\t%s" % dump_mode(mode)

        s += dump_props(connector.props)
    return s

def dump_crtcs(drm):
    s = "CRTCs:\n"
    s += "id\tfb\tpos\tsize\n"
    for crtc in drm.crtcs:
        s += "%d\t%d\t(%d,%d)\t(%dx%d)\n" % (
               crtc.id,
               crtc.fb.id if crtc.fb else 0,
               crtc.x, crtc.y,
               crtc.width, crtc.height)
        s += dump_mode(crtc.mode) if crtc.mode else ""

        s += dump_props(crtc.props)
    return s

def dump_planes(drm):
    s = "Planes:\n"
    s += "id\tcrtc\tfb\tCRTC x,y\tx,y\tgamma size\tpossible crtcs\n"

    for plane in drm.planes:
        s += "%d\t%d\t%d\t%d,%d\t\t%d,%d\t%-8d\t%s\n" % (
               plane.id,
               plane.crtc.id if plane.crtc else 0,
               plane.fb.id if plane.fb else 0,
# FIXME: what are these?
#               plane.crtc_x, plane.crtc_y, plane.x, plane.y,
               999, 999, 999, 999,
               plane.gamma_size,
               ', '.join([str(crtc.id) for crtc in plane.possible_crtcs]))

        if not plane.formats:
            continue

        s += "  formats:"
        for format_ in plane.formats:
            s += " %s" % format_.name
        s += "\n"

        s += dump_props(plane.props)
    return s

def dump_framebuffers(drm):
    s = "Frame buffers:\n"
    s += "id\tsize\t\tpitch\n"
    for fb in drm.framebuffers:
        s += "%u\t(%ux%u)\t%u\n" %(
               fb.id,
               fb.width, fb.height,
               fb.pitch)
    return s





def draw_smpte_rects(x, y, width, height, colors):
    for i in range(len(colors)):
        draw.rectangle([(x + (width * i), y), (x + (width * (i + 1)), y + height)], fill=colors[i], outline=colors[i])

def draw_smpte_pattern(draw):
    fb_width, fb_height = draw.im.size

    # top colors: grey/silver, yellow, cyan, green, magenta, red, blue
    y = 0
    width = fb_width / 7
    height = fb_height * 6 / 9
    draw_smpte_rects(0, 0, width, height, ['#c0c0c0', '#c0c000', '#00c0c0', '#00c000', '#c000c0', '#c00000', '#0000c0'])

    # middle colors: blue, black magenta, black, cyan, black, grey
    y = height
    width = fb_width / 7
    height = fb_height * 1 / 9
    draw_smpte_rects(0, y, width, height, ['#0000c0', '#131313', '#c000c0', '#131313', '#00c0c0', '#131313', '#c0c0c0'])

    # bottom colors: in-phase, super white, quadrature, black, 3.5%, 7.5%, 11.5%, black
    y += height
    width = fb_width / 6
    height = fb_height * 2 / 9
    draw_smpte_rects(0, y, width, height, ['#00214c', '#ffffff', '#32006a', '#131313'])

    x = width * 4
    width = fb_width / 6 / 3
    draw_smpte_rects(x, y, width, height, ['#090909', '#131313', '#1d1d1d'])

    x = fb_width * 5 / 6
    width = fb_width / 6
    draw_smpte_rects(x, y, width, height, ['#131313'])

def draw_mono_pattern(draw):
    fb_width, fb_height = draw.im.size
    c = 'white'
    draw.rectangle([(0, 0), (fb_width - 1, fb_height - 1)], fill=None, outline=c)
    draw.line([(0, 0), (fb_width - 1, fb_height - 1)], fill=c)
    draw.line([(fb_width - 1, 0), (0, fb_height - 1)], fill=c)
    draw.ellipse([(fb_width*1/4, fb_height*1/4), (fb_width*3/4, fb_height*3/4)], fill=None, outline=c)



parser = argparse.ArgumentParser(epilog="Default is to dump all info on the first available device")

parser.add_argument("-c", help="list connectors", action="store_true")
parser.add_argument("-e", help="list encoders", action="store_true")
parser.add_argument("-f", help="list framebuffers", action="store_true")
parser.add_argument("-p", help="list CRTCs and planes (pipes)", action="store_true")

test = parser.add_argument_group('Test options')

#    fprintf(stderr, "\n Test options:\n\n");
#    fprintf(stderr, "\t-P <crtc_id>:<w>x<h>[+<x>+<y>][*<scale>][@<format>]\tset a plane\n");


#   struct pipe_arg {
#       const char **cons;
#       uint32_t *con_ids;
#       unsigned int num_cons;
#       uint32_t crtc_id;
#       char mode_str[64];
#       char format_str[5];
#       unsigned int vrefresh;
#       unsigned int fourcc;
#       drmModeModeInfo *mode;
#       struct crtc *crtc;
#       unsigned int fb_id[2], current_fb_id;
#       struct timeval start;
#
#       int swap_count;
#   };

class PipeArgs(object):
    def __init__(self):
        self.connector_ids = []
        self.crtcid = None
        self.modestr = ""
        self.vrefresh = None
        self.formatstr = ""
        self.format = None
        self.connectors = []
        self.mode = None
        self.crtcs = []


class SetModeAction(argparse.Action):
#    def __init__(self, nargs=0, **kw):
#        super().__init__(nargs=nargs, **kw)
#    def __init__(self, option_strings, dest, nargs=0, **kwargs):
#        super(SetModeAction, self).__init__(option_strings, dest, nargs=nargs, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        #print '%r %r %r' % (namespace, values, option_string)
        pipeargs = getattr(namespace, self.dest)
        if pipeargs is None:
            pipeargs = []
            setattr(namespace, self.dest, pipeargs)

        p = PipeArgs()
        pipeargs.append(p)

        if values is None:
            return

        connstr, delim, modestr = values.partition(':')
        if ':' in modestr:
            raise argparse.ArgumentError(self, 'extra :')

        if connstr:
            connid, delim, crtcid = connstr.partition('@')
            if connid:
                p.connector_ids = [int(i) for i in connid.split(',')]
            if '@' in crtcid:
                raise argparse.ArgumentError(self, 'extra @')
            if crtcid:
                try:
                    p.crtcid = int(crtcid)
                except ValueError:
                    raise argparse.ArgumentError(self, "crtc_id=%s is not an int" % crtcid)

        if modestr:
            #print modestr
            mode, delim, format_ = modestr.partition('@')
            #print mode
            if '@' in format_:
                raise argparse.ArgumentError(self, 'extra @')
            mode, delim, vrefresh = mode.partition('-')
            #print "mode %s\n" % mode
            #print "delim %s\n" % delim
            #print "vrefresh %s\n" % vrefresh
            if mode:
                p.modestr = mode
            if vrefresh:
                try:
                    p.vrefresh = int(vrefresh)
                except ValueError:
                    raise argparse.ArgumentError(self, "vrefresh=%s is not an int" % vrefresh)
            if format_:
                p.formatstr = format_

#    fprintf(stderr, "\t-s <connector_id>[,<connector_id>][@<crtc_id>]:<mode>[-<vrefresh>][@<format>]\tset a mode\n");
test.add_argument('-s', action=SetModeAction, nargs='?', help="set mode [<connector_id>,][@<crtc_id>][:[<mode>[-<vrefresh>]][@<format>]]")

test.add_argument("-C", help="test hw cursor", action="store_true")
test.add_argument("-v", help="test vsynced page flipping", action="store_true")

class SetPropertyAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not hasattr(namespace, 'props'):
            namespace.props = []

        try:
            obj_id, prop_name, value = values.split(':')
        except:
            raise argparse.ArgumentError(self, "could not parse '%s'" % values)

        try:
            obj_id = int(obj_id)
        except ValueError:
            raise argparse.ArgumentError(self, "obj_id=%s is not an int" % obj_id)

        namespace.props.append([obj_id, prop_name, value])

test.add_argument('-w', action=SetPropertyAction, help="set property <obj_id>:<prop_name>:<value>")

parser.add_argument("-d", help="drop master after mode set", action="store_true")
parser.add_argument("-M", help="use the given driver", metavar=('module'))
parser.add_argument("-D", help="use the given device", metavar=('device'))

parser.add_argument("--pattern", help="test pattern (default:smpte)", choices=['smpte', 'mono'], default="smpte")


args = parser.parse_args()

# default dump all
if len(sys.argv) == 1:
    args.c = args.e = args.f = args.p = True

#print(args)

class Device(object):
    def __init__(self, drm):
        self.drm = drm
        self.width = 0
        self.height = 0
        self.fb = None
        self.bo = None
        self.cursor = None

drm = Drm()

if args.e:
    print(dump_encoders(drm))
if args.c:
    print(dump_connectors(drm))
if args.p:
    print(dump_crtcs(drm))
    print(dump_planes(drm))
if args.f:
    print(dump_framebuffers(drm))


if args.s:
    if not drm.cap.DRM_CAP_DUMB_BUFFER:
        fail("driver doesn't support the dumb buffer API\n")

    dev = Device(drm)

    x = 0
    for pipe in args.s:

        if pipe.connector_ids:
            for conn_id in pipe.connector_ids:
                conn = [conn for conn in drm.connectors if conn.id == conn_id]
                if not conn:
                    fail("couldn't find connector with id: %s\n" % conn_id)
                pipe.connectors.extend(conn)
        else:
            # default is the first connected connector
            pipe.connectors = drm.find_connectors()[:1]
            if not pipe.connectors:
                fail("couldn't find any connected connector\n")

        pipe.mode = pipe.connectors[0].find_mode(pipe.modestr, pipe.vrefresh)
        if not pipe.mode:
            fail("mode not found: %s %s\n" % (pipe.modestr, pipe.vrefresh if pipe.vrefresh else ""))

        if pipe.crtcid:
            pipe.crtcs = [crtc for crtc in drm.crtcs if crtc.id == pipe.crtcid]
        else:
            pipe.crtcs = drm.find_crtcs(*pipe.connectors)
        if not pipe.crtcs:
            fail("crtc not found %s\n" % pipe.crtcid if pipe.crtcid else "")
        pipe.crtc = pipe.crtcs[0]

        dev.width += pipe.mode.hdisplay
        if dev.height < pipe.mode.vdisplay:
            dev.height = pipe.mode.vdisplay

        pipe.planes = drm.find_planes(pipe.crtc)
        if not pipe.planes:
            fail("couldn't find plane for crtc %s\n" % pipe.crtc.id)
        pipe.plane = pipe.planes[0]

        if pipe.formatstr:
            pipe.format = None
            try:
                pipe.format = DrmFormat(pipe.formatstr)
            except NotImplementedError:
                fail("format '%s' is not supported\n" % pipe.formatstr)
            if not pipe.format in pipe.plane.formats:
                fail("format '%s' is not supported by the plane\n" % pipe.formatstr)
        else:
            pipe.format = pipe.plane.preferred_format

        from pydrm.image import DrmImageFramebuffer
        dev.fb = DrmImageFramebuffer(dev.drm, pipe.format, dev.width, dev.height)

        pipe.crtc.set(dev.fb, x, 0, pipe.mode, *pipe.connectors)
        x += pipe.mode.hdisplay

        from PIL import ImageDraw
        draw = ImageDraw.Draw(dev.fb.image)

        if args.pattern == 'smpte':
            draw_smpte_pattern(draw)
        elif args.pattern == 'mono':
            draw_mono_pattern(draw)

        dev.fb.flush()

        input("Press enter to stop")

        if 0:
            dev.fb.remove()

            print(dump_framebuffers(drm))

            print(pipe.crtc.inspect(True))
            pipe.crtc.fetch()
            print(pipe.crtc.inspect(True))

