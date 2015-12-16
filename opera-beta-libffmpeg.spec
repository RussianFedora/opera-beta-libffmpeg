%global build_for_x86_64 1
%global build_for_i386 1
%define debug_package %{nil}

%define chromium_system_libs 0

%define chromium_ver 48.0.2564.41
%define opera_chan opera-beta

#%if 0%{?fedora} >= 21
#%define clang 1
#%else
%define clang 0
#%endif

Summary:	Additional FFmpeg library for Opera Web browser providing H264 and MP4 support
Name:		%{opera_chan}-libffmpeg
Version:	35.0.2066.10
Release:	3%{?dist}
Epoch:		5

Group:		Applications/Internet
License:	BSD, LGPL
URL:		https://gist.github.com/lukaszzek/ec04d5c953226c062dac

Source0:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{chromium_ver}.tar.xz
Source1:	depot_tools.tar.xz
Source2:	gn-binaries.tar.xz
Source3:	check_chromium_version.sh

%ifarch x86_64
Provides:   libffmpeg.so()(64bit)
%else
Provides:   libffmpeg.so
%endif

%if 0%{?build_for_x86_64}
%if !0%{?build_for_i386}
ExclusiveArch:    x86_64
%else
ExclusiveArch:    x86_64 i686
%endif
%else
%if 0%{?build_for_i386}
ExclusiveArch:    i686
%endif
%endif

BuildRequires:  SDL-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  dirac-devel >= 1.0.0
BuildRequires:  elfutils-libelf-devel
BuildRequires:  elfutils-devel
BuildRequires:  expat-devel
BuildRequires:  fdupes
BuildRequires:  flac-devel
BuildRequires:  flex
BuildRequires:  freetype-devel
BuildRequires:  gperf
BuildRequires:  gsm
BuildRequires:  gsm-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gyp
BuildRequires:  hicolor-icon-theme
BuildRequires:  hunspell-devel
BuildRequires:  imlib2-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libdc1394
BuildRequires:  libdc1394-devel
BuildRequires:  libdrm-devel
BuildRequires:  libdrm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  libogg-devel
BuildRequires:  liboil-devel >= 0.3.15
BuildRequires:  libtheora-devel >= 1.1
BuildRequires:  libusbx-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libvpx-devel
BuildRequires:  ncurses-devel
BuildRequires:  ninja-build
BuildRequires:  pam-devel
BuildRequires:  pciutils-devel
BuildRequires:  perl(Switch)
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(cairo) >= 1.6
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(nspr) >= 4.9.5
BuildRequires:  pkgconfig(nss) >= 3.14
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  schroedinger-devel
BuildRequires:  slang-devel
BuildRequires:  speech-dispatcher-devel
BuildRequires:  sqlite-devel
BuildRequires:  texinfo
BuildRequires:  util-linux
BuildRequires:  valgrind-devel

%if 0%{?chromium_system_libs}
BuildRequires:  libicu-devel >= 4.0
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  perl-JSON
BuildRequires:  usbutils
BuildRequires:  yasm
BuildRequires:  pkgconfig(libevent)
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(speex)
%endif

%if ! %{defined rhel}
%if 0%{?fedora} < 22
BuildRequires:  faac-devel >= 1.28
%endif
BuildRequires:  lame-devel
BuildRequires:  opencore-amr-devel
BuildRequires:  wdiff
BuildRequires:  x264-devel
BuildRequires:  xvidcore-devel
%endif

%if 0%{?clang}
BuildRequires:	clang
%endif

Requires:	%{opera_chan} = 5:%{version}

%description
Due to changes in Chromium, Opera is no longer able to use the system FFmpeg
library for H264 video playback on Linux, so H264-encoded videos fail to play by
default (but HTML5 video encoded using different formats, like webm, work). For
legal reasons, Opera may not be distributed with H264 compatible FFmpeg library
included into package.

It's possible to build the extra version of Chromium modified FFmpeg providing
H264 and MP4 support. Opera-libffmpeg package includes this library.

%prep
%setup -q -c

cd %{_builddir}/%{name}-%{version}/chromium-%{chromium_ver}
xz -d %{SOURCE1}
xz -d %{SOURCE2}

# Workaround for "No such file or directory" build error:
touch ./chrome/test/data/webui/i18n_process_css_test.html

%build
buildconfig+="-Dwerror=
                -Dcomponent=shared_library
                -Dffmpeg_branding=Chrome"

%if 0%{?clang}
buildconfig+=" -Dclang=1
		-Dclang_use_chrome_plugins=0"
%else
buildconfig+=" -Dclang=0"
%endif

%if 0%{?chromium_system_libs}
buildconfig+=" -Duse_system_icu=1
		-Duse_system_flac=1
                -Duse_system_speex=1
                -Duse_system_libexif=1
                -Duse_system_libevent=1
                -Duse_system_libmtp=1
                -Duse_system_opus=1
                -Duse_system_bzip2=1
                -Duse_system_harfbuzz=1
                -Duse_system_libjpeg=1
                -Duse_system_libpng=1
                -Duse_system_libxslt=1
                -Duse_system_libxml=1
                -Duse_system_libyuv=1
                -Duse_system_nspr=1
                -Duse_system_protobuf=1
                -Duse_system_yasm=1"
