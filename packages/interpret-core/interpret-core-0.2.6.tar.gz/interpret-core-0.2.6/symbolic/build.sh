#!/bin/sh

# This script is written as Bourne shell and is POSIX compliant to have less interoperability issues between distros.

# Periodically check the valgrind results on the build server by going to:
# https://dev.azure.com/ms/interpret/_build?definitionId=293&_a=summary
# By clicking on the build of interest, then "Test ebm_native Linux", then "View raw log"
# We normally have 2 "still reachable" blocks from the Testing executable.
#
# We run the clang-tidy and Visual Studio static analysis tools on the build server.  Warnings do not stop the build, 
# so these need to be inspected to catch static analysis issues.  The results can be viewed in the build logs here:
# https://dev.azure.com/ms/interpret/_build?definitionId=293&_a=summary
# By clicking on the build of interest, then "Build ebm_native Windows", then "View raw log"
#
# Ideally we'd prefer to have static analysis running on all OSes, but we can probably just rely on our
# build system to handle this aspect since adding it in multiple places adds complexity to this build script.
# Also, I ran into issues when I first tried it, which to me suggests these might introduce periodic issues:
#   - on Mac, clang-tidy doesn't seem to come by default in the OS.  You are suposed to 
#     "brew reinstall llvm", but I got a message that llvm was part of the OS and it suggested 
#     that upgrading was a very bad idea.  You could also compile it from scratch, but this seems
#     to me like it would complicate this build script too much for the benefit
#   - on Linux, I was able to get clang-tidy to work by using "sudo apt-get -y install clang clang-tidy"
#     but this requires installing clang and clang-tidy.  I have a better solution using Visual Studio
#   - on Ubuntu, "sudo apt-get -y install cppcheck" seems to hang my build machines, so that sucks.
#   - Visual Studio now includes support for both it's own static analysis tool and clang-tidy.  This seems to
#     be the easiest ways to access these tools for us since they require no additional installation.
#   - by adding "/p:EnableClangTidyCodeAnalysis=True /p:RunCodeAnalysis=True" to MSBuild I can get the static
#     analysis tools to run on the build system, but they won't run in typical builds in Visual Studio, which
#     would slow down our builds.
#   - If you want to enable these static checks on build in Visual Studio, go to:
#     "Solution Explorer" -> right click the project "ebm_native" -> "Properties" -> "Code Analysis"
#     From there you can enable "Clang-Tidy" and "Enable Code Analysis on Build"
#   - You also for free see the Visual Studio static analysis in the "Error List" window if you have
#     "Build + IntelliSense" selected in the drop down window with that option.
#   - any static analysis warnings don't kill the build it seems.  That's good since static analysis tool warnings
#     constantly change, so we probably don't want to turn them into errors otherwise it'll constantly be breaking.
#   - https://include-what-you-use.org/ is alpha, and it looks like it changes a lot.  Doesn't seem worth the benefit.
#   - NOTE: scan-build and clang-tidy are really the same thing, but with different interfaces

