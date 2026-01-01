%define _app_orgname ru.sashikknox
%define _app_appname AwesomeGame
%define _app_launcher_name Офигенная игра

Name:       %{_app_orgname}.%{_app_appname}
Summary:    Love2D Game Example for AuroraOS
Release:    1
Version:    1.0.0
Group:      Amusements/Games
License:    BSD3
Source0:    %{name}.tar.gz

%define __requires_exclude ^libvorbis.*\\.so.*|libopenal\\.so.*|libmpg123\\.so.*|libfreetype\\.so.*|libharfbuzz\\.so.*|libmodplug\\.so.*|libtheora\\.so.*|libtheoradec\\.so.*|libgraphite2\\.so.*|libliblove\\.so.*$
%define __provides_exclude_from ^%{_datadir}/%{name}/lib/.*\\.so.*$

BuildRequires: pkgconfig(openal)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(theoradec)
BuildRequires: pkgconfig(vorbis)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(libmpg123)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(glesv1_cm)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(sdl2)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(udev)
BuildRequires: rsync
BuildRequires: patchelf
BuildRequires: zip
BuildRequires: ninja
BuildRequires: lua

%description
"Game example for AuroraOS made with LÖVE engine"

%prep
%setup -q -n %{name}-%{version}

cmake \
    -G Ninja \
    -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja \
    -Bbuild/%{_arch}/libsdl \
    -DCMAKE_BUILD_TYPE=Release \
    -DSDL_PULSEAUDIO=OFF \
    -DSDL_RPATH=OFF \
    -DSDL_AUDIO=OFF \
    -DSDL_STATIC=OFF \
    -DSDL_WAYLAND=ON \
    -DSDL_X11=OFF \
    -DSDL_WAYLAND_LIBDECOR=OFF \
    libsdl

cmake -Bbuild/%{_arch}/libmodplug \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    libmodplug

# clone to build dir
rsync -aP LuaJIT/* build/%{_arch}/LuaJIT/


%build
cmake --build build/%{_arch}/libsdl -j`nproc`
pushd build/%{_arch}/libmodplug
make -j`nproc`
make DESTDIR=`pwd` install
popd 

pushd build/%{_arch}/LuaJIT
make CFLAGS="-fPIC"  -j`nproc`
popd
# update scripts
pushd love/src/scripts
lua auto.lua boot nogame
popd

cmake \
    -G Ninja \
    -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja \
    -Bbuild/%{_arch}/love \
    -DAURORAOS=YES \
    -DAURORAOS_APPDATA="%{_app_orgname}/%{_app_appname}" \
    -DCMAKE_BUILD_TYPE=Debug \
    -DMODPLUG_INCLUDE_DIR=build/%{_arch}/libmodplug/usr/local/include \
    -DMODPLUG_LIBRARY=build/%{_arch}/libmodplug/libmodplug.so.1.0.0 \
    -DLUAJIT_INCLUDE_DIR=build/%{_arch}/LuaJIT/src/ \
    -DLUAJIT_LIBRARY=build/%{_arch}/LuaJIT/src/libluajit.a \
    -DLOVE_EXE_NAME=%{name} \
    -DLOVE_LIB_NAME="love-11.0" \
    love
cmake --build build/%{_arch}/love -j`nproc`


%install
install -D %{_libdir}/libgraphite2.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libtheora.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libharfbuzz.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libtheoradec.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libvorbisfile.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libopenal.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libfreetype.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D %{_libdir}/libmpg123.so* -t %{buildroot}%{_datadir}/%{name}/lib

install -D -s build/%{_arch}/libsdl/libSDL2-2.0.so* -t %{buildroot}%{_datadir}/%{name}/lib
install -D -s build/%{_arch}/libmodplug/libmodplug.so.1* -t %{buildroot}%{_datadir}/%{name}/lib
patchelf --force-rpath --set-rpath %{_datadir}/%{name}/lib build/%{_arch}/love/libliblove.so
install -D -s build/%{_arch}/love/libliblove.so -t %{buildroot}%{_datadir}/%{name}/lib
patchelf --force-rpath --set-rpath %{_datadir}/%{name}/lib build/%{_arch}/love/love
install -D -s build/%{_arch}/love/love  %{buildroot}%{_bindir}/%{name}
install -m 655 -D icons/86.png  %{buildroot}%{_datadir}/icons/hicolor/86x86/apps/%{name}.png
install -m 655 -D icons/108.png %{buildroot}%{_datadir}/icons/hicolor/108x108/apps/%{name}.png
install -m 655 -D icons/128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -m 655 -D icons/172.png %{buildroot}%{_datadir}/icons/hicolor/172x172/apps/%{name}.png

sed "s/__ORGNAME__/%{_app_orgname}/g" love.desktop.in>%{name}.desktop
sed -i "s/__APPNAME__/%{_app_appname}/g" %{name}.desktop
sed -i "s/__X_APPLICATION__/%{firejail_section}/g" %{name}.desktop
sed -i "s/__LAUNCHER_NAME__/%{_app_launcher_name}/g" %{name}.desktop

install -m 655 -D %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

pushd game
zip -FS -r -y %{buildroot}%{_datadir}/%{name}/game.love *
popd

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/icons/hicolor/86x86/apps/%{name}.png
%{_datadir}/icons/hicolor/108x108/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/172x172/apps/%{name}.png
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
