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


import maya.cmds as cmds


class MeshMavenCore:

    def __init__(self):
        pass

    def get_selected_objects(self):
        """
        Returns a list of selected objects in Maya.
        """

        selected_objects = cmds.ls(selection=True, transforms=True)

        if not selected_objects:
            cmds.warning("Please select an object.")
            return
        
        return selected_objects

    def get_selected_components(self):
        """
        Returns a list of selected components (vertices, edges, or faces) in Maya.
        """

        selected_components = cmds.ls(selection=True, flatten=True)
        return selected_components

    def get_open_edges(self):
        """
        Returns a list of all the open edges of a single selected object.
        """

        selected_objects = self.get_selected_objects()
        
        selected_objects = selected_objects[0]

        # Get all edges of the selected object
        edges = cmds.ls(cmds.polyListComponentConversion(
            selected_objects, fromVertex=True, toEdge=True), flatten=True)

        open_edges = []

        # Check each edge for being open
        for edge in edges:
            connected_faces = cmds.polyListComponentConversion(edge, fromEdge=True, toFace=True)
            connected_faces = cmds.ls(connected_faces, flatten=True)

            if len(connected_faces) == 1:
                open_edges.append(edge)

        return open_edges

    def get_vertex_closest_to_axis(self, axis):
        """
        Returns vertex closest to the chosen axis
        """

        components = self.get_selected_components()

        # Make sure the components are of type edge
        edges = cmds.filterExpand(components, selectionMask=32)
        
        # Convert edges to vertices
        vertices = cmds.ls(cmds.polyListComponentConversion(
            edges, fromEdge=True, toVertex=True), flatten=True)

        if not vertices:
            cmds.warning("No vertices found")

        # Initialize variables to store closest vertex and its distance to Y-axis
        closest_vertex = None
        closest_distance = float('inf')  # Initialize with infinity

        if axis == "X":
            mirror_plane = 1
        elif axis == "Y":
            mirror_plane = 2
        elif axis == "Z":
            mirror_plane = 0
        
        for vertex in vertices:
            # Get vertex position
            vertex_pos = cmds.pointPosition(vertex, world=True)
            axis_distance = abs(vertex_pos[mirror_plane])
        
            # Check if this vertex is closer to axis
            if axis_distance < closest_distance:
                closest_distance = axis_distance
                closest_vertex = vertex
        return closest_vertex

    def scale_vertices(self, axis, vertex_pos):
        """
        Scale the vertices based a axis of a particular vertex
        """

        components = self.get_selected_components()

        # Make sure the components are of type edge
        edges = cmds.filterExpand(components, selectionMask=32)

        if not edges:
            cmds.warning("Please select edges")
            return

        # Convert edges to vertices
        vertices = cmds.ls(cmds.polyListComponentConversion(
            edges, fromEdge=True, toVertex=True), flatten=True)

        if not vertices:
            cmds.warning("No vertices found in the selected edges.")
            return
        
        if axis == "X":
            scale_factor = (1e-05, 1, 1)
        elif axis == "Y":
            scale_factor = (1, 1e-05, 1)
        elif axis == "Z":
            scale_factor = (1, 1, 1e-05)
        # Perform relative scaling around  vertex_pos
        cmds.select(vertices)
        cmds.scale(scale_factor[0], scale_factor[1], 
                   scale_factor[2], relative=True, pivot=vertex_pos)

    def set_pivot(self, x, y, z):
        """
        Set pivot of selected objects to given coordinate.
        """
        selected_objects = self.get_selected_objects()

        for obj in selected_objects:
            # Move the scale and rotate pivots to the given coordinate
            cmds.move(x, y, z, obj + ".scalePivot", obj + ".rotatePivot", rotatePivotRelative=True)

    def set_scale_attr(self, obj, axis):
        """
        Scale objects based on axis.
        """

        if axis == "X":
            cmds.setAttr(obj + ".scaleX", (-1))
        elif axis == "Y":
            cmds.setAttr(obj + ".scaleY", (-1))
        elif axis == "Z":
            cmds.setAttr(obj + ".scaleZ", (-1))

    def mirror_object(self, axis):
        """
        Duplicate and scale object in negative direction of axis to 
        create a replica of the object.
        """
        selected_objects = self.get_selected_objects()

        duplicated_objects = []
        for obj in selected_objects:
            duplicated_obj = cmds.duplicate(obj)[0]  # Duplicate and get the first returned object
            self.set_scale_attr(duplicated_obj, axis)
            duplicated_objects.append(duplicated_obj)

        if not duplicated_objects:
            cmds.warning("Failed to duplicate objects.")
        
        return duplicated_objects

    def freeze_transform(self):
        """
        Freeze the transform values of selected objects.
        """

        selected_objects = self.get_selected_objects()
        cmds.makeIdentity(selected_objects, apply=True, translate=True, 
                          rotate=True, scale=True, normal=False, preserveNormals=True)

    def delete_history(self):
        """
        Delete history of selected objects.
        """

        selected_objects = self.get_selected_objects()
        cmds.delete(selected_objects, constructionHistory=True)

    def get_bad_components(self):
        """
        Select faces with more than 4 sides, concave faces, faces with holes, and non-manifold geometry.
        """

        selected_objects = self.get_selected_objects()

        # Initialize list to hold all problematic faces
        bad_components = []

        # Select faces with more than 4 sides
        cmds.select(selected_objects)
        cmds.polySelectConstraint(mode=3, type=8, size=3)
        faces_with_more_than_4_sides = self.get_selected_components()
        cmds.polySelectConstraint(disable=True)
    
        if faces_with_more_than_4_sides:
            bad_components.extend(faces_with_more_than_4_sides)
        
        # Select concave faces
        cmds.select(selected_objects, replace=True)
        cmds.polySelectConstraint(mode=3, type=8, convexity=1)
        concave_faces = self.get_selected_components()
        cmds.polySelectConstraint(disable=True)

        if concave_faces:
            bad_components.extend(concave_faces)

        # Select faces with holes
        cmds.select(selected_objects, replace=True)
        cmds.polySelectConstraint(mode=3, type=8, holes=1)
        faces_with_holes = self.get_selected_components()
        cmds.polySelectConstraint(disable=True)

        if faces_with_holes:
            bad_components.extend(faces_with_holes)

        # Select vertices of non-manifold geometry
        cmds.select(selected_objects, replace=True)
        non_manifold_vertices = cmds.polyInfo(nonManifoldVertices=True)

        if non_manifold_vertices:
            bad_components.extend(non_manifold_vertices)

        return bad_components

    def merge_vertex(self):
        """
        Merges all the selected vertices.
        """
        components = self.get_selected_components()

        # Make sure the components are of type vertex
        vertices = cmds.filterExpand(components, selectionMask=31)

        if not vertices:
            cmds.error("No vertices to merge.")
            return
        
        cmds.polyMergeVertex(vertices, distance=0.0001, alwaysMergeTwoVertices=True)

    def soften_harden(self):
        """
        Based on selection automatically softens and hardens all the edges or selected edges of an object.
        """

        selected_objects = self.get_selected_objects()
        components = self.get_selected_components()

        # Make sure the components are of type edge
        edges = cmds.filterExpand(components, selectionMask=32)

        if not selected_objects and not edges:
            cmds.warning("No object or edge selected.")
            return
        
        cmds.polySoftEdge(a=30, constructionHistory=False)

    def soften_edge(self):
        """
        Based on selection softens all the edges or selected edges of an object.
        """
        selected_objects = self.get_selected_objects()
        components = self.get_selected_components()

        # Make sure the components are of type edge
        edges = cmds.filterExpand(components, selectionMask=32)

        if not selected_objects and not edges:
            cmds.warning("No object or edge selected.")
            return
        
        cmds.polySoftEdge(a=180, constructionHistory=False)

    def harden_edge(self):
        """
        Based on selection hardens all the edges or selected edges of an object.
        """
        selected_objects = self.get_selected_objects()
        components = self.get_selected_components()

        # Make sure the components are of type edge
        edges = cmds.filterExpand(components, selectionMask=32)

        if not selected_objects and not edges:
            cmds.warning("No object or edge selected.")
            return
        
        cmds.polySoftEdge(a=0, constructionHistory=False)

    def combine(self):
        """
        Combine selected objects.
        """
        selected_objects = self.get_selected_objects()

        if len(selected_objects) < 2:
            cmds.warning("Please select at least two objects to combine.")
            return
        
        cmds.polyUnite(selected_objects, constructionHistory=False)

    def separate(self):
        """
        Separate selected objects.
        """
        selected_objects = self.get_selected_objects()
        
        cmds.polySeparate(selected_objects, constructionHistory=False)

    def duplicate(self, axis):
        """
        duplicate combine and merge objects based on the selected axis
        """

        # Get all the selected objects
        selected_objects = self.get_selected_objects()

        for obj in selected_objects:

            cmds.select(obj, replace=True)

            # Find open edges and select it for further usage
            open_edges = self.get_open_edges()
            cmds.select(open_edges, replace=True)

            # Find closest vertex based on user input
            closest_vertex = self.get_vertex_closest_to_axis(axis)

            # Get coordinate of vertex closest to the axis
            vtx_coordinate = cmds.pointPosition(closest_vertex, world=True)

            # Use closest_vertex as vertex_pos for the input of scale_vertices method
            self.scale_vertices(axis, vtx_coordinate)

            # Get the parent object of the open edges
            shape_node = cmds.listRelatives(open_edges[0], parent=True, fullPath=True)

            if shape_node:
                parent_object = cmds.listRelatives(shape_node, parent=True, fullPath=True)

            # Select parent object
            if not parent_object:
                cmds.warning("No parent object found.")

            cmds.select(parent_object[0], replace=True)

            # Freeze transform values of the object
            self.freeze_transform()

            # Set pivot of the object to the vertex closest to the axis
            self.set_pivot(vtx_coordinate[0], vtx_coordinate[1], vtx_coordinate[2])

            # Mirror, combine then delete history
            mirrored_objects = self.mirror_object(axis)

            # Select old object and mirrored object
            cmds.select(parent_object, mirrored_objects, replace=True)
            self.combine()

            # Get a list of new open edges and vertices
            new_open_edges = self.get_open_edges()
            new_vertices = cmds.ls(cmds.polyListComponentConversion(
                new_open_edges, fromEdge=True, toVertex=True), flatten=True)

            # Select new open edge vertices and merge them
            cmds.select(new_vertices, replace=True)
            self.merge_vertex()
            merged_vertices = self.get_selected_components()
            new_shape_node = cmds.listRelatives(merged_vertices[0], parent=True, fullPath=True)
            new_object = cmds.listRelatives(new_shape_node, parent=True, fullPath=True)
            cmds.select(new_object)
            self.delete_history()
            cmds.select(clear=True)

    def undo(self):
        """
        Undo all the steps done in duplicate method.
        """

        UNDO_COUNT = 9
        for _ in range(UNDO_COUNT):
            cmds.undo()

    def bridge(self, division):
        """
        Bridge equal number of selected edges.
        """

        components = self.get_selected_components()
        selected_edges = cmds.filterExpand(components, selectionMask=32)

        if not selected_edges or len(selected_edges) < 2:
            cmds.warning("Please select at least two edges to bridge.")
            return
        
        cmds.polyBridgeEdge(constructionHistory=False, divisions=division, smoothingAngle=30)

    def union(self):
        """
        Union of selected objects.
        """

        selected_objects = self.get_selected_objects()
        cmds.polyBoolOp(selected_objects, operation=1, constructionHistory=False)

    def difference(self):
        """
        Difference of selected objects.
        """

        selected_objects = self.get_selected_objects()
        cmds.polyBoolOp(selected_objects, operation=2, constructionHistory=False)

    def intersection(self):
        """
        Intersection of selected objects.
        """

        selected_objects = self.get_selected_objects()
        cmds.polyBoolOp(selected_objects, operation=3, constructionHistory=False)

    def check(self):
        """
        Freeze transform values, set pivot to origin and delete history of the selected objects
        and select faces with more than 4 sides, concave faces, faces with holes, and non-manifold geometry.
        """

        # Freeze transform values, set pivot to origin and delete history of the selected objects
        self.freeze_transform()
        self.set_pivot(0, 0, 0)
        self.delete_history()
        cmds.select(self.get_bad_components(), replace=True)  # select all the components with issue

    def export(self):
        """
        Export selected object using default dialog of Maya.
        """

        self.get_selected_objects()

        # Use Maya's default Export Selection dialog
        cmds.ExportSelection()