# The only things that Linux makes illegal in filenames are the zero termination character '\0' and the path character '/'
# This makes it hard to write shell scripts that handle things like control characters, spaces, newlines, etc properly.
# In Linux filenames and directories often don't have spaces and scripts often don't handle them.  In Windows
# we often do have spaces in directory names though, and we want to be able to build from the Windows Bash shell,
# so we handle them here.
# We need to pass multiple directory/filenames pairs into g++/clang++ from multiple different directories 
# (making find hard), and we also have additional files we use (see --version-script), so we need to build up 
# variables that contain the filesnames to pass into the compiler. This reference says there is no portable way 
# to handle spaces (see 1.4 Template: Building up a variable), 
# so they recommend setting IFS to tab and newline, which means files with tab and newline won't work:
# https://dwheeler.com/essays/filenames-in-shell.html
# I'm not quite sure that's true.  If we use the often frowned upon eval command we can put single quotes arround
# any strings that we use, and eval will parse them correctly with spaces.  This opens us up to issues with eval, 
# so we need to sanitize our strings beforehand similar to this discussion, although printf "%q" is too new
# currently (2016) for us to take a dependency on it, so we use sed to sanitize our single quote filenames instead:
# https://stackoverflow.com/questions/17529220/why-should-eval-be-avoided-in-bash-and-what-should-i-use-instead
#
# Here are some good references on the issues regarding odd characters in filenames: 
# - https://dwheeler.com/essays/filenames-in-shell.html
# - https://dwheeler.com/essays/fixing-unix-linux-filenames.html
# These should work in our script below (some have been explicitly tested):
# - newlines in files "a.cpp\nb.cpp" which can be interpreted as separate files in some scripts
# - files that start with '-' characters.  eg: "-myfile.txt" which can be interpreted as arguments in some scripts
# - files that begin or end or contain spaces eg: "  a.cpp  b.cpp  " which get stripped or turned into multiple arguments
# - tab characters "\t"
# - string escape characters "\\"
# - quote characters "\"" or "\'" or "\`"
# - asterix in filenames "*" eg: "*.cpp" which can get glob expanded
# - ';' character -> which can be used to run new shell commands in some scripts
# - control characters (ASCII 1-31)
# - UTF-8 characters
# - try the following stress test case (works on windows):     ./-in ter;_Pr`e't/shared/ebm_native/-ha rd;_Fi`l'e.cpp
# We also cannot use the following safely:
# - find exec with the \; ending since it eats the return codes of our compiler, which we really really want!
# - raw "exec" without re-shelling the result
#   https://unix.stackexchange.com/questions/156008/is-it-possible-to-use-find-exec-sh-c-safely
# - ld -> for C++ programs we need to know implementation specific directories and object files for initialization.
#   We re-call g++/clang++ to link with object files instead.  We need to separate our compile and link steps because
#   we compile the same C++ files over several times with different compiler options so these need to generate
#   separated .o files with different names.  I'm not sure if GNU make/cmake handles this natievly if we go that route.
# - make -> well, we might use make someday if compile speed becomes an issue, but I like that this script doesn't 
#   require installing anything before calling it on either standard mac or linux machines, and GNU make requires installation 
#   on macs and isn't part of the standard clang++ build pipeline.  cmake also requires installation.  Bourne shell POSIX script 
#   is the most out of the box compatible solution.  Also, per above, I'm not sure if make/cmake handles duplicate
#   compilation of .cpp files multiple times with different compiler options
# - tee -> we write the compiler output to both a file and to stdout, but tee swallows any error codes in the compiler
#   I've been using backticks to store the output in a variable first, which is frowned upon, so consider
#   command substitution instead, which is now even part of the more recent bourne shells and is POSIX compliant now
#   PIPESTATUS is bash specific
# - no command substitution (although I might change my mind on this given POSIX now supports command substitution).  
#   We don't use backticks much here so it's low cost to use the older method.  Backticks are more compatible, 
#   but also command substitution seems to remove trailing newlines, which although esoteric introduces an error 
#   condition we'd want to at least investigate and/or check and/or handle.
#   https://superuser.com/questions/403800/how-can-i-make-the-bash-backtick-operator-keep-newlines-in-output/827879
# - don't use echo "$something".  Use printf "%s" "$something"

# TODO also build our html resources here, and also in the .bat file for Windows

sanitize() {
   # use this techinque where single quotes are expanded to '\'' (end quotes insert single quote, start quote)
   # but fixed from the version in this thread: 
   # https://stackoverflow.com/questions/15783701/which-characters-need-to-be-escaped-when-using-bash
   # https://stackoverflow.com/questions/17529220/why-should-eval-be-avoided-in-bash-and-what-should-i-use-instead
   printf "%s" "$1" | sed "s/'/'\\\\''/g; 1s/^/'/; \$s/\$/'/"
}

