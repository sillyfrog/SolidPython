#! /usr/bin/env python3
import unittest
import re

from solid import OpenSCADObject, scad_render
from solid.utils import extrude_along_path
from euclid3 import Point2, Point3

from typing import Union

tri = [Point3(0, 0, 0), Point3(10, 0, 0), Point3(0, 10, 0)]

class TestExtrudeAlongPath(unittest.TestCase):
    # Test cases will be dynamically added to this instance
    # using the test case arrays above
    def assertEqualNoWhitespace(self, a, b):
        remove_whitespace = lambda s: re.subn(r'[\s\n]','', s)[0]
        self.assertEqual(remove_whitespace(a), remove_whitespace(b))

    def assertEqualOpenScadObject(self, expected:str, actual:Union[OpenSCADObject, str]):
        if isinstance(actual, OpenSCADObject):
            act = scad_render(actual)
        elif isinstance(actual, str):
            act = actual
        self.assertEqualNoWhitespace(expected, act)

    def test_extrude_along_path(self):
        path = [[0, 0, 0], [0, 20, 0]]
        # basic test
        actual = extrude_along_path(tri, path)
        expected = 'polyhedron(faces = [[0, 3, 1], [1, 3, 4], [1, 4, 2], [2, 4, 5], [2, 5, 0], [0, 5, 3], [6, 0, 1], [6, 1, 2], [6, 2, 0], [7, 3, 4], [7, 4, 5], [7, 5, 3]], points = [[0.0000000000, 0.0000000000, 0.0000000000], [10.0000000000, 0.0000000000, 0.0000000000], [0.0000000000, 0.0000000000, 10.0000000000], [0.0000000000, 20.0000000000, 0.0000000000], [10.0000000000, 20.0000000000, 0.0000000000], [0.0000000000, 20.0000000000, 10.0000000000], [3.3333333333, 0.0000000000, 3.3333333333], [3.3333333333, 20.0000000000, 3.3333333333]]);'
        self.assertEqualOpenScadObject(expected, actual)

    def test_extrude_along_path_vertical(self):
        # make sure we still look good extruding along z axis; gimbal lock can mess us up
        vert_path = [[0, 0, 0], [0, 0, 20]]
        actual = extrude_along_path(tri, vert_path)
        expected = 'polyhedron(faces=[[0,3,1],[1,3,4],[1,4,2],[2,4,5],[2,5,0],[0,5,3],[6,0,1],[6,1,2],[6,2,0],[7,3,4],[7,4,5],[7,5,3]],points=[[0.0000000000,0.0000000000,0.0000000000],[-10.0000000000,0.0000000000,0.0000000000],[0.0000000000,10.0000000000,0.0000000000],[0.0000000000,0.0000000000,20.0000000000],[-10.0000000000,0.0000000000,20.0000000000],[0.0000000000,10.0000000000,20.0000000000],[-3.3333333333,3.3333333333,0.0000000000],[-3.3333333333,3.3333333333,20.0000000000]]);'
        self.assertEqualOpenScadObject(expected, actual)

    def test_extrude_along_path_1d_scale(self):
        # verify that we can apply scalar scaling
        path = [[0, 0, 0], [0, 20, 0]]
        scales_1d = [1.5, 0.5]
        actual = extrude_along_path(tri, path, scales=scales_1d)
        expected = 'polyhedron(faces=[[0,3,1],[1,3,4],[1,4,2],[2,4,5],[2,5,0],[0,5,3],[6,0,1],[6,1,2],[6,2,0],[7,3,4],[7,4,5],[7,5,3]],points=[[0.0000000000,0.0000000000,0.0000000000],[15.0000000000,0.0000000000,0.0000000000],[0.0000000000,0.0000000000,15.0000000000],[0.0000000000,20.0000000000,0.0000000000],[5.0000000000,20.0000000000,0.0000000000],[0.0000000000,20.0000000000,5.0000000000],[5.0000000000,0.0000000000,5.0000000000],[1.6666666667,20.0000000000,1.6666666667]]);'
        self.assertEqualOpenScadObject(expected, actual)

    def test_extrude_along_path_2d_scale(self):
        # verify that we can apply differential x & y scaling
        path = [[0, 0, 0], [0, 20, 0], [0, 40, 0]]
        scales_2d = [Point2(1,1), Point2(0.5, 1.5), Point2(1.5, 0.5), ]
        actual = extrude_along_path(tri, path, scales=scales_2d)
        expected = 'polyhedron(faces=[[0,3,1],[1,3,4],[1,4,2],[2,4,5],[2,5,0],[0,5,3],[3,6,4],[4,6,7],[4,7,5],[5,7,8],[5,8,3],[3,8,6],[9,0,1],[9,1,2],[9,2,0],[10,6,7],[10,7,8],[10,8,6]],points=[[0.0000000000,0.0000000000,0.0000000000],[10.0000000000,0.0000000000,0.0000000000],[0.0000000000,0.0000000000,10.0000000000],[0.0000000000,20.0000000000,0.0000000000],[5.0000000000,20.0000000000,0.0000000000],[0.0000000000,20.0000000000,15.0000000000],[0.0000000000,40.0000000000,0.0000000000],[15.0000000000,40.0000000000,0.0000000000],[0.0000000000,40.0000000000,5.0000000000],[3.3333333333,0.0000000000,3.3333333333],[5.0000000000,40.0000000000,1.6666666667]]);'
        self.assertEqualOpenScadObject(expected, actual)

    def test_extrude_along_path_2d_scale_list_input(self):
        # verify that we can apply differential x & y scaling
        path = [[0, 0, 0], [0, 20, 0], [0, 40, 0]]
        scales_2d = [(1,1), (0.5, 1.5), (1.5, 0.5), ]
        actual = extrude_along_path(tri, path, scales=scales_2d)
        expected = 'polyhedron(faces=[[0,3,1],[1,3,4],[1,4,2],[2,4,5],[2,5,0],[0,5,3],[3,6,4],[4,6,7],[4,7,5],[5,7,8],[5,8,3],[3,8,6],[9,0,1],[9,1,2],[9,2,0],[10,6,7],[10,7,8],[10,8,6]],points=[[0.0000000000,0.0000000000,0.0000000000],[10.0000000000,0.0000000000,0.0000000000],[0.0000000000,0.0000000000,10.0000000000],[0.0000000000,20.0000000000,0.0000000000],[5.0000000000,20.0000000000,0.0000000000],[0.0000000000,20.0000000000,15.0000000000],[0.0000000000,40.0000000000,0.0000000000],[15.0000000000,40.0000000000,0.0000000000],[0.0000000000,40.0000000000,5.0000000000],[3.3333333333,0.0000000000,3.3333333333],[5.0000000000,40.0000000000,1.6666666667]]);'
        self.assertEqualOpenScadObject(expected, actual)

    def test_extrude_along_path_end_caps(self):
        path = [[0, 0, 0], [0, 20, 0]]
        actual = scad_render(extrude_along_path(tri, path, connect_ends=False))
        expected = 'polyhedron(faces = [[0, 3, 1], [1, 3, 4], [1, 4, 2], [2, 4, 5], [2, 5, 0], [0, 5, 3], [6, 0, 1], [6, 1, 2], [6, 2, 0], [7, 3, 4], [7, 4, 5], [7, 5, 3]], points = [[0.0000000000, 0.0000000000, 0.0000000000], [10.0000000000, 0.0000000000, 0.0000000000], [0.0000000000, 0.0000000000, 10.0000000000], [0.0000000000, 20.0000000000, 0.0000000000], [10.0000000000, 20.0000000000, 0.0000000000], [0.0000000000, 20.0000000000, 10.0000000000], [3.3333333333, 0.0000000000, 3.3333333333], [3.3333333333, 20.0000000000, 3.3333333333]]);'
        self.assertEqualNoWhitespace(expected, actual)

    def test_extrude_along_path_connect_ends(self):
        path = [[0, 0, 0], [20, 0, 0], [20,20,0], [0,20, 0]]
        actual = extrude_along_path(tri, path, connect_ends=True)
        expected = 'polyhedron(faces=[[0,3,1],[1,3,4],[1,4,2],[2,4,5],[2,5,0],[0,5,3],[3,6,4],[4,6,7],[4,7,5],[5,7,8],[5,8,3],[3,8,6],[6,9,7],[7,9,10],[7,10,8],[8,10,11],[8,11,6],[6,11,9],[0,9,1],[1,9,10],[1,10,2],[2,10,11],[2,11,0],[0,11,9]],points=[[0.0000000000,0.0000000000,0.0000000000],[-7.0710678119,-7.0710678119,0.0000000000],[0.0000000000,0.0000000000,10.0000000000],[20.0000000000,0.0000000000,0.0000000000],[27.0710678119,-7.0710678119,0.0000000000],[20.0000000000,0.0000000000,10.0000000000],[20.0000000000,20.0000000000,0.0000000000],[27.0710678119,27.0710678119,0.0000000000],[20.0000000000,20.0000000000,10.0000000000],[0.0000000000,20.0000000000,0.0000000000],[-7.0710678119,27.0710678119,0.0000000000],[0.0000000000,20.0000000000,10.0000000000]]);'
        self.assertEqualOpenScadObject(expected, actual)

    def test_extrude_along_path_rotations(self):
        # confirm we can rotate for each point in path
        path = [[0,0,0], [20, 0,0 ]]
        rotations = [-45, 45]
        actual = extrude_along_path(tri, path, rotations=rotations)
        expected = 'polyhedron(faces=[[0,3,1],[1,3,4],[1,4,2],[2,4,5],[2,5,0],[0,5,3],[6,0,1],[6,1,2],[6,2,0],[7,3,4],[7,4,5],[7,5,3]],points=[[0.0000000000,0.0000000000,0.0000000000],[0.0000000000,-7.0710678119,-7.0710678119],[0.0000000000,-7.0710678119,7.0710678119],[20.0000000000,0.0000000000,0.0000000000],[20.0000000000,-7.0710678119,7.0710678119],[20.0000000000,7.0710678119,7.0710678119],[0.0000000000,-4.7140452079,0.0000000000],[20.0000000000,-0.0000000000,4.7140452079]]);'
        self.assertEqualOpenScadObject(expected, actual)

        # confirm we can rotate with a single supplied value
        path = [[0,0,0], [20, 0,0 ]]
        rotations = [45]
        actual = extrude_along_path(tri, path, rotations=rotations)
        expected = 'polyhedron(faces=[[0,3,1],[1,3,4],[1,4,2],[2,4,5],[2,5,0],[0,5,3],[6,0,1],[6,1,2],[6,2,0],[7,3,4],[7,4,5],[7,5,3]],points=[[0.0000000000,0.0000000000,0.0000000000],[0.0000000000,-10.0000000000,0.0000000000],[0.0000000000,0.0000000000,10.0000000000],[20.0000000000,0.0000000000,0.0000000000],[20.0000000000,-7.0710678119,7.0710678119],[20.0000000000,7.0710678119,7.0710678119],[0.0000000000,-3.3333333333,3.3333333333],[20.0000000000,-0.0000000000,4.7140452079]]);'
        self.assertEqualOpenScadObject(expected, actual)        

    def test_extrude_along_path_transforms(self):
        path = [[0,0,0], [20, 0,0 ]]
        # scale points by a factor of 2 & then 1/2
        # Make sure we can take a transform function for each point in path
        transforms = [lambda p, path, loop: 2*p, lambda p, path, loop: 0.5*p]
        actual = extrude_along_path(tri, path, transforms=transforms)
        expected = 'polyhedron(faces=[[0,3,1],[1,3,4],[1,4,2],[2,4,5],[2,5,0],[0,5,3],[6,0,1],[6,1,2],[6,2,0],[7,3,4],[7,4,5],[7,5,3]],points=[[0.0000000000,0.0000000000,0.0000000000],[0.0000000000,-20.0000000000,0.0000000000],[0.0000000000,0.0000000000,20.0000000000],[20.0000000000,0.0000000000,0.0000000000],[20.0000000000,-5.0000000000,0.0000000000],[20.0000000000,0.0000000000,5.0000000000],[0.0000000000,-6.6666666667,6.6666666667],[20.0000000000,-1.6666666667,1.6666666667]]);'
        self.assertEqualOpenScadObject(expected, actual)

        # Make sure we can take a single transform function for all points
        transforms = [lambda p, path, loop: 2*p]
        actual = extrude_along_path(tri, path, transforms=transforms)
        expected = 'polyhedron(faces = [[0, 3, 1], [1, 3, 4], [1, 4, 2], [2, 4, 5], [2, 5, 0], [0, 5, 3], [6, 0, 1], [6, 1, 2], [6, 2, 0], [7, 3, 4], [7, 4, 5], [7, 5, 3]], points = [[0.0000000000, 0.0000000000, 0.0000000000], [0.0000000000, -20.0000000000, 0.0000000000], [0.0000000000, 0.0000000000, 20.0000000000], [20.0000000000, 0.0000000000, 0.0000000000], [20.0000000000, -20.0000000000, 0.0000000000], [20.0000000000, 0.0000000000, 20.0000000000], [0.0000000000, -6.6666666667, 6.6666666667], [20.0000000000, -6.6666666667, 6.6666666667]]);'
        self.assertEqualOpenScadObject(expected, actual)

    def test_extrude_along_path_numpy(self):
        try: 
            import numpy as np # type: ignore
        except ImportError:
            return

        N = 3
        thetas=np.linspace(0,np.pi,N) 
        path=list(zip(3*np.sin(thetas),3*np.cos(thetas),thetas)) 
        profile=list(zip(np.sin(thetas),np.cos(thetas), [0]*len(thetas))) 
        scalepts=list(np.linspace(1,.1,N))   

        # in earlier code, this would have thrown an exception
        a = extrude_along_path(shape_pts=profile, path_pts=path, scales=scalepts)
 
if __name__ == '__main__':
    unittest.main()
