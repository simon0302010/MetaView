import sys
import numpy as np
from PyQt5 import QtWidgets
from vispy import scene
from vispy.geometry import create_sphere
from vispy.visuals.filters import TextureFilter
import imageio.v2 as imageio
from urllib.request import urlretrieve
import os


class SimpleEarth(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Earth")
        self.resize(800, 600)

        # create canvas
        self.canvas = scene.SceneCanvas(bgcolor="black")
        view = self.canvas.central_widget.add_view()
        view.camera = "arcball"
        view.camera.distance = 3.0

        # download texture
        texture_path = "earth.jpg"
        if not os.path.exists(texture_path):
            url = (
                "https://www.solarsystemscope.com/textures/download/2k_earth_daymap.jpg"
            )
            urlretrieve(url, texture_path)

        # load texture
        earth_texture = np.flipud(imageio.imread(texture_path))

        # create earth
        sphere = create_sphere(rows=128, cols=128, radius=1.0)
        vertices = sphere.get_vertices()
        faces = sphere.get_faces()

        # gen texcoord
        vertices, faces, texcoords = self.generate_sphere_texcoords(vertices, faces)

        # create mesh
        mesh = scene.visuals.Mesh(vertices=vertices, faces=faces, color="white")
        mesh.attach(TextureFilter(earth_texture, texcoords=texcoords))

        # rotate
        mesh.transform = scene.transforms.MatrixTransform()
        mesh.transform.rotate(270, (1, 0, 0))
        mesh.transform.rotate(90, (0, 0, 1))
        view.add(mesh)

        # add marker
        lat, lon = 42.360278, -71.057778
        lat_rad, lon_rad = np.radians(lat), np.radians(lon)
        # use same coordinates as texture mapping
        x = 1.02 * np.cos(lat_rad) * (-np.cos(lon_rad))
        y = -1.02 * np.sin(lat_rad)
        z = 1.02 * np.cos(lat_rad) * (-np.sin(lon_rad))

        marker = scene.visuals.Markers(
            pos=np.array([[x, y, z]]), size=10, face_color="red"
        )
        # apply same transform as earth mesh
        marker.transform = scene.transforms.MatrixTransform()
        marker.transform.rotate(270, (1, 0, 0))
        marker.transform.rotate(90, (0, 0, 1))
        marker.transform = scene.transforms.MatrixTransform()
        marker.transform.rotate(270, (1, 0, 0))
        marker.transform.rotate(90, (0, 0, 1))
        view.add(marker)

        self.setCentralWidget(self.canvas.native)

    def generate_sphere_texcoords(self, vertices, faces):
        """Generate texture coordinates for a sphere with seam fixing."""
        # calc texcoords
        r = np.linalg.norm(vertices, axis=1, keepdims=True)
        r[r == 0] = 1.0
        norm = vertices / r
        u = 0.5 + np.arctan2(-norm[:, 2], -norm[:, 0]) / (2 * np.pi)
        v = 0.5 - np.arcsin(norm[:, 1]) / np.pi
        texcoords = np.column_stack([u, v])

        # fix seam
        new_vertices = vertices.copy()
        new_texcoords = texcoords.copy()
        new_faces = faces.copy()

        seam_faces = []
        for i, face in enumerate(faces):
            face_u = texcoords[face, 0]
            if np.max(face_u) - np.min(face_u) > 0.5:
                seam_faces.append(i)

        for face_idx in seam_faces:
            face = new_faces[face_idx]
            face_u = new_texcoords[face, 0]
            for j in range(3):
                if face_u[j] < 0.5:
                    # create vertex
                    new_vertex_idx = len(new_vertices)
                    new_vertices = np.vstack((new_vertices, vertices[face[j]]))
                    # add texcoord
                    new_tex = texcoords[face[j]].copy()
                    new_tex[0] += 1.0
                    new_texcoords = np.vstack((new_texcoords, new_tex))
                    # update face
                    new_faces[face_idx, j] = new_vertex_idx

        return new_vertices, new_faces, new_texcoords


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SimpleEarth()
    window.show()
    sys.exit(app.exec_())