make_initial_paths_simple() {
   local obj_path_unsanitized="$1"
   local bin_path_unsanitized="$2"

   [ -d "$obj_path_unsanitized" ] || mkdir -p "$obj_path_unsanitized"
   ret_code=$?
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi
   [ -d "$bin_path_unsanitized" ] || mkdir -p "$bin_path_unsanitized"
   ret_code=$?
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi
}

compile_file() {
   local compiler="$1"
   local compiler_args_sanitized="$2"
   local file_unsanitized="$3"
   local obj_path_unsanitized="$4"
   local zone="$5"

   # glob expansion returns *.cpp or *.c when there are no matches, so we need to check for the existance of the file
   if [ -f "$file_unsanitized" ] ; then
      local file_sanitized=`sanitize "$file_unsanitized"`
      # https://www.oncrashreboot.com/use-sed-to-split-path-into-filename-extension-and-directory
      local file_body_unsanitized=`printf "%s" "$file_unsanitized" | sed 's/\\(.*\\)\\/\\(.*\\)\\.\\(.*\\)$/\\2/'`
      local object_full_file_unsanitized="$obj_path_unsanitized/${file_body_unsanitized}_$zone.o"
      local object_full_file_sanitized=`sanitize "$object_full_file_unsanitized"`
      all_object_files_sanitized="$all_object_files_sanitized $object_full_file_sanitized"
      local compile_specific="$compiler $compiler_args_sanitized -c $file_sanitized -o $object_full_file_sanitized 2>&1"
      compile_out=`eval $compile_specific`
      # TODO: we might need to sanitize compile_out here!
      local ret_code=$?
      compile_out_full="$compile_out_full$compile_out"
      if [ $ret_code -ne 0 ]; then 
         printf "%s\n" "$compile_out_full"
         printf "%s\n" "$compile_out_full" > "$log_file"
         exit $ret_code
      fi
   fi
}

