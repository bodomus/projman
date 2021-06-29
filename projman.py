import hou
import os
from PySide2 import QtWidgets, QtUiTools


class ProjectManager(QtWidgets.QWidget):
    def __init__(self):
        super(ProjectManager, self).__init__()
        self.job = hou.getenv("JOB")
        self.createInterface()

        loader = QtUiTools.QUiLoader()
        p = self.getUiPath()
        self.ui = loader.load(r'c:/Houdini/18.0.348/houdini/python2.7libs/projman/projman.ui')
        self.clsScene = self.ui.findChild(QtWidgets.QPushButton, "btnClearScene")
        self.clsScene.clicked.connect(self.clearScene)
        self.setPrj = self.ui.findChild(QtWidgets.QPushButton, "btnSetProject")
        self.setPrj.clicked.connect(self.setProject)
        self.lblProjName = self.ui.findChild(QtWidgets.QLabel, "lblProjectName")
        self.lblProjName.setText('')
        self.lblProjPath = self.ui.findChild(QtWidgets.QLabel, "lblProjectPath")
        self.lblProjPath.setText('')

        self.list = self.ui.findChild(QtWidgets.QListWidget, "listWidget")
        self.list.doubleClicked.connect(self.loadHIPFile)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.setLayout(self.layout)

    def loadHIPFile(self, item):
        job = hou.getenv('JOB')
        j = os.path.join(job, item.data())
        hou.hipFile.load(j)

    def clearScene(self):
        hou.hipFile.clear()

    def setProject(self):
        job = hou.ui.selectFile(title='Select directory', file_type=hou.fileType.Directory)
        hou.hscript("setenv JOB=" + job)
        self.lblProjName.setText(job.split('/')[-2])
        self.lblProjPath.setText(hou.expandString(job))
        self.createInterface()

    def createInterface(self):
        # self.list.clear()
        job = hou.getenv('JOB')
        # job=job.replace('/','\\')
        try:
            for file in os.listdir(job):
                if file.endswith('.hip'):
                    self.list.addItem(file)
        except:
            hou.ui.displayMessage("Oops!  That was no valid path.  Try change project directory...")

        return None

    def getUiPath(self):
        return hou.getenv('HFS') + '/houdini/python2.7libs/projman/'
