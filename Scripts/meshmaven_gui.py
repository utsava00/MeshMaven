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


import sys
import subprocess
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import meshmaven_core as backend


def main():
    check_and_install_packages()

    # Make dialog a global variable
    global dialog

    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass

    # Creating and showing the dialog
    dialog = Ui()
    dialog.show()


def install_package(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def check_and_install_packages():
    """Check and install necessary packages."""
    try:
        import PySide2
    except ImportError:
        install_package('PySide2')
        import PySide2

    try:
        import shiboken2
    except ImportError:
        install_package('shiboken2')
        import shiboken2


def get_maya_window():
    """Retrieve Maya's main window so that new UI elements can be correctly parented to it."""
    main_window_ptr = omui.MQtUtil.mainWindow()

    if sys.version_info.major >= 3:
        # Python 3: Directly use wrapInstance without 'long'
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        # Python 2.7: Use 'long' for compatibility
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class Ui(QtWidgets.QDialog):

    def __init__(self, parent=get_maya_window()):
        super(Ui, self).__init__(parent)

        self.setWindowTitle("MeshMaven")
        self.setMinimumWidth(300)
        flags = (
            QtCore.Qt.Window |
            QtCore.Qt.WindowMinMaxButtonsHint |
            QtCore.Qt.WindowCloseButtonHint
        )
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.core = backend.MeshMavenCore()  # Instantiate the Core class from the core module
        self.widgets()
        self.layouts()
        self.connections()

    def widgets(self):
        """
        Create all the widgets used in the UI.
        """

        # Create labels
        self.label1 = QtWidgets.QLabel("<b>Common Tools</b>")
        self.label2 = QtWidgets.QLabel("<b>Booleans</b>")
        self.label3 = QtWidgets.QLabel("<b>File Check</b>")

        # Create divider lines
        self.line1 = QtWidgets.QFrame()
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line2 = QtWidgets.QFrame()
        self.line2.setFrameShadow(QtWidgets.QFrame.Plain)

        self.line3 = QtWidgets.QFrame()
        self.line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line4 = QtWidgets.QFrame()
        self.line4.setFrameShadow(QtWidgets.QFrame.Plain)

        self.line5 = QtWidgets.QFrame()
        self.line5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line5.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Create axis checkboxes for horizontal layout
        self.checkbox1 = QtWidgets.QCheckBox("X")
        self.checkbox1.setChecked(True)
        self.checkbox2 = QtWidgets.QCheckBox("Y")
        self.checkbox3 = QtWidgets.QCheckBox("Z")

        # Create a button group for axis checkboxes
        self.axis_group = QtWidgets.QButtonGroup()
        self.axis_group.addButton(self.checkbox1)
        self.axis_group.addButton(self.checkbox2)
        self.axis_group.addButton(self.checkbox3)
        self.axis_group.setExclusive(True)

        # Create buttons for horizontal layout
        self.hl1_button1 = QtWidgets.QPushButton("Merge Vertex")
        self.hl1_button2 = QtWidgets.QPushButton("Soften/Harden")

        self.hl2_button1 = QtWidgets.QPushButton("Soften Edge")
        self.hl2_button2 = QtWidgets.QPushButton("Harden Edge")

        self.hl3_button1 = QtWidgets.QPushButton("Combine")
        self.hl3_button2 = QtWidgets.QPushButton("Separate")

        self.hl4_button1 = QtWidgets.QPushButton("Duplicate")
        self.hl4_button2 = QtWidgets.QPushButton("Undo Duplicate")

        self.hl5_button1 = QtWidgets.QPushButton("Bridge")
        self.div_field = QtWidgets.QSpinBox()
        self.div_field.setValue(0)
        self.div_field.setRange(0, 1000)
        self.div_field.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hl6_button1 = QtWidgets.QPushButton("Union")
        self.hl6_button2 = QtWidgets.QPushButton("Difference")
        self.hl6_button3 = QtWidgets.QPushButton("Intersection")

        self.hl7_button1 = QtWidgets.QPushButton("Check")
        self.hl7_button2 = QtWidgets.QPushButton("Export")

    def layouts(self):
        """
        Create all the layouts present in the UI.
        """

        # Create multiple horizontal layouts and add buttons
        h_layout1 = QtWidgets.QHBoxLayout()
        h_layout1.addWidget(self.hl1_button1)
        h_layout1.addWidget(self.hl1_button2)

        h_layout2 = QtWidgets.QHBoxLayout()
        h_layout2.addWidget(self.hl2_button1)
        h_layout2.addWidget(self.hl2_button2)

        h_layout3 = QtWidgets.QHBoxLayout()
        h_layout3.addWidget(self.hl3_button1)
        h_layout3.addWidget(self.hl3_button2)

        h_layout4 = QtWidgets.QHBoxLayout()
        h_layout4.addWidget(self.hl4_button1)
        h_layout4.addWidget(self.hl4_button2)

        h_layout_cbox = QtWidgets.QHBoxLayout()
        h_layout_cbox.addWidget(self.checkbox1, alignment=QtCore.Qt.AlignCenter)
        h_layout_cbox.addWidget(self.checkbox2, alignment=QtCore.Qt.AlignCenter)
        h_layout_cbox.addWidget(self.checkbox3, alignment=QtCore.Qt.AlignCenter)

        h_layout5 = QtWidgets.QHBoxLayout()
        h_layout5.addWidget(self.hl5_button1)
        h_layout5.addWidget(self.div_field)

        h_layout6 = QtWidgets.QHBoxLayout()
        h_layout6.addWidget(self.hl6_button1)
        h_layout6.addWidget(self.hl6_button2)
        h_layout6.addWidget(self.hl6_button3)

        h_layout7 = QtWidgets.QHBoxLayout()
        h_layout7.addWidget(self.hl7_button1)
        h_layout7.addWidget(self.hl7_button2)

        # Create main layout and add other layouts and widgets
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.label1, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.line1)
        main_layout.addLayout(h_layout1)
        main_layout.addLayout(h_layout2)
        main_layout.addLayout(h_layout3)
        main_layout.addLayout(h_layout4)
        main_layout.addLayout(h_layout_cbox)
        main_layout.addWidget(self.line2)

        main_layout.addWidget(self.label2, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.line3)
        main_layout.addLayout(h_layout5)
        main_layout.addLayout(h_layout6)
        main_layout.addWidget(self.line4)

        main_layout.addWidget(self.label3, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.line5)
        main_layout.addLayout(h_layout7)
        main_layout.addStretch()

    def connections(self):
        """
        Connect all the respective buttons with their backend counterparts.
        """

        # Connect buttons
        self.hl1_button1.clicked.connect(self.core.merge_vertex)
        self.hl1_button2.clicked.connect(self.core.soften_harden)
        self.hl2_button1.clicked.connect(self.core.soften_edge)
        self.hl2_button2.clicked.connect(self.core.harden_edge)
        self.hl3_button1.clicked.connect(self.core.combine)
        self.hl3_button2.clicked.connect(self.core.separate)
        self.hl4_button1.clicked.connect(self.call_duplicate)
        self.hl4_button2.clicked.connect(self.core.undo)
        self.hl5_button1.clicked.connect(self.call_bridge)
        self.hl6_button1.clicked.connect(self.core.union)
        self.hl6_button2.clicked.connect(self.core.difference)
        self.hl6_button3.clicked.connect(self.core.intersection)
        self.hl7_button1.clicked.connect(self.core.check)
        self.hl7_button2.clicked.connect(self.core.export)

    def call_duplicate(self):
        """
        Utilize the backend duplicate method from the core file 
        to connect with UI with proper inputs from the user.
        """

        axis = None
        if self.checkbox1.isChecked():
            axis = "X"
        elif self.checkbox2.isChecked():
            axis = "Y"
        elif self.checkbox3.isChecked():
            axis = "Z"

        self.core.duplicate(axis)

    def call_bridge(self):
        """
        Utilize the backend bridge method from the core file 
        to connect with UI with proper inputs from the user.
        """

        division = self.div_field.value()

        self.core.bridge(division)


if __name__ == "__main__":

    main()
