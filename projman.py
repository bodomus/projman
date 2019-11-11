import hou
import os
from PySide2 import QtWidgets, QtUiTools

class ProjectManager (QtWidgets.QWidget):
    def __init__(self):
        super(ProjectManager, self).__init__()
        self.job = hou.getenv("JOB")
        self.createInterface()

        loader = QtUiTools.QUiLoader()
        p = self.getUiPath()
        self.ui = loader.load(r'c:/Houdini/17.5.327/houdini/python2.7libs/projman/projman.ui')
        self.clearScene = self.ui.findChild(QtWidgets.QPushButton, "btnClearScene")
        self.clearScene.clicked.connect(self.clearScene)
        self.setProject = self.ui.findChild(QtWidgets.QPushButton, "btnSetProject")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.setLayout(self.layout)

    def loadHIPFile(self, item):
        print (item.data())
        hou.hipFile.load(os.path.join(self.job, item.data()))

    def clearScene(self):
        hou.hipFile.clear()

    def createInterface(self):
        return None
    def getUiPath(self):
        return hou.getenv('HFS')+'/houdini/python2.7libs/projman/'

    def createBoundaries(self):
        geo = hou.pwd().geometry()
        pt0 = geo.createPoint()
        pt0.setPosition(hou.Vector3(1, 0, 0))
        pt1 = geo.createPoint()
        pt1.setPosition(hou.Vector3(0, 1, 0))
        pt2 = geo.createPoint()
        pt2.setPosition(hou.Vector3(0, 0, 1))
        poly = geo.createPolygon()
        poly.addVertex(pt0);
        poly.addVertex(pt1);
        poly.addVertex(pt2);