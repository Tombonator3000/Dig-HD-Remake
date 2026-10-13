#!/bin/bash
set -euo pipefail
R=$(cd "$(dirname "$0")" && pwd)
export PATH="$R/toolchain/usr/bin:$PATH"
CROSS=x86_64-w64-mingw32
PREFIX="$R/win-deps"
mkdir -p "$PREFIX" "$R/windows-build"
cd "$R/zlib-1.3.2"
make -f win32/Makefile.gcc PREFIX="$CROSS-" -j3 > "$R/zlib-build.log" 2>&1
mkdir -p "$PREFIX/include" "$PREFIX/lib"
cp zlib.h zconf.h "$PREFIX/include/"
cp libz.a "$PREFIX/lib/"
cd "$R/libpng-1.6.55"
CC="$CROSS-gcc" AR="$CROSS-ar" RANLIB="$CROSS-ranlib" CPPFLAGS="-I$PREFIX/include" LDFLAGS="-L$PREFIX/lib" ./configure --host="$CROSS" --prefix="$PREFIX" --disable-shared --enable-static > "$R/png-configure.log" 2>&1
make -j3 > "$R/png-build.log" 2>&1
make install >> "$R/png-build.log" 2>&1
cd "$R/windows-build"
CXX="$CROSS-g++" LDFLAGS='-static-libgcc -static-libstdc++' "$R/source/configure" --host="$CROSS" --disable-all-engines --enable-engine=scumm,scumm-7-8 --disable-engine=he,rebel2-psx --disable-detection-full --disable-debug --enable-optimizations --enable-png --enable-zlib --disable-mt32emu --disable-fluidsynth --disable-cloud --disable-libcurl --disable-sdlnet --disable-tts --disable-eventrecorder --with-sdl-prefix="$R/SDL2-2.32.10/x86_64-w64-mingw32" --with-png-prefix="$PREFIX" --with-zlib-prefix="$PREFIX" > "$R/windows-configure.log" 2>&1
make -j3 > "$R/windows-build.log" 2>&1
"$CROSS-strip" scummvm.exe
file scummvm.exe
"$CROSS-objdump" -p scummvm.exe | sed -n '/DLL Name/p'