%else
buildconfig+=" -Duse_system_icu=0
		-Duse_system_flac=0
                -Duse_system_speex=0
                -Duse_system_libexif=0
                -Duse_system_libevent=0
                -Duse_system_libmtp=0
                -Duse_system_opus=0
                -Duse_system_bzip2=0
                -Duse_system_harfbuzz=0
                -Duse_system_libjpeg=0
                -Duse_system_libpng=0
                -Duse_system_libxslt=0
                -Duse_system_libxml=0
                -Duse_system_libyuv=0
                -Duse_system_nspr=0
                -Duse_system_protobuf=0
                -Duse_system_yasm=0"
%endif

%ifarch x86_64
buildconfig+=" -Dsystem_libdir=lib64
		-Dtarget_arch=x64"
%endif

buildconfig+=" -Duse_pulseaudio=1
                -Dlinux_link_libpci=1
                -Dlinux_link_gnome_keyring=1
                -Dlinux_link_gsettings=1
                -Dlinux_link_libgps=1
		-Dlinux_link_libspeechd=1
                -Djavascript_engine=v8
                -Dlinux_use_gold_binary=0
                -Dlinux_use_gold_flags=0
                -Dgoogle_api_key=AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q
                -Dgoogle_default_client_id=4139804441.apps.googleusercontent.com
                -Dgoogle_default_client_secret=KDTRKEZk2jwT_7CDpcmMA--P"

%if 0%{?fedora} >= 20
buildconfig+=" -Dlibspeechd_h_prefix=speech-dispatcher/"
%endif

%if 0%{?clang}
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
# Modern Clang produces a *lot* of warnings 
export CXXFLAGS="${CXXFLAGS} -Wno-unknown-warning-option -Wno-unused-local-typedef -Wunknown-attributes -Wno-tautological-undefined-compare"
export GYP_DEFINES="clang=1"
%endif

cd %{_builddir}/%{name}-%{version}/chromium-%{chromium_ver}
./build/linux/unbundle/replace_gyp_files.py $buildconfig

export GYP_GENERATORS='ninja'
./build/gyp_chromium build/all.gyp --depth=. $buildconfig

mkdir -p %{_builddir}/%{name}-%{version}/chromium-%{chromium_ver}/out/Release

ninja-build -C %{_builddir}/%{name}-%{version}/chromium-%{chromium_ver}/out/Release ffmpeg

%install
mkdir -p %{buildroot}%{_libdir}/%{opera_chan}/lib_extra
install -m 644 %{_builddir}/%{name}-%{version}/chromium-%{chromium_ver}/out/Release/lib/libffmpeg.so %{buildroot}%{_libdir}/%{opera_chan}/lib_extra/

%files
%{_libdir}/%{opera_chan}/lib_extra/libffmpeg.so

%changelog
* Wed Dec 16 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.10-3
- use gcc instead clang

* Wed Dec 16 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.10-2
- Remove -Dffmpeg_soname_version=%{opera_major_ver}

* Wed Dec 16 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.10-1
- Update to 35.0.2066.10
- Remove %{opera_major_ver} due to upstream changes

* Thu Dec 03 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:34.0.2036.24-1
- Update to 34.0.2036.24

* Fri Nov 27 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:34.0.2036.16-1
- Update to 34.0.2036.16

* Mon Nov 09 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:34.0.2036.3-1
- Update to 34.0.2036.3

* Mon Oct 26 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:33.0.1990.35-1
- Update to 33.0.1990.35

* Fri Oct 09 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:33.0.1990.20-1
- Update to 33.0.1990.20

* Sat Oct 03 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> 5:33.0.1990.11-2.R
- Add workaround for "No such file or directory" build error (affects Chromium >= 46)

* Sat Oct 03 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> 5:33.0.1990.11-1.R
- Update to 33.0.1990.11

* Tue Sep 08 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> 5:32.0.1948.19-1.R
- Update to 32.0.1948.19

* Tue Sep 01 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> 5:32.0.1948.12-1.R
- Update to 32.0.1948.12

* Sat Aug 22 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru>
- Rework patch

* Fri Aug 21 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> 5:32.0.1948.4-2.R
- Drop empty debuginfo package (affects Fedora >= 24)

* Thu Aug 20 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> 5:32.0.1948.4-1.R
- Rename to opera-beta-libffmpeg according to new channel
- Update to 32.0.1948.4

* Thu Aug 20 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> 5:31.0.1889.174-1.R
- Update to 31.0.1889.174
- Add check_chromium_version.sh

* Wed Aug 12 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> 5:31.0.1889.99-1.R
- Initial build
