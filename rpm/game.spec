%define firejail_section X-Application
# %if ! "0%{?_app_orgname}"
%if ! %{defined _app_orgname}
%define _app_orgname ru.sashikknox
%define _app_appname love2d
%endif
%if "0%{?_oldaurora}"
%define xauroraapp "\#[X-Aurora-Application]\#IconMode=Crop"
%else
%define xauroraapp ""
%endif

Name:       %{_app_orgname}.%{_app_appname}
Summary:    Love2D Game Engine
Release:    1
Version:    11.3.0
Group:      Amusements/Games
License:    zlib
Source0:    %{name}.tar.gz

%define __requires_exclude ^libvorbis.*\\.so.*|libopenal\\.so.*|libmpg123\\.so.*|libfreetype\\.so.*|libharfbuzz\\.so.*|libmodplug\\.so.*|libtheora\\.so.*|libtheoradec\\.so.*|libgraphite2\\.so.*|libliblove\\.so.*$
%define __provides_exclude_from ^%{_datadir}/%{name}/lib/.*\\.so.*$

BuildRequires: pkgconfig(sdl2)
BuildRequires: pkgconfig(openal)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(theoradec)
BuildRequires: pkgconfig(vorbis)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(libmpg123)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: rsync
BuildRequires: patchelf

%description
"LÖVE is an *awesome* framework you can use to make 2D games in Lua. 
It's free, open-source, and works on Windows, macOS, Linux, Android, iOS 
and AuroraOS."

%prep
%setup -q -n %{name}-%{version}

cmake -Bbuild_libmodplug_%{_arch} \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    libmodplug

# clean previous build data in LuaJIT
pushd LuaJIT
make clean 
popd


%build
pushd build_libmodplug_%{_arch}
make -j`nproc`
make DESTDIR=`pwd` install
popd 

pushd LuaJIT
make -j`nproc`
popd

cmake \
    -Bbuild_love_%{_arch} \
    -DAURORAOS=YES \
    -DCMAKE_BUILD_TYPE=Debug \
    -DMODPLUG_INCLUDE_DIR=build_libmodplug_%{_arch}/usr/local/include \
    -DMODPLUG_LIBRARY=build_libmodplug_%{_arch}/libmodplug.so.1.0.0 \
    -DLUAJIT_INCLUDE_DIR=LuaJIT/src/ \
    -DLUAJIT_LIBRARY=LuaJIT/src/libluajit.a \
    -DLOVE_EXE_NAME=%{name} \
    -DLOVE_LIB_NAME="love-11.0" \
    love
pushd build_love_%{_arch}
make -j`nproc`
popd


%install
install -D %{_libdir}/libgraphite2.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libtheora.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libharfbuzz.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libtheoradec.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libvorbisfile.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libopenal.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libfreetype.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libmpg123.so* -t %{buildroot}%{_datadir}/%{name}/lib

install -D -s build_libmodplug_%{_arch}/libmodplug.so.1* -t %{buildroot}%{_datadir}/%{name}/lib
patchelf --force-rpath --set-rpath %{_datadir}/%{name}/lib build_love_%{_arch}/libliblove.so
install -D -s build_love_%{_arch}/libliblove.so -t %{buildroot}%{_datadir}/%{name}/lib
patchelf --force-rpath --set-rpath %{_datadir}/%{name}/lib build_love_%{_arch}/love
install -D -s build_love_%{_arch}/love  %{buildroot}%{_bindir}/%{name}
install -m 655 -D icons/86.png  %{buildroot}%{_datadir}/icons/hicolor/86x86/apps/%{name}.png
install -m 655 -D icons/108.png %{buildroot}%{_datadir}/icons/hicolor/108x108/apps/%{name}.png
install -m 655 -D icons/128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -m 655 -D icons/172.png %{buildroot}%{_datadir}/icons/hicolor/172x172/apps/%{name}.png

sed "s/__ORGNAME__/%{_app_orgname}/g" love.desktop.in>%{name}.desktop
sed -i "s/__APPNAME__/%{_app_appname}/g" %{name}.desktop
sed -i "s/__X_APPLICATION__/%{firejail_section}/g" %{name}.desktop
sed -i "s/__X_AURORA_APP__/%{xauroraapp}/g" %{name}.desktop
sed -i "s/#/\n/g" %{name}.desktop

install -m 655 -D %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/icons/hicolor/86x86/apps/%{name}.png
%{_datadir}/icons/hicolor/108x108/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/172x172/apps/%{name}.png
%{_datadir}/%{name}/lib/*
%{_datadir}/applications/%{name}.desktop
