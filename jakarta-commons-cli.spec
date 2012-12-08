# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0

%define base_name       cli
%define short_name      commons-%{base_name}
%define section         devel

Name:           jakarta-commons-cli
Version:        1.1
Release:        %mkrel 0.0.7
Epoch:          0
Summary:        Jakarta Commons CLI, a Command Line Interface for Java
License:        Apache License
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://jakarta.apache.org/commons/cli/
Source:         http://archive.apache.org/dist/jakarta/commons/cli/source/%{short_name}-%{version}-src.tar.gz

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-commons-logging
BuildRequires:  java-rpmbuild >= 0:1.6

# (anssi) There is no reason to depend on these, as programs may use
# jakarta-commons-cli even without them, such as azureus. Installing them
# brings no benefit unless they are explicitely placed in classpath, in which
# case the end-user application should require them directly anyway. This is
# also how Debian does it.
#Requires:       jakarta-commons-lang
#Requires:       jakarta-commons-logging

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
The CLI library provides a simple and easy to use API for working with
the command line arguments and options.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
BuildRequires:  java-javadoc

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n %{short_name}-%{version}-src
%remove_java_binaries


%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath commons-logging commons-lang)
export CLASSPATH="$CLASSPATH:target/classes:target/test-classes"
 # for tests
mkdir lib
%{ant} \
  -Dbuild.sysclasspath=only \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  jar dist


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{short_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT


%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt README.txt
%{_javadir}/*
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-0.0.5mdv2011.0
+ Revision: 665796
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-0.0.4mdv2011.0
+ Revision: 606047
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-0.0.3mdv2010.1
+ Revision: 522939
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.1-0.0.2mdv2010.0
+ Revision: 425395
- rebuild

* Mon Jul 14 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.1-0.0.1mdv2009.0
+ Revision: 234462
- new version 1.1

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.0-8.0.4mdv2009.0
+ Revision: 167933
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-8.0.4mdv2008.1
+ Revision: 120902
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Sep 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-8.0.3mdv2008.0
+ Revision: 87927
- remove run-time dependencies on jakarta-commons-lang and
  jakarta-commons-logging, they should be pulled in by the application that
  uses commons-cli if they are really needed

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-8.0.2mdv2008.0
+ Revision: 87399
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Fri Aug 03 2007 David Walluck <walluck@mandriva.org> 0:1.0-8.0.1mdv2008.0
+ Revision: 58742
- sync with latest jpackage release
- Import jakarta-commons-cli




* Sat Jun 22 2006 David Walluck <walluck@mandriva.org> 0:1.0-7.1mdv2006.0
- bump release

* Thu Jun 01 2006 David Walluck <walluck@mandriva.org> 0:1.0-6.2mdv2006.0
- rebuild for libgcj.so.7
- aot-compile

* Fri May 27 2005 David Walluck <walluck@mandriva.org> 0:1.0-6.1mdk
- release

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.0-6jpp
- Rebuild with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-5jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.0-4jpp
- Upgrade to Ant 1.6.X

* Sun Oct 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-3jpp
- Non-versioned javadoc dir symlink.
- Crosslink with local J2SE javadocs.

* Fri Apr  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-2jpp
- Rebuild for JPackage 1.5.

* Tue Dec 10 2002 Ville Skyttä <ville.skytta at iki.fi> - 1.0-1jpp
- 1.0, first JPackage release.
