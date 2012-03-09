Name:           yuma
Version:        2.2
Release:        2%{?dist}
Summary:        YANG-based Unified Modular Automation Tools

Group:          Development/Tools
License:        BSD
URL:            http://www.netconfcentral.org/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Yuma is a YANG-based NETCONF-over-SSH client and server
development toolkit.  The netconfd server includes an automated
central NETCONF protocol stack, based directly on YANG modules.
The yangcli client supports single sessions over SSH with some
script support.  The yangdump and yangdiff development tools are also
included, to compile and process YANG modules.

Requires: ncurses
Requires: libxml2
Requires: libssh2

# do not build the yuma-debug packages
%define debug_package %{nil}

# set to release number above
%define myrel 2

# main package rules

%prep
%setup -q

%build
cd libtecla
./configure --prefix=$RPM_BUILD_ROOT 
cd ..
%ifarch x86_64
make LIB64=1 RELEASE=%{myrel} %{?_smp_mflags}
%else
make RELEASE=%{myrel} %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ifarch x86_64
make install LDFLAGS+=--build-id LIB64=1 RELEASE=%{myrel} DESTDIR=$RPM_BUILD_ROOT
%else
make install LDFLAGS+=--build-id RELEASE=%{myrel} DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/yangcli
%{_bindir}/yangdump
%{_bindir}/yangdiff
%{_sbindir}/netconfd
%{_sbindir}/netconf-subsystem
%{_sysconfdir}/yuma/yangcli-sample.conf
%{_sysconfdir}/yuma/yangdiff-sample.conf
%{_sysconfdir}/yuma/yangdump-sample.conf
%{_sysconfdir}/yuma/netconfd-sample.conf
/usr/share/doc/yuma/yuma-legal-notices.pdf
/usr/share/doc/yuma/AUTHORS
/usr/share/doc/yuma/README
/usr/share/doc/yuma/COPYRIGHT
%{_mandir}/man1/yangcli.1.gz
%{_mandir}/man1/yangdiff.1.gz
%{_mandir}/man1/yangdump.1.gz
%{_mandir}/man1/netconfd.1.gz
%{_mandir}/man1/netconf-subsystem.1.gz
%{_datadir}/yuma/modules/*
%{_libdir}/libncx.so*
%{_libdir}/libagt.so*
%{_libdir}/yuma/

%post
echo "Yuma installed."
echo "Check the user manuals in /usr/share/doc/yuma"

%changelog
* Fri Mar 09 2012 Andy Bierman <andy at netconfcentral.org> 2.2-2 [1737]
  * netconfd
    * enhanced unique-stmt checking to support embedded lists
      change val_unique_t to hold XPath struct instead of value back-ptr
      Note:  <non-unique> value in error reporting for unique-error may not
      be correct if list with multiple instances has error.  Will indicate
      the first node in the node-set with an error, which may not be
      the instance that caused a non-unique error within a nested list
    * fix bug in yuma-arp: SIL callbacks not getting loaded
      properly because revision date was wrong
    * fix bug in new instance_check code where false when-stmt may
      get ignored and falsely flag a missing mandatory node error

  * yangdump
    * fix bug where xpath is checked for an external augment
      even if context node is NULL because of some error in the
      external module, so target node not available
    * removed the list-in-unique-path error check
    * add auto-generated code for YANG features
      Conditional code allows features to be enabled
      at compile-time, boot-time, and/or module-load time
      Usage:
       1) Compile-time
         The H file will contain a #define for <mod>_F_<feature>
         The default is to enable features at compile-time.
         To disable, comment out this #define.  All code related
         to the feature will be #ifdef removed from the image.
       2) Boot-time
         If --feature-enable-default=true (d), then --feature-disable
         parameters should be added to turn features off.
         If --feature-enable-default=false, then --feature-enable
         parameters should be added to turn features on.
       3) Module Load time
         During the module SIL init callback, the module features
         will be enabled or disabled according to the #define
         constancts in step 1.  However these settings will
         not override any CLI/conf settings in step 2 (at this time)
    * fixed bug where --feature-enable-default=false would
      cause the server to shutdown if any modules with features
      were loaded
    * now allowing just feature name in --feature-enable and
      --feature-disable parameters instead of only module-name:feature-name
    * --format=uc or --format=uh now cause the notification send functions
      to be generated in the user SIL files, not the yuma SIL files.
      All code which may be edited by the user is now in the user SIL files
      if make_sil_dir --split is used
    * deprecated --feature-code-default parameter.  This is ignored
      by yangdump. Same init sequence is always generated.
    * deprecated --feature-static and feature-dynamic parameters.
      These ares ignored by yangdump.  See Usage section above for new
      YANG feature management procedure.

  * YANG modules
    * update latest NETMOD WG modules
    * add 2 new test modules used to test recent code additions

  * Documentation
    * update developer manual
    * update utility scripts and man pages
* Fri Jan 27 2012 Andy Bierman <andy at netconfcentral.org> 2.2-1 [1712]
  * netconfd
    * Added server regression testing and Coverity static code cleanup
      by Marc Pashley, James Parkin, and Joe Handford
    * fix bug where RPC SIL validate or invoke callback returns an error
      but does not call agt_record_error; server returns <ok>
      and ignores the error return status; now adding an
      <rpc-error> if none, when RPC SIL validate or invoke callback returns
      an error.
    * fixed bug in load module where a module with errors could
      sometimes be loaded anyway.  Now server will exit if
      initial modules loaded have errors, even if YANG parse
      returns NO_ERR for a module with a non-zero error count
    * fixed bug where unknown namespace error caused server to incorrectly
      skip the entire rest of the XML message.  During load_running_config
      it is possible the server is configured to remove bad nodes
      and continue to the next XML sibling node.
    * implemented recoverable edits in agt_val.c;
      * add transactions to cfg.c; now saving an auto-incrementing
        transaction ID across reboots so new ID always used any time
        a config edit request is processed;
      * val_merge is now always non-destructive to the source value
      * newval and curval are always rooted in a source XML tree
      * add VAL_FL_DELETED to mark curval as deleted and not remove
        until commit finalized
      * update undo record handling so it is always used and supports
        recoverable edits
      * refactor edit code and move some ncx code to new module
        agt/agt_cfg.c
      * agt_val_root_check rewrite:
        Commit tests (see RFC 6020, Sec. 8.3.3) are separated out
        from agt_val_instance_check), instead of searching the
        target config for nodes that need commit tests.
        Started undo_rec based test pruning.
      * update commit procedure to use VAL_FL_SUBTREE_DIRTY flag
        to prune unchanged subtrees in the candidate config
        instead of expensive subtree-compare.
      * now cleaning all edit records from candidate so commit
        will not get fooled by delete x, then create x
      * remove agt_val_split_root_check code
        * callback states AGT_CB_COMMIT_CHECK and AGT_CB_TEST_APPLY
          have been removed and the agt_val code simplified
        * val_clone removed; changed applied to real data tree and
          undone if needed; no special test phase, just recoverable apply phase
      * changed user SID to 0 (for superuser) when a commit is rolled
        back; the old user id should not be used; must force all edits
        to be reverted.
      * now only restoring backup from disk if rollback failed,
        not if commit failed
      * add reverse_edit to send SIL callbacks for a reverse edit
        during a rollback; needed when the SIL already returned
        NO_ERR for a COMMIT callback
      * optimized 'applyhere' compares to test just child nodes
        and not all descendent nodes to speed up agt_val processing
      * optimize unique-stmt checking to minimize data retrieval
        and test duplication
      * add code to prune commit tests for objects do not need new
        tests because they have not changed value;
      * optimized instance_check so if-feature and when-stmts
        do not need to be evaluated again (done pre-root-check)
    * fixed bug in delete_config_validate where error path and
      error info parms are reversed; set errval for <url> if needed
    * fix object ID for XPath so choices and cases are removed
      from the path extression; also add module prefix to prevent
      external augment with same local-name from matching expression
    * fix bug where deleting a default leaf did not re-mark the leaf
      as set-by-default
    * fix bug in commit code where newval was not checked for NULL
      before accessing a field in it
    * change output buffer logging from debug4 to debug3
    * updated agt_acm debug logging
    * remove all #ifdefs around log_debug code
    * added agt_log_acm_reads and agt_log_acm_writes
      to the agt_profile to control log output for NACM access
    * fixed bug in error-path generation where /nc:config node
      was incorrectly added as the starting node, instead of the
      top-level YANG object from the database
    * fixed bug where error-path is not getting set if the
      error node is the <url> parameter
    * fixed bug where error-path = '/' was not generated correctly
      so that field would be missing for <validate> and other rpc-error
      responses
    * fix error-path generation so it conforms to RFC 6241
    * fix memory leak in generating unique-error
    * updated error message for list within the path of a
      unique statement component; clarified with YANG author that
      lists not allowed since nodes from different lists cannot
      be in the same unique test tuple
    * added a <bad-value> element to the <error-info> for a
      missing value instance error (310), containing the name of the
      missing node.
    * fix bug where no namespace ID is set for an <rpc-error>
      where the 'select' attribute in the <filter> parameter
      is invalid; set to NETCONF instead of 0
    * fixed bug in XML generation where XML-safe string was not
      generated in string node content
    * fixed bug in copy-config where copy from inline to
      candidate was not getting fully validated or applied correctly
    * fix bug in val_set_canonical_order where list sometimes not
      inserted in sorted order
    * fixed bug in load_config where invoke could be called even
      if validate phase failed
    * add ncx:user-write extension
      see extension 'user-write' in yuma-ncx.yang for details
      Server will block user access to specific edit operations
      if this extension is present in a YANG database node definition
    * add /system/sysNetconfServerCLI monitoring data to
      inspect the CLI parameters used at boot-time
    * add boolean flags to agt_profile to track load-config
      error progress so startup-error and running-error parameters
      can be processed correctly:
       - agt_load_validate_errors    (OK if --startup-error=continue)
       - agt_load_rootcheck_errors   (OK if --running-error=continue)
       - agt_load_apply_errors       (fatal error if SIL apply/commit fails)
    * fixed bug 3476123; leafrefs not getting written to XML correctly
    * fixed bug where inherited when-stmt and if-feature
      statements (from choice or case nodes) were not
      checked when deleting dead nodes
    * fixed bug in check_editop where create on duplicate leaf-list was not
      properly rejected with a data-exists error
    * added support to make sure modules with top-level mandatory nodes
      are rejected by the server if the --running-error parameter is
      set to 'stop'.  This prevents a user from loading such a module
      and causing the server to shutdown.
    * added agt_validate_all (d:T) to agt_profile to control
      <validate> op behavior.  Set to false to have <validate> only
      call SILs for the nodes that are changed in the candidate,
      which is how <commit> validate works.
    * fix bug in NACM where read or write access was wrongly denied
      when read-default=deny and write-default=deny
    * fixed bug where the server would terminate the <load-config> op
      if parse or rpc-instance-check errors occurred, even though
      --startup-error=continue and the nodes with errors were optional
      so they could be removed without making the running config invalid

  * yangcli:
    * fixed bug in filling database content for a OBJ_TYP_CASE
      when the 1 and only case member was a complex type
    * fix bug deleting containers or lists where mandatory child nodes
      were incorrectly filled in, instead of skipped
    * enhance CLI parsing so container can be something other
      than a choice of empty leafs. e.g:
        validate source=@myconfig.xml
        myconfig.xml:
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
           ...
        </config>
      This does not work if a 'source' parameter is given by
      selecting a case number when filling in a choice.
    * fix bug where user is prompted for a case number even if
       there is only 1 enabled case in the choice
    * fix bug where user is prompted if flag should be set y/n
      when editing a leaf of type 'empty'; leaf value already
      implicitly entered by selecting this leaf as the edit target
    * fix bug in val_set_canonical_order where list sometimes not
      inserted in sorted order
    * fixed bug 3476123; leafrefs not getting written to XML correctly
    * added XPath tab completion provided by Zesi Cai (thanks!)
      When a '/' is entered instead of the start of a command,
      the tab key will show all top-level objects available.
      After each '/', the tab shows the next level of child nodes.
      Does not support index (predicate) insertion.

  * yangdump:
    * fix segfault bug where stale backptr was accessed that
      contained heap garbage
    * fixed memory leak where submodule with errors was not freed
      correctly after it was processed
    * added '--full' parameter to yangdump --identifiers to show
      identifiers with module name of each node expanded

  * YANG Parse:
    * fixed bug where conditional descendant nodes specified in
      a unique-stmt are treated as an error.  This is only an error
      is a key-stmt test fails; For unique-stmt, missing nodes
      in a unique test tuple cause the test to be skipped
    * fix bug where nested leafref types within unions were not always getting
      checked in final resolve steps
    * fix off-by-1 bug in object-id generation when module names
      are added
    * Remove memory leak from consume_revision
    * fix bug where default value for union data type sometimes
      incorrectly flagged as invalid value; can cause segfault
    * fix bug where checking if a parameter is set to its default for
      an identityref, bits, or leafref always returned FALSE
    * fixed bug where XPath context node for when-stmt
      in an augment-stmt was not set correctly
    * fixed bug where errors in consume_body_stmts were not
      always rippled all the way back to ncxmod.c, causing
      mod->res == NO_ERR but mod->errors > 0

  * Build
    * Fixed makefile.sil so that yuma symbols are always
      checked first before standard library module names
      Also removed extra libraries libagt and libncx from
      the SIL link command.  This is not needed and will
      cause an error if these libraries are not found.
   * Fixed bug in several Makefiles where libm is not explicitly
      declared in the link command.  This causes STATIC=1 builds
      to fail on Ubuntu 11.10 (symbol 'round' not found from libm)
   * Cleaned up static build of yangcli

* Tue Sep 27 2011 Andy Bierman <andy at netconfcentral.org> 2.1-2 [1457]
  * Build
    * fix bug added recently that breaks build in libtoaster
      in a plain build (YUMA_HOME not set) and breaks CYGWIN
      build as well
* Sun Sep 25 2011 Andy Bierman <andy at netconfcentral.org> 2.1-1 [1424]
  * netconfd
    * add --runpath to netconfd.yang
    * fix bug reported by Sara Dickinson where leafref was
      not getting validated during commit; turned out leafrefs and
      instance-identifiers were not getting validated for 
      target=running or during commit
    * fix bug where <validate> parameters were not handled correctly
      and <ok> was returned without validating the target config.
    * add --factory-startup CLI parameter.
      Currently there is no way to rewrite the invisible
      startup-cfg.xml if --with-startup=false, except
      by modifying the factory settings and saving the config.
      This parameter forces the startup config and the running
      config to contain the factory default settings during
      initialization.
    * fixed bug (reported by Sara Dickinson) where must-stmt tests
      for sibling nodes were getting skipped as soon as 1 must-test
      failed.  This could result in nodes that should be invalid
      left in the running config during load_running_config
      if --startup-error=continue (the default)
    * fix bug in agt_proc.c where CPU cores were not causing
      a new val entry to be created.  Introduced with vi-cov commit
    * add yuma-arp module, implemented by Igor Smolyar
    * fixed bug 3404233
      The client and server both incorrectly accepted
      an XML node for a YANG choice or case node.
      These nodes do not exist in a YANG data tree, just
      in the YANG object tree
    * fix bug in COMMIT phase where SIL callback functions
      for nested nodes were not getting invoked for create
      and merge edit operations.
    * fixed bug introduced in last release where SIL validation
      callbacks are being called multiple times
    * fixed bug where commit callback for editop=OP_EDITOP_DELETE
      the curnode is a detached node -- the parent node is NULL.
    * fixed bug 3395740
    * source tree specified by YUMA_HOME environment variable
      no longer required to be present
    * added libagt.so to shared library install location (d: /usr/lib)
    * using shared libraries in default location for libagt and libncx
      for ubuntu and RPM packaging.  Not static libaries anymore!
    * building and installing libncx.a and libagt.a if STATIC=1 
      present in make cmd
    * updated SIL makefile so YUMA_HOME is not used unless
      FORCE_YUMA_HOME=1 is present in the make cmd;
      /usr/lib/yuma is used by default
    * make /arp node present by default, using refactored code from agt_acm.c

  * yangcli
    * add JSON output support for --display-mode=json
      and saving data with @foo.json
    * fix bug where manager session control block not checked for NULL
    * add external parameter support for RPC commands

      yangcli> some-command @filespec.xml

      filespec.xml (in YUMA_DATAPATH) == RPC input element
      <input>
        <a>10</a>
        <b>fred</b>
      </input>
    * fixed bug where an edit command (e.g., create) on
      a choice or case node would generate an XML node
      for the choice or case.  Now being removed from
      the XML payload before an <edit-config> is sent

  * yangdump:
    * added support for split SIL filesor combined (old way):
      * --format=yc : Yuma SIL C file
      * --format=yh : Yuma SIL H file
      * --format=uc : User SIL C file
      * --format=uc : User SIL H file
      * --format=c  : Combined Yuma/User SIL C file
      * --format=h  : Combined Yuma/User SIL H file
   * added support for code generation for automatic retrieval
     of ancestor-or-self key values in user SIL callbacks
    * Remove #ifdef around #include directives for generated files.
    * fixed bug 3404234
      --format=c output (SIL code) was not handling nested
        config=false containers (lists and leaf-lists still
        not handled!).  Now nested config=false containers
        will automatically be created
    * fixed bug for --format=c where edit callbacks were being
      generated for OBJ_TYP_CHOICE and OBJ_TYP_CASE nodes.
      Since these nodes never exist in a database, these callbacks
      get registered but never invoked
    * fixed bug where SIL code generated for boolean, union, and identityref
      datatypes is incorrect -- the data type will be whatever the union
      was parsed will be treated as a string; causes segfault;
      !!! not fixed in v1
      * union now passed to User SIL function as val_value_t
        instead of string
      * affected edit callback functions and notification send functions
   * added __cplusplus 'extern C' wrappers to H file generation
     for --format=h|uh|yh
  * Build:
   * added --split parameter to make_sil_dir
     * make_sil_dir --split foo  : makes files in foo/src/
        * y_foo.c : Yuma SIL C file
        * y_foo.h : Yuma SIL H file
        * u_foo.c : User SIL C file
        * u_foo.h : User SIL H file
    * building and installing libagt as a dynamic library
    * building Ubuntu package will mostly dynamic libraries
      instead of STATIC=1 and FULL_STATIC=1
    * bumped version to 2.1
    * updated Makefiles to allow debian debuild of 3 packages 
      when DEBIAN=1 set:
        no flag: build yuma package
        DEVELOPER=1: build yuma-dev package
        DOC=1: build  yuma-doc package
    * add HTML versions of manuals to install process
    * move PDFs from /usr/share/doc/yuma to /usr/share/doc/yuma/pdf
    * updated user manuals

  * YANG parse: 
    * fix error message for leafref-stmt
    * fix bug 3404231
      * incorrect handling of object type when checking
        leaf/leaf-list leafref loops, which could cause
        the wrong struct in a union to be used
    * fixed bug 3404239
      All YANG data-def constructs were being checked for
      config, default, mandatory, min/max-elements
      before refine-stmts were applied.
      Moved all relevant tests from 'resolve' phase to 
      'resolve_final' phase.
    * Added modules/test/fail/t13.yang test case for compiler
      to check mandatory+default combo after refine applied.
    * fixed bug: anyxml objects were not getting checked during
      resolve_final phase (mandatory-stmt warnings)
    * suppress error messages when invalid XPath detected during
      validation of a union datatype.  Unions are only required
      to be valid for 1 of N union types, not any particular type.

* Sun Aug 21 2011 Andy Bierman <andy at netconfcentral.org> 2.0-2 [1325]
 * yangcli
  * fixed bug where --batchmode is ignored if --run-command
    is also used
  * added support to connect to tailf confd servers over TCP;
    added --transport=ssh|tcp parameter to connect command
    and CLI parameter for startup connecting via TCP
  * Fix potential double calls to free and memory leaks resulting from
    calls to set_str(). In some paths the function set_str()
  * fixed bugs in autoload procedure

 * netconfd
  * fixed 2 framing bugs in base:1.1 mode
  * rewrote buffer code to pack incoming message buffers instead
    of using client buffer size as-is
  * fixed memory leak in new support code for malformed-message
    only occured when malformed-message error generated
  * Improve logging for debug purposes from netconf-subsys.c
    (by Mark Pashley)
  * Many bugfixes and dead code removal detected by Coverity
    static analysis (from vi-cov branch by Mark Pashley)
  * Removed potential memory leak in cache_data_rules in NACM
  * Summary of bugfixes to copy_config_validate():
    Coverity reported the following issues:
      DEAD CODE
      Code with no effect.
      Use after free
      Null pointer derference
      Resource Leaks
  * sprintf changed to snprintf and strcpy changed to strncpy
    in some cases, to make sure no buffer overrun can occur
  * add module yuma-time-filter.yang
  * add last-modified XML attribute to <rpc-reply> for <get>
    and <get-config> replies
  * add if-modified-since parameter to <get> and <get-config>
    protocol operations
  * make logging from netconf-subsystem configurable via command line options
  * updated netconfd user manual

 * yangdump
  * fix bug in format=html or format=yang where pattern may
    not get generated in the output
  * add support for path links in leafrefs in --format=html

 * YANG parse:
  * fixed bug where val_clone of enum sometimes had static enu.name
    pointing at old.enu.dname so if old was freed, new.enu.name
    would point at garbage in the heap
  * fixed some memory leaks in error corner-cases
  * fixed bug where valid patterns parsed as non-strings
    were not correctly processed and no compiled pattern
    was created
  * fixed bug where unquoted prefixed string (foo:bar) would
    not be saved correctly in the compiled pattern (bar)

 * XML parse:
  * add tracefile support to debug input fed to XML textReader

 * CLI:
  * Change the signature of all instances of main to meet the 'c'
    standard.

* Thu Jul 21 2011 Andy Bierman <andy at netconfcentral.org> 2.0-1 [1253]
  * initial 2.0 release
    * contains all yuma 1.15 features, plus major features
	* NETCONF base:1.1 support (RFC 6241 and RFC 6242)
	* with-defaults 'report-all-tagged' mode (RFC 6243)
	* --urltarget path selection mechanism (UrlPath)


%package devel
BuildArch: noarch
Summary:  YANG-based Unified Modular Automation Tools (Developer)

%description devel
Yuma Tools is a YANG-based NETCONF-over-SSH client and server
development toolkit.  This package contains H files, scripts,
and other files needed to create SIL code for use with
the netconfd server.

%post devel
echo "Yuma developer files installed."

%files devel
%defattr(-,root,root,-)
%{_bindir}/make_sil_dir
%{_mandir}/man1/make_sil_dir.1.gz
%{_includedir}/yuma/
%{_datadir}/yuma/util/
%{_datadir}/yuma/src/libtoaster/


%package doc
BuildArch: noarch
Summary:  YANG-based Unified Modular Automation Tools (Documentation)

%description doc
Yuma Tools is a YANG-based NETCONF-over-SSH client and server
development toolkit.  This package contains the Yuma user manuals
in PDF and HTML format.

%post doc
echo "Yuma documentation files installed."

%files doc
%defattr(-,root,root,-)
/usr/share/doc/yuma/server-call-chain.txt
/usr/share/doc/yuma/pdf/
/usr/share/doc/yuma/html/