compile_directory_c() {
   local compiler="$1"
   local compiler_args_sanitized="$2"
   local src_path_unsanitized="$3"
   local obj_path_unsanitized="$4"
   local zone="$5"

   # zsh (default shell in macs) terminates if you try to glob expand zero results, so check first
   find "$src_path_unsanitized" -maxdepth 1 -type f -name '*.c' 2>/dev/null | grep -q .
   if [ $? -eq 0 ]; then 
      # use globs with preceeding directory per: https://dwheeler.com/essays/filenames-in-shell.html
      for file_unsanitized in "$src_path_unsanitized"/*.c ; do
         compile_file "$compiler" "$compiler_args_sanitized" "$file_unsanitized" "$obj_path_unsanitized" "$zone"
      done
   fi
}

compile_directory_cpp() {
   local compiler="$1"
   local compiler_args_sanitized="$2"
   local src_path_unsanitized="$3"
   local obj_path_unsanitized="$4"
   local zone="$5"

   # zsh (default shell in macs) terminates if you try to glob expand zero results, so check first
   find "$src_path_unsanitized" -maxdepth 1 -type f -name '*.cpp' 2>/dev/null | grep -q .
   if [ $? -eq 0 ]; then 
      # use globs with preceeding directory per: https://dwheeler.com/essays/filenames-in-shell.html
      for file_unsanitized in "$src_path_unsanitized"/*.cpp ; do
         compile_file "$compiler" "$compiler_args_sanitized" "$file_unsanitized" "$obj_path_unsanitized" "$zone"
      done
   fi
}

compile_compute() {
   local compiler="$1"
   local compiler_args_sanitized="$2"
   local src_path_sanitized="$3"
   local src_path_unsanitized="$4"
   local obj_path_unsanitized="$5"
   local zone="$6"

   compile_directory_cpp "$compiler" "$compiler_args_sanitized -DZONE_$zone" "$src_path_unsanitized/compute" "$obj_path_unsanitized" "$zone"
   compile_directory_cpp "$compiler" "$compiler_args_sanitized -I$src_path_sanitized/compute/${zone}_ebm -DZONE_$zone" "$src_path_unsanitized/compute/${zone}_ebm" "$obj_path_unsanitized" "$zone"
}

link_file() {
   local linker="$1"
   local linker_args_sanitized="$2"
   local all_object_files_sanitized="$3"
   local bin_path_unsanitized="$4"
   local bin_file="$5"
   local log_file_unsanitized="$6"

   local bin_path_sanitized=`sanitize "$bin_path_unsanitized"`
   local compile_specific="$linker $linker_args_sanitized $all_object_files_sanitized -o $bin_path_sanitized/$bin_file 2>&1"
   compile_out=`eval $compile_specific`
   # TODO: we might need to sanitize compile_out here!
   local ret_code=$?
   compile_out_full="$compile_out_full$compile_out"
   printf "%s\n" "$compile_out_full"
   printf "%s\n" "$compile_out_full" > "$log_file_unsanitized"
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi
}

copy_bin_files() {
   local bin_path_unsanitized="$1"
   local bin_file="$2"
   local python_lib_unsanitized="$3"
   local staging_path_unsanitized="$4"

   cp "$bin_path_unsanitized/$bin_file" "$python_lib_unsanitized/"
   ret_code=$?
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi
   cp "$bin_path_unsanitized/$bin_file" "$staging_path_unsanitized/"
   ret_code=$?
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi
}

build_32_bit=0
build_64_bit=1
for arg in "$@"; do
   if [ "$arg" = "-32bit" ]; then
      build_32_bit=1
   fi
   if [ "$arg" = "-no64bit" ]; then
      build_64_bit=0
   fi
done

# TODO: this could be improved upon.  There is no perfect solution AFAIK for getting the script directory, and I'm not too sure how the CDPATH thing works
# Look at BASH_SOURCE[0] as well and possibly select either it or $0
# The output here needs to not be the empty string for glob substitution below:
root_path_initial=`dirname -- "$0"`
root_path_unsanitized=`CDPATH= cd -- "$root_path_initial" && pwd -P`
if [ ! -f "$root_path_unsanitized/build.sh" ] ; then
   # there are all kinds of reasons why we might not have gotten the script path in $0.  It's more of a convention
   # than a requirement to have either the full path or even the script itself.  There are far more complicated
   # scripts out there that attempt to use various shell specific workarounds, like BASH_SOURCE[0] to best solve
   # the problem, but it's possible in theory to be running over an SSL connection without a script on the local
   # system at all, so getting the directory is a fundamentally unsolved problem.  We can terminate though if
   # we find ourselves in such a weird condition.  This also happens when the "source" command is used.
   printf "Could not find script file root directory for building InterpretML.  Exiting."
   exit 1
fi

root_path_sanitized=`sanitize "$root_path_unsanitized"`
src_path_unsanitized="$root_path_unsanitized/shared/ebm_native"
src_path_sanitized=`sanitize "$src_path_unsanitized"`
python_lib_unsanitized="$root_path_unsanitized/python/interpret-core/interpret/lib"
python_lib_sanitized=`sanitize "$python_lib_unsanitized"`
staging_path_unsanitized="$root_path_unsanitized/staging"
staging_path_sanitized=`sanitize "$staging_path_unsanitized"`

# re-enable these warnings when they are better supported by g++ or clang: -Wduplicated-cond -Wduplicated-branches -Wrestrict
both_args=""
both_args="$both_args -Wall -Wextra"
both_args="$both_args -Wunused-result"
both_args="$both_args -Wno-parentheses"
both_args="$both_args -Wdouble-promotion"
both_args="$both_args -Wshadow"
both_args="$both_args -Wformat=2"
both_args="$both_args -fvisibility=hidden"
both_args="$both_args -fno-math-errno -fno-trapping-math"
both_args="$both_args -march=core2"
both_args="$both_args -fpic"
both_args="$both_args -pthread"
both_args="$both_args -DEBM_NATIVE_EXPORTS"

c_args="-std=c99"

cpp_args="-std=c++11"
cpp_args="$cpp_args -Wold-style-cast"
cpp_args="$cpp_args -fvisibility-inlines-hidden"

common_args="-I$src_path_sanitized/inc"
common_args="$common_args -I$src_path_sanitized/common_c"
common_args="$common_args -I$src_path_sanitized/common_cpp"

bridge_args="$common_args"
bridge_args="$bridge_args -I$src_path_sanitized/bridge_c"
bridge_args="$bridge_args -I$src_path_sanitized/bridge_cpp"

main_args="$bridge_args"
main_args="$main_args -I$src_path_sanitized"

compute_args="$bridge_args"
compute_args="$compute_args -I$src_path_sanitized/compute"
compute_args="$compute_args -I$src_path_sanitized/compute/loss_functions"
compute_args="$compute_args -I$src_path_sanitized/compute/metrics"

# add any other non-include options
common_args="$common_args -Wno-format-nonliteral"

os_type=`uname`

if [ "$os_type" = "Darwin" ]; then
   # reference on rpath & install_name: https://www.mikeash.com/pyblog/friday-qa-2009-11-06-linking-and-install-names.html

   # try moving some of these clang specific warnings into both_args if g++ eventually supports them
   c_compiler=clang
   cpp_compiler=clang++
   both_args="$both_args -Wnull-dereference -Wgnu-zero-variadic-macro-arguments"

   printf "%s\n" "Creating initial directories"
   [ -d "$staging_path_unsanitized" ] || mkdir -p "$staging_path_unsanitized"
   ret_code=$?
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi
   [ -d "$python_lib_unsanitized" ] || mkdir -p "$python_lib_unsanitized"
   ret_code=$?
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi

   if [ $build_64_bit -eq 1 ]; then
      ########################## macOS release|x64

      printf "%s\n" "Compiling ebm_native with $c_compiler/$cpp_compiler for macOS release|x64"
      obj_path_unsanitized="$root_path_unsanitized/tmp/clang/obj/release/mac/x64/ebm_native"
      bin_path_unsanitized="$root_path_unsanitized/tmp/clang/bin/release/mac/x64/ebm_native"
      bin_file="lib_ebm_native_mac_x64.dylib"
      log_file_unsanitized="$obj_path_unsanitized/ebm_native_release_mac_x64_build_log.txt"
      both_args_extra="-m64 -DNDEBUG -O3"
      c_args_specific="$c_args $both_args $both_args_extra"
      cpp_args_specific="$cpp_args $both_args $both_args_extra"
      link_args_specific="$cpp_args_specific -dynamiclib -install_name @rpath/$bin_file"
   
      all_object_files_sanitized=""
      compile_out_full=""

      make_initial_paths_simple "$obj_path_unsanitized" "$bin_path_unsanitized"
      compile_directory_c "$c_compiler" "$c_args_specific $common_args" "$src_path_unsanitized/common_c" "$obj_path_unsanitized" "C"
      compile_directory_c "$c_compiler" "$c_args_specific $bridge_args" "$src_path_unsanitized/bridge_c" "$obj_path_unsanitized" "C"
      compile_directory_cpp "$cpp_compiler" "$cpp_args_specific $main_args -DZONE_main" "$src_path_unsanitized" "$obj_path_unsanitized" "main"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "cpu"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "avx512"
      link_file "$cpp_compiler" "$link_args_specific" "$all_object_files_sanitized" "$bin_path_unsanitized" "$bin_file" "$log_file_unsanitized"
      copy_bin_files "$bin_path_unsanitized" "$bin_file" "$python_lib_unsanitized" "$staging_path_unsanitized"

      ########################## macOS debug|x64

      printf "%s\n" "Compiling ebm_native with $c_compiler/$cpp_compiler for macOS debug|x64"
      obj_path_unsanitized="$root_path_unsanitized/tmp/clang/obj/debug/mac/x64/ebm_native"
      bin_path_unsanitized="$root_path_unsanitized/tmp/clang/bin/debug/mac/x64/ebm_native"
      bin_file="lib_ebm_native_mac_x64_debug.dylib"
      log_file_unsanitized="$obj_path_unsanitized/ebm_native_debug_mac_x64_build_log.txt"
      both_args_extra="-m64 -O1 -fsanitize=address,undefined -fno-sanitize-recover=address,undefined -fno-optimize-sibling-calls -fno-omit-frame-pointer"
      c_args_specific="$c_args $both_args $both_args_extra"
      cpp_args_specific="$cpp_args $both_args $both_args_extra"
      link_args_specific="$cpp_args_specific -dynamiclib -install_name @rpath/$bin_file"
   
      all_object_files_sanitized=""
      compile_out_full=""

      make_initial_paths_simple "$obj_path_unsanitized" "$bin_path_unsanitized"
      compile_directory_c "$c_compiler" "$c_args_specific $common_args" "$src_path_unsanitized/common_c" "$obj_path_unsanitized" "C"
      compile_directory_c "$c_compiler" "$c_args_specific $bridge_args" "$src_path_unsanitized/bridge_c" "$obj_path_unsanitized" "C"
      compile_directory_cpp "$cpp_compiler" "$cpp_args_specific $main_args -DZONE_main" "$src_path_unsanitized" "$obj_path_unsanitized" "main"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "cpu"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "avx512"
      link_file "$cpp_compiler" "$link_args_specific" "$all_object_files_sanitized" "$bin_path_unsanitized" "$bin_file" "$log_file_unsanitized"
      copy_bin_files "$bin_path_unsanitized" "$bin_file" "$python_lib_unsanitized" "$staging_path_unsanitized"
   fi
elif [ "$os_type" = "Linux" ]; then

   c_compiler=gcc
   cpp_compiler=g++

   # try moving some of these g++ specific warnings into both_args if clang eventually supports them
   both_args="$both_args -Wlogical-op -Wl,--version-script=$src_path_sanitized/ebm_native_exports.txt -Wl,--exclude-libs,ALL -Wl,-z,relro,-z,now"
   both_args="$both_args -Wl,--wrap=memcpy -static-libgcc -static-libstdc++ -shared"

   printf "%s\n" "Creating initial directories"
   [ -d "$staging_path_unsanitized" ] || mkdir -p "$staging_path_unsanitized"
   ret_code=$?
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi
   [ -d "$python_lib_unsanitized" ] || mkdir -p "$python_lib_unsanitized"
   ret_code=$?
   if [ $ret_code -ne 0 ]; then 
      exit $ret_code
   fi

   if [ $build_64_bit -eq 1 ]; then
      ########################## Linux release|x64

      printf "%s\n" "Compiling ebm_native with $c_compiler/$cpp_compiler for Linux release|x64"
      obj_path_unsanitized="$root_path_unsanitized/tmp/gcc/obj/release/linux/x64/ebm_native"
      bin_path_unsanitized="$root_path_unsanitized/tmp/gcc/bin/release/linux/x64/ebm_native"
      bin_file="lib_ebm_native_linux_x64.so"
      log_file_unsanitized="$obj_path_unsanitized/ebm_native_release_linux_x64_build_log.txt"
      both_args_extra="-m64 -DNDEBUG -O3"
      c_args_specific="$c_args $both_args $both_args_extra"
      cpp_args_specific="$cpp_args $both_args $both_args_extra"
      link_args_specific="$cpp_args_specific"
   
      all_object_files_sanitized=""
      compile_out_full=""

      make_initial_paths_simple "$obj_path_unsanitized" "$bin_path_unsanitized"
      compile_directory_c "$c_compiler" "$c_args_specific $common_args" "$src_path_unsanitized/common_c" "$obj_path_unsanitized" "C"
      compile_directory_c "$c_compiler" "$c_args_specific $bridge_args" "$src_path_unsanitized/bridge_c" "$obj_path_unsanitized" "C"
      compile_directory_cpp "$cpp_compiler" "$cpp_args_specific $main_args -DZONE_main" "$src_path_unsanitized" "$obj_path_unsanitized" "main"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "cpu"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "avx512"
      compile_file "$cpp_compiler" "$cpp_args_specific" "$src_path_unsanitized"/special/linux_wrap_functions.cpp "$obj_path_unsanitized" "NONE"
      link_file "$cpp_compiler" "$link_args_specific" "$all_object_files_sanitized" "$bin_path_unsanitized" "$bin_file" "$log_file_unsanitized"
      copy_bin_files "$bin_path_unsanitized" "$bin_file" "$python_lib_unsanitized" "$staging_path_unsanitized"

      ########################## Linux debug|x64

      printf "%s\n" "Compiling ebm_native with $c_compiler/$cpp_compiler for Linux debug|x64"
      obj_path_unsanitized="$root_path_unsanitized/tmp/gcc/obj/debug/linux/x64/ebm_native"
      bin_path_unsanitized="$root_path_unsanitized/tmp/gcc/bin/debug/linux/x64/ebm_native"
      bin_file="lib_ebm_native_linux_x64_debug.so"
      log_file_unsanitized="$obj_path_unsanitized/ebm_native_debug_linux_x64_build_log.txt"
      both_args_extra="-m64 -O1"
      c_args_specific="$c_args $both_args $both_args_extra"
      cpp_args_specific="$cpp_args $both_args $both_args_extra"
      link_args_specific="$cpp_args_specific"
   
      all_object_files_sanitized=""
      compile_out_full=""

      make_initial_paths_simple "$obj_path_unsanitized" "$bin_path_unsanitized"
      compile_directory_c "$c_compiler" "$c_args_specific $common_args" "$src_path_unsanitized/common_c" "$obj_path_unsanitized" "C"
      compile_directory_c "$c_compiler" "$c_args_specific $bridge_args" "$src_path_unsanitized/bridge_c" "$obj_path_unsanitized" "C"
      compile_directory_cpp "$cpp_compiler" "$cpp_args_specific $main_args -DZONE_main" "$src_path_unsanitized" "$obj_path_unsanitized" "main"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "cpu"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "avx512"
      compile_file "$cpp_compiler" "$cpp_args_specific" "$src_path_unsanitized"/special/linux_wrap_functions.cpp "$obj_path_unsanitized" "NONE"
      link_file "$cpp_compiler" "$link_args_specific" "$all_object_files_sanitized" "$bin_path_unsanitized" "$bin_file" "$log_file_unsanitized"
      copy_bin_files "$bin_path_unsanitized" "$bin_file" "$python_lib_unsanitized" "$staging_path_unsanitized"
   fi

   if [ $build_32_bit -eq 1 ]; then
      ########################## Linux release|x86

      printf "%s\n" "Compiling ebm_native with $c_compiler/$cpp_compiler for Linux release|x86"
      obj_path_unsanitized="$root_path_unsanitized/tmp/gcc/obj/release/linux/x86/ebm_native"
      bin_path_unsanitized="$root_path_unsanitized/tmp/gcc/bin/release/linux/x86/ebm_native"
      bin_file="lib_ebm_native_linux_x86.so"
      log_file_unsanitized="$obj_path_unsanitized/ebm_native_release_linux_x86_build_log.txt"
      both_args_extra="-msse2 -mfpmath=sse -m32 -DNDEBUG -O3"
      c_args_specific="$c_args $both_args $both_args_extra"
      cpp_args_specific="$cpp_args $both_args $both_args_extra"
      link_args_specific="$cpp_args_specific"
      
      all_object_files_sanitized=""
      compile_out_full=""

      if [ ! -d "$obj_path_unsanitized" ]; then
         printf "%s\n" "Doing first time installation of x86"

         # this is the first time we're being compiled x86 on this machine, so install other required items

         # TODO consider NOT running sudo inside this script and move that requirement to the caller
         #      per https://askubuntu.com/questions/425754/how-do-i-run-a-sudo-command-inside-a-script

         sudo apt-get -y update
         ret_code=$?
         if [ $ret_code -ne 0 ]; then 
            exit $ret_code
         fi

         sudo apt-get -y install g++-multilib
         ret_code=$?
         if [ $ret_code -ne 0 ]; then 
            exit $ret_code
         fi

         mkdir -p "$obj_path_unsanitized"
      fi
      ret_code=$?
      if [ $ret_code -ne 0 ]; then 
         exit $ret_code
      fi
      [ -d "$bin_path_unsanitized" ] || mkdir -p "$bin_path_unsanitized"
      ret_code=$?
      if [ $ret_code -ne 0 ]; then 
         exit $ret_code
      fi

      compile_directory_c "$c_compiler" "$c_args_specific $common_args" "$src_path_unsanitized/common_c" "$obj_path_unsanitized" "C"
      compile_directory_c "$c_compiler" "$c_args_specific $bridge_args" "$src_path_unsanitized/bridge_c" "$obj_path_unsanitized" "C"
      compile_directory_cpp "$cpp_compiler" "$cpp_args_specific $main_args -DZONE_main" "$src_path_unsanitized" "$obj_path_unsanitized" "main"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "cpu"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "avx512"
      compile_file "$cpp_compiler" "$cpp_args_specific" "$src_path_unsanitized"/special/linux_wrap_functions.cpp "$obj_path_unsanitized" "NONE"
      link_file "$cpp_compiler" "$link_args_specific" "$all_object_files_sanitized" "$bin_path_unsanitized" "$bin_file" "$log_file_unsanitized"
      copy_bin_files "$bin_path_unsanitized" "$bin_file" "$python_lib_unsanitized" "$staging_path_unsanitized"

      ########################## Linux debug|x86

      printf "%s\n" "Compiling ebm_native with $c_compiler/$cpp_compiler for Linux debug|x86"
      obj_path_unsanitized="$root_path_unsanitized/tmp/gcc/obj/debug/linux/x86/ebm_native"
      bin_path_unsanitized="$root_path_unsanitized/tmp/gcc/bin/debug/linux/x86/ebm_native"
      bin_file="lib_ebm_native_linux_x86_debug.so"
      log_file_unsanitized="$obj_path_unsanitized/ebm_native_debug_linux_x86_build_log.txt"
      both_args_extra="-msse2 -mfpmath=sse -m32 -O1"
      c_args_specific="$c_args $both_args $both_args_extra"
      cpp_args_specific="$cpp_args $both_args $both_args_extra"
      link_args_specific="$cpp_args_specific"
      
      all_object_files_sanitized=""
      compile_out_full=""

      make_initial_paths_simple "$obj_path_unsanitized" "$bin_path_unsanitized"
      compile_directory_c "$c_compiler" "$c_args_specific $common_args" "$src_path_unsanitized/common_c" "$obj_path_unsanitized" "C"
      compile_directory_c "$c_compiler" "$c_args_specific $bridge_args" "$src_path_unsanitized/bridge_c" "$obj_path_unsanitized" "C"
      compile_directory_cpp "$cpp_compiler" "$cpp_args_specific $main_args -DZONE_main" "$src_path_unsanitized" "$obj_path_unsanitized" "main"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "cpu"
      compile_compute "$cpp_compiler" "$cpp_args_specific $compute_args" "$src_path_sanitized" "$src_path_unsanitized" "$obj_path_unsanitized" "avx512"
      compile_file "$cpp_compiler" "$cpp_args_specific" "$src_path_unsanitized"/special/linux_wrap_functions.cpp "$obj_path_unsanitized" "NONE"
      link_file "$cpp_compiler" "$link_args_specific" "$all_object_files_sanitized" "$bin_path_unsanitized" "$bin_file" "$log_file_unsanitized"
      copy_bin_files "$bin_path_unsanitized" "$bin_file" "$python_lib_unsanitized" "$staging_path_unsanitized"
   fi
else
   printf "%s\n" "OS $os_type not recognized.  We support clang/clang++ on macOS and gcc/g++ on Linux"
   exit 1
fi
