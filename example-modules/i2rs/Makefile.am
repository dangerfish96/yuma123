netconfmodule_LTLIBRARIES = libietf-i2rs-rib.la

noinst_HEADERS = ietf-i2rs-rib.h com.h Socket.h

libietf_i2rs_rib_la_SOURCES = \
$(top_srcdir)/example-modules/i2rs/ietf-i2rs-rib.c $(top_srcdir)/example-modules/i2rs/Socket.c $(top_srcdir)/example-modules/i2rs/com.c


libietf_i2rs_rib_la_CPPFLAGS = -I $(top_srcdir)/netconf/src/ -I$(top_srcdir)/netconf/src/agt -I$(top_srcdir)/netconf/src/mgr -I$(top_srcdir)/netconf/src/ncx -I$(top_srcdir)/netconf/src/platform -I$(top_srcdir)/netconf/src/ydump $(XML_CPPFLAGS)

libietf_i2rs_rib_la_LDFLAGS = -module $(top_builddir)/netconf/src/agt/libyumaagt.la $(top_builddir)/netconf/src/ncx/libyumancx.la


examples_yang_DATA = $(top_srcdir)/example-modules/i2rs/ietf-i2rs-rib.yang
