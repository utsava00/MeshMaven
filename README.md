# MeshMaven

MeshMaven is a powerful tool designed for Autodesk Maya to streamline and enhance your 3D modeling workflow. This tool provides an easy-to-use interface and various features to help you manage and manipulate meshes efficiently, saving you time and improving your productivity in creating detailed and complex 3D models.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Files](#files)
- [Design Choices](#design-choices)
- [Testing and Compatibility](#testing-and-compatibility)
- [License](#license)
- [Semantic Versioning](#semantic-versioning)
- [Version Control](#version-control)
- [Development Notes](#development-notes)
- [Contributing](#contributing)
- [Support](#support)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Autodesk Maya 2018.2 or later (MeshMaven has been tested on Maya 2018.2 on Windows and Maya 2024.2 on both Windows and Linux)
- Python 2.7 or Python 3.x (depending on the version of Maya)

## Installation

To install MeshMaven, follow these steps:

1. Download the MeshMaven repository from GitHub.
2. Extract the contents of the zip file to a directory of your choice.
3. Open Autodesk Maya.
4. Drag and drop the `drag_and_drop_installer.py` file into the Maya viewport.
5. Follow the prompts to complete the installation process.

![Installation](Images/meshmaven_installation.gif)

**Note:** You must restart Maya after installation for the tool to be available.

The installation script will copy the necessary files to the scripts directory of the corresponding Maya version you are using and create a new shelf with a MeshMaven icon for easy access.

## Features

MeshMaven offers a variety of features designed to enhance your modeling workflow:

- **Automatic Installation**: The tool can be installed effortlessly by dragging and dropping the installer into Maya.
- **Unique Duplicate Function**: The duplicate function sets the pivot to the vertex closest to the mirror axis rather than Maya's default duplication where the object is duplicated from the center of the object or the center of the world.
- **Enhanced Access to Maya Operations**:
  - **Merge Vertex, Soften/Harden, Soften Edge, Harden Edge, Combine, Separate, Bridge, Union, Difference, Intersection**: These are default Maya options which usually take longer to access due to multiple menu navigation steps. MeshMaven provides direct buttons for these operations on the tool for easy and quick access.
- **Mesh Error Checking**: The Check button on the tool checks the selected mesh for any errors like faces with more than 4 sides, concave faces, faces with holes, non-manifold geometry, and selects the faces or vertices with errors.

## Usage

Using MeshMaven is straightforward:

1. After installing, open Maya.
2. Navigate to the new "MeshMaven" shelf created during installation.
3. Click the MeshMaven icon to launch the GUI.
4. Use the GUI to access various mesh manipulation features:
   - Select the object you want to manipulate.
   - Choose the desired operation (e.g., Duplicate, Bridge).
   - Adjust settings as needed and apply the changes.

![Usage](Images/meshmaven_usage.gif)

## Files

Here is a detailed description of the files included in the MeshMaven project:

- `Scripts/meshmaven_gui.py`: This file contains the GUI code for MeshMaven. It defines the user interface and handles user interactions.
- `Scripts/meshmaven_core.py`: This file includes the core functionality for mesh manipulation. It contains the algorithms for mirroring, scaling, and getting vertex closest to axis.
- `drag_and_drop_installer.py`: The installer script that sets up MeshMaven in Maya. It copies necessary files to the appropriate directories and creates a new shelf with the MeshMaven icon.
- `shelf_MeshMaven.mel`: This MEL script defines the shelf layout and buttons for MeshMaven within Autodesk Maya. It ensures easy access to MeshMaven's functionalities directly from Maya's interface.

## Design Choices

During the development of MeshMaven, several design choices were made to ensure the tool's effectiveness and ease of use:

- **User Interface**: The GUI was designed to be intuitive and user-friendly, allowing users to quickly access the tool's features without needing extensive documentation.
- **Cross-Platform Compatibility**: The tool was developed to be cross-platform compatible, tested on both Windows and Linux. This ensures that users on different operating systems can benefit from MeshMaven.
- **Automation**: The installation process was automated as much as possible to simplify the setup for users. By dragging and dropping the installer into Maya, users can quickly install the tool without manually copying files or modifying settings.
- **Efficiency**: The core functions were optimized for performance to handle large and complex meshes without significant slowdowns.

## Testing and Compatibility

- Tested on Maya 2018.2 on Windows.
- Tested on Maya 2024.2 on both Windows and Linux.
- Developed to be cross-platform compatible.
- **Note**: This tool might work on older versions of Maya, but compatibility cannot be guaranteed.
- **Note**: This tool has not been tested on macOS but should work.

## License

This project is licensed under the GPL-3.0 License. For more details, see the [LICENSE](LICENSE) file.

## Semantic Versioning

MeshMaven uses Semantic Versioning through the use of tags. Each release is tagged with a version number to ensure easy navigation between different versions of the tool. This allows users to track changes and revert to previous versions if necessary.

## Version Control

We recommend managing versions by pushing commits with version numbers rather than creating separate version folders. This approach avoids unnecessary complications and saves space over time. Tags can be created after committing to mark specific releases.

## Development Notes

- MeshMaven was designed to integrate seamlessly with Maya’s existing functionalities, providing additional tools without disrupting the standard workflow.
- The tool prioritizes ease of use and efficient performance, making it accessible for both novice and experienced users.
- Extensive testing was performed to ensure the tool works as expected on different versions of Maya and across various operating systems.

## Contributing

We welcome contributions to MeshMaven! If you have suggestions for new features, improvements, or bug fixes, please open an issue or submit a pull request on GitHub. Your feedback and contributions are invaluable in making MeshMaven better.

## Support

If you find this tool useful and would like to support its development, consider making a donation. Your support is greatly appreciated!

- [Donate via PayPal](https://www.paypal.com/paypalme/utsava00)

Thank you for your support!
