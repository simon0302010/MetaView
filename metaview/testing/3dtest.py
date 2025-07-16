import sys

import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

# pyqtgraph, pyopengl
from pyqtgraph.opengl import GLMeshItem, GLViewWidget, MeshData

# numpy-stl
from stl import mesh


class NonInteractiveGLViewWidget(GLViewWidget):
    def mousePressEvent(self, ev):
        pass

    def mouseMoveEvent(self, ev):
        pass

    def mouseReleaseEvent(self, ev):
        pass

    def wheelEvent(self, ev):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = NonInteractiveGLViewWidget()
    try:
        stl_mesh = mesh.Mesh.from_file(sys.argv[1])
    except IndexError:
        print("Please provide the path to a 3D model.")
        sys.exit(1)

    points = stl_mesh.points.reshape(-1, 3)
    faces = np.arange(points.shape[0]).reshape(-1, 3)

    # Center the object
    center = points.mean(axis=0)
    points -= center

    mesh_data = MeshData(vertexes=points, faces=faces)
    mesh_item = GLMeshItem(
        meshdata=mesh_data,
        smooth=True,
        drawFaces=True,
        drawEdges=False,
        color=(0.8, 0.8, 0.8, 1),
        shader="shaded",
    )
    view.addItem(mesh_item)

    # make whole object visible
    max_extent = np.abs(points).max()
    view.setCameraPosition(distance=max_extent * 3)

    # spin it
    def spin():
        mesh_item.rotate(1, 0, 0, 1)

    timer = QTimer()
    timer.timeout.connect(spin)
    timer.start(30)

    view.show()
    app.exec()
