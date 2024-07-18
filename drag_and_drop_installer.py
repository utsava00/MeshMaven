"""
MeshMaven: A tool for managing and manipulating meshes in Maya.
Copyright (C) 2024  Utsava

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import os
import shutil
import maya.cmds as cmds
import maya.mel as mel


def install_meshmaven_tool(*args):
    """
    Installs the MeshMaven tool by copying necessary files to the Maya scripts directory.
    """
    # Current directory and file paths
    cur_path = os.path.dirname(__file__)
    scripts_folder = cmds.internalVar(userScriptDir=True)
    shelf_dir = cmds.internalVar(userShelfDir=True)

    # Files to be installed
    gui_file = os.path.join(cur_path, 'Scripts', 'meshmaven_gui.py')
    core_file = os.path.join(cur_path, 'Scripts', 'meshmaven_core.py')
    mel_file = os.path.join(cur_path, 'Scripts', 'shelf_MeshMaven.mel')

    # Confirm installation
    result = cmds.confirmDialog(title='Install MeshMaven Tool',
                                message='Installing MeshMaven Tool to:\n%s\n\nContinue?' % scripts_folder,
                                button=['Continue', 'Cancel'],
                                defaultButton='Continue',
                                cancelButton='Cancel',
                                dismissString='Cancel')
    if result != 'Continue':
        return

    # Function to copy files with overwrite if exists
    def copy_with_overwrite(src, dst):
        if os.path.exists(dst):
            os.remove(dst)  # Remove existing file
        shutil.copy(src, dst)

    # Copy files with overwrite if necessary
    try:
        copy_with_overwrite(gui_file, os.path.join(scripts_folder, 'meshmaven_gui.py'))
        copy_with_overwrite(core_file, os.path.join(scripts_folder, 'meshmaven_core.py'))
        copy_with_overwrite(mel_file, os.path.join(shelf_dir, 'shelf_MeshMaven.mel'))
    except Exception as e:
        cmds.warning('Failed to copy files: %s' % str(e))
        return

    # Load shelf if not existing
    shelf_file = os.path.join(shelf_dir, 'shelf_MeshMaven.mel').replace('\\', '/')
    mel.eval('source "%s"' % shelf_file)
    mel.eval('shelf_MeshMaven()')

    cmds.confirmDialog(title='MeshMaven Installed',
                       message='MeshMaven Tool installed successfully.\nRestart Maya to use the tool.',
                       button=['OK'])

    # Delete __pycache__ directory if it exists
    pycache_dir = os.path.join(scripts_folder, '__pycache__')
    if os.path.exists(pycache_dir):
        shutil.rmtree(pycache_dir, ignore_errors=True)

# Function to handle dropped file action


def onMayaDroppedPythonFile(*args):
    """
    Entry point for executing the installation script when dropped into Maya viewport.
    """
    install_meshmaven_tool()


# Ensure this script can be imported without executing
if __name__ == '__main__':
    install_meshmaven_tool()
