netconfmodule_LTLIBRARIES = libi2rs.la

libi2rs_la_SOURCES = \
$(top_srcdir)/example-modules/i2rs/i2rs.c

libi2rs_la_CPPFLAGS = -I $(top_srcdir)/netconf/src/ -I$(top_srcdir)/netconf/src/agt -I$(top_srcdir)/netconf/src/mgr -I$(top_srcdir)/netconf/src/ncx -I$(top_srcdir)/netconf/src/platform -I$(top_srcdir)/netconf/src/ydump $(XML_CPPFLAGS)
libi2rs_la_LDFLAGS = -module $(top_builddir)/netconf/src/agt/libyumaagt.la $(top_builddir)/netconf/src/ncx/libyumancx.la 


examples_yang_DATA = $(top_srcdir)/example-modules/i2rs/i2rs.yang
