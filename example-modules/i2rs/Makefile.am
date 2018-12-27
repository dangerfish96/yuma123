netconfmodule_LTLIBRARIES = libi2rs.la

noinst_HEADERS = ietf-i2rs-rib.h com.h

libi2rs_la_SOURCES = \
$(top_srcdir)/example-modules/i2rs/ietf-i2rs-rib.c $(top_srcdir)/example-modules/i2rs/Socket.c

libi2rs_la_CPPFLAGS = -I $(top_srcdir)/netconf/src/ -I$(top_srcdir)/netconf/src/agt -I$(top_srcdir)/netconf/src/mgr -I$(top_srcdir)/netconf/src/ncx -I$(top_srcdir)/netconf/src/platform -I$(top_srcdir)/netconf/src/ydump $(XML_CPPFLAGS)

libi2rs_la_LDFLAGS = -module $(top_builddir)/netconf/src/agt/libyumaagt.la $(top_builddir)/netconf/src/ncx/libyumancx.la


examples_yang_DATA = $(top_srcdir)/example-modules/i2rs/ietf-i2rs-rib.yang
