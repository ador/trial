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

# Installing nodejs as a normal user (without sudo)
# Don't forget to source your ~/.bashrc file afterwards!

set -o pipefail
this_dir="$(dirname "$0")"

node_version="0.12.7"
download_url="https://nodejs.org/dist/v0.12.7/node-v${node_version}.tar.gz"
install_dir="$HOME/nodejs-${node_version}-install"
node_bin_dir=${install_dir}/bin

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

# prerequisites of install
check_command "tar" "g++" "make" "python"

# download and unpack
mkdir -p "${install_dir}"
pushd "${install_dir}" > "/dev/null"
  if [ ! -f ${install_dir}/node-v${node_version}.tar.gz ]; then
    echo "Downloading nodejs ${node_version} ..."
    wget "${download_url}"
  fi
  echo "Extracting package..."
  tar zxvf node-v${node_version}.tar.gz -C . > "/dev/null"
  echo "...done"
  echo "Compiling... "
  pushd node-v${node_version} > "/dev/null"
    ./configure --prefix=${install_dir}
    make
    make install
  popd > "/dev/null"
  echo "...done"
popd > "/dev/null"

mkdir -p ${node_bin_dir}

# maybe it does not exist yet
touch ~/.bashrc

d_bashrc_lines="$(cat << BASHRC_LINES
export PATH=$(escape_string "$node_bin_dir"):"\$PATH"
BASHRC_LINES
)"

eval "$d_bashrc_lines"
node -v
echo "$d_bashrc_lines" >> "$HOME/.bashrc_nodejs"

bashrc_line='. "$HOME/.bashrc_nodejs" # automatic generated line'
if ! grep -Fxqe "$bashrc_line" "$HOME/.bashrc"; then
  cat "$HOME/.bashrc" > "$HOME/.bashrc_tmp"
  echo "$bashrc_line" >> "$HOME/.bashrc_tmp"
  mv "$HOME/.bashrc_tmp" "$HOME/.bashrc" 
fi
