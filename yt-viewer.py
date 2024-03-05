import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import QUrl, Qt, QPoint, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QIcon



class YouTubeViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.oldPos = self.pos()
        self.isResizing = False
        self.edgeMargin = 5 

    from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle('YouTube Video Viewer')
        self.setGeometry(300, 300, 800, 600)
        self.topLayout = QHBoxLayout()
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        
        # Icon
        self.iconButton = QPushButton()  
        self.iconButton.setIcon(QIcon('icons/yticon.png'))  
        self.iconButton.setIconSize(QSize(64, 64))  
        self.iconButton.setFixedSize(70, 70)  
        self.iconButton.setStyleSheet("background-color: transparent; border: none;")  

        # Buttons Min, Close, Cast
        self.minimizeButton = QPushButton('_')
        self.closeButton = QPushButton('X')
        self.castButton = QPushButton()  # Erstellen des Cast-Buttons ohne Text
        self.castButton.setIcon(QIcon('icons/Casticon.png'))  # Setzen des Icons für den Cast-Button

        # Button-Size
        self.minimizeButton.setFixedSize(40, 40)
        self.closeButton.setFixedSize(40, 40)
        self.castButton.setFixedSize(40, 40)
        
        self.topLayout.addWidget(self.iconButton)
        
        leftSpacer = QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.topLayout.addSpacerItem(leftSpacer)

        # Spacer 
        spacer = QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.topLayout.addSpacerItem(spacer)

        # Layout
        self.topLayout.addWidget(self.minimizeButton)
        self.topLayout.addWidget(self.closeButton)
        self.topLayout.addWidget(self.castButton)

        # Button-Connection
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.closeButton.clicked.connect(self.close)
        self.castButton.clicked.connect(self.castYoutube)

        # Main-Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)
        self.layout.addLayout(self.topLayout)

        # URL-Enter
        self.url_line_edit = QLineEdit(self)
        self.url_line_edit.setPlaceholderText('YouTube-URL:')
        self.url_line_edit.returnPressed.connect(self.load_url)
        self.layout.addWidget(self.url_line_edit)

        # WebView
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)

        # Layout Widget
        self.setLayout(self.layout)
        self.setStyleSheet("QWidget { border: 1px solid black; }")






    def load_url(self):
        url = self.url_line_edit.text()
        if url:
            video_id = url.split('watch?v=')[-1]
            embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&fs=1"
            self.browser.setUrl(QUrl(embed_url))
            self.url_line_edit.setVisible(False)

    def castYoutube(self):        
        profile = QWebEngineProfile("YouTubeProfile", self)
        profile.setHttpUserAgent('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36; Youtube; Tizen 4.0')
        self.browser.setPage(QWebEnginePage(profile, self.browser))
        self.browser.setUrl(QUrl('http://youtube.com/tv'))
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        if event.pos().x() > self.width() - self.edgeMargin and event.pos().y() > self.height() - self.edgeMargin:
            self.isResizing = True

    def mouseMoveEvent(self, event):
        if self.isResizing:
            newWidth = max(self.width() + (event.globalX() - self.oldPos.x()), self.minimumWidth())
            newHeight = max(self.height() + (event.globalY() - self.oldPos.y()), self.minimumHeight())
            self.resize(newWidth, newHeight)
            self.oldPos = event.globalPos()
        else:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.isResizing = False

    def enterEvent(self, event):        
        self.minimizeButton.setVisible(True)
        self.closeButton.setVisible(True)
        self.castButton.setVisible(True)  
        self.url_line_edit.setVisible(True) 
        self.iconButton.setVisible(True)  
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.minimizeButton.setStyleSheet("QPushButton { background-color: #444444; color: white; border: 2px solid #555555; }"
                                          "QPushButton:hover { background-color: #666666; }"
                                          "QPushButton:pressed { background-color: #888888; }")
        self.closeButton.setStyleSheet("QPushButton { background-color: red; color: white; border: 2px solid #aa0000; }"
                                       "QPushButton:hover { background-color: #cc0000; }"
                                       "QPushButton:pressed { background-color: #ff0000; }")

    def leaveEvent(self, event):        
        self.minimizeButton.setVisible(False)
        self.closeButton.setVisible(False)
        self.castButton.setVisible(False)
        self.url_line_edit.setVisible(False)  
        self.iconButton.setVisible(False)  
        self.layout.setContentsMargins(0, 0, 0, 0)
    

def main():
    app = QApplication(sys.argv)
    viewer = YouTubeViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
