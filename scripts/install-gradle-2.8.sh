#!/bin/bash -eu

# The MIT License
#
# Copyright (c) 2014, András Radnai, Adrienn Szabó
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 

# Don't forget to source your ~/.bashrc file afterwards!

set -o pipefail
this_dir="$(dirname "$0")"

gradle_version="2.8"
gradle_download_url="https://services.gradle.org/distributions/gradle-${gradle_version}-bin.zip"
gradle_install_dir="$HOME/gradle-${gradle_version}-install"
gradle_home="${gradle_install_dir}/gradle-${gradle_version}/"


escape_string () 
{
    string="$1";
    echo -n "'$(echo -n "$string" | sed "s|'|'\\\''|g")'"
}

function check_command {
  declare command_name
  for command_name in "$@"; do
    compgen -c "$command_name" | grep -Fxqe "$command_name" || (echo "$command_name: command not found, but needed"; false )
  done
}

check_command "unzip" "java"

mkdir -p "${gradle_install_dir}"
pushd "${gradle_install_dir}" > "/dev/null"
  if [ ! -f ${gradle_install_dir}/gradle-${gradle_version}-all.zip ]; then
    echo "Downloading gradle ${gradle_version} ..."
    wget "${gradle_download_url}"
  fi
  echo "Extracting package..."
  unzip -o "$(basename "${gradle_download_url}")" > "/dev/null"
  echo ...done
popd > "/dev/null"

mkdir -p ${gradle_home}

if ! [ -d "$gradle_home" ]; then (
  echo "Installation not complete: $gradle_home is not a valid directory. PATH variable won't be set"
  false
) fi

# maybe it does not exist yet
touch ~/.bashrc

d_bashrc_lines="$(cat << BASHRC_LINES
export GRADLE_HOME=$(escape_string "$gradle_home")
export PATH=$(escape_string "$gradle_home/bin"):"\$PATH"
BASHRC_LINES
)"

eval "$d_bashrc_lines"
gradle -version
echo "$d_bashrc_lines" >> "$HOME/.bashrc_gradle"

bashrc_line='. "$HOME/.bashrc_gradle" # automatic generated line w3'
if ! grep -Fxqe "$bashrc_line" "$HOME/.bashrc"; then
  cat "$HOME/.bashrc" > "$HOME/.bashrc_tmp"
  echo "$bashrc_line" >> "$HOME/.bashrc_tmp"
  mv "$HOME/.bashrc_tmp" "$HOME/.bashrc" 
fi
