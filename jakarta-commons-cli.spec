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

Summary:	Jakarta Commons CLI, a Command Line Interface for Java
Name:		jakarta-commons-cli
Version:	1.1
Release:	1
License:	Apache License
Group:		Development/Java
Url:		https://jakarta.apache.org/commons/cli/
Source0:	http://archive.apache.org/dist/jakarta/commons/cli/source/%{short_name}-%{version}-src.tar.gz
%if !%{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-junit >= 0:1.6
BuildRequires:	junit
BuildRequires:	jakarta-commons-lang
BuildRequires:	jakarta-commons-logging
BuildRequires:	java-rpmbuild >= 0:1.6
# (anssi) There is no reason to depend on these, as programs may use
# jakarta-commons-cli even without them, such as azureus. Installing them
# brings no benefit unless they are explicitely placed in classpath, in which
# case the end-user application should require them directly anyway. This is
# also how Debian does it.
#Requires:	jakarta-commons-lang
#Requires:	jakarta-commons-logging

%description
The CLI library provides a simple and easy to use API for working with
the command line arguments and options.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
BuildRequires:	java-javadoc

%description    javadoc
Javadoc for %{name}.

%prep
%setup -qn %{short_name}-%{version}-src
%remove_java_binaries

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath commons-logging commons-lang)
export CLASSPATH="$CLASSPATH:target/classes:target/test-classes"
 # for tests
mkdir lib
%ant \
	-Dbuild.sysclasspath=only \
	-Dfinal.name=%{short_name} \
	-Dj2se.javadoc=%{_javadocdir}/java \
	jar dist

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p dist/%{short_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{gcj_compile}

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%doc LICENSE.txt README.txt
%{_javadir}/*
%{gcj_files}

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

