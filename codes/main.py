import sys
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QLineEdit, 
    QMessageBox, QStyle, QDialog, QVBoxLayout
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings
)

TARGET_URL = "http://localhost:3000"

class RestrictedWebPage(QWebEnginePage):
    """تقييد التنقل داخل نطاق localhost:3000 فقط"""
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        url_str = url.toString()
        if isMainFrame:
            allowed = (
                url_str.startswith("http://localhost:3000") or
                url_str.startswith("http://127.0.0.1:3000") or
                url_str.startswith("chrome-devtools://") or
                url_str == "about:blank"
            )
            if not allowed:
                QMessageBox.warning(
                    None, 
                    "وصول محظور", 
                    f"المتصفح مقفول حصراً على localhost:3000\nالرابط المحظور: {url_str}"
                )
                return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)

class DevToolsDialog(QDialog):
    """نافذة أدوات التطوير وفحص العناصر (DevTools)"""
    def __init__(self, target_page, parent=None):
        super().__init__(parent)
        self.setWindowTitle("أدوات التطوير - Developer Tools")
        self.resize(1000, 600)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.dev_view = QWebEngineView()
        target_page.setDevToolsPage(self.dev_view.page())
        layout.addWidget(self.dev_view)

class LocalhostBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Localhost:3000 Dev Environment")
        self.setGeometry(100, 100, 1280, 800)
        self.is_mobile = False

        # إعداد محرك الويب والبروفايل
        self.browser = QWebEngineView()
        self.profile = QWebEngineProfile.defaultProfile()
        self.page = RestrictedWebPage(self.profile, self.browser)
        self.browser.setPage(self.page)
        self.setCentralWidget(self.browser)

        # تفعيل Local Storage وJavaScript
        settings = self.page.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # إنشاء شريط الأدوات مع أيقونات Qt الأصلية
        toolbar = QToolBar("أدوات التحكم")
        toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(toolbar)

        # زر الرجوع
        act_back = QAction(self.style().standardIcon(QStyle.SP_ArrowBack), "رجوع", self)
        act_back.triggered.connect(self.browser.back)
        toolbar.addAction(act_back)

        # زر التقدم
        act_forward = QAction(self.style().standardIcon(QStyle.SP_ArrowForward), "تقدم", self)
        act_forward.triggered.connect(self.browser.forward)
        toolbar.addAction(act_forward)

        # زر إعادة التحميل
        act_reload = QAction(self.style().standardIcon(QStyle.SP_BrowserReload), "تحديث", self)
        act_reload.triggered.connect(self.browser.reload)
        toolbar.addAction(act_reload)

        # زر الصفحة الرئيسية
        act_home = QAction(self.style().standardIcon(QStyle.SP_DirHomeIcon), "الرئيسية", self)
        act_home.triggered.connect(self.go_home)
        toolbar.addAction(act_home)

        toolbar.addSeparator()

        # شريط العنوان (قراءة فقط لمنع كتابة روابط خارجية)
        self.url_bar = QLineEdit()
        self.url_bar.setReadOnly(True)
        self.browser.urlChanged.connect(self.update_url)
        toolbar.addWidget(self.url_bar)

        toolbar.addSeparator()

        # زر Hard Reload (مسح الـ Cache وإعادة التحميل)
        act_hard_reload = QAction(self.style().standardIcon(QStyle.SP_DialogResetButton), "تحديث نقي (Hard Reload)", self)
        act_hard_reload.triggered.connect(self.hard_reload)
        toolbar.addAction(act_hard_reload)

        # زر التبديل بين وضع الهواتف وسطح المكتب
        act_toggle_view = QAction(self.style().standardIcon(QStyle.SP_ComputerIcon), "قياس الشاشة (Mobile/Desktop)", self)
        act_toggle_view.triggered.connect(self.toggle_view_mode)
        toolbar.addAction(act_toggle_view)

        # زر أدوات التطوير (Inspect / Console)
        act_devtools = QAction(self.style().standardIcon(QStyle.SP_FileDialogContentsView), "فحص العناصر (DevTools)", self)
        act_devtools.triggered.connect(self.open_devtools)
        toolbar.addAction(act_devtools)

        # التوجيه إلى localhost:3000 عند الإقلاع
        self.go_home()

    def go_home(self):
        self.browser.setUrl(QUrl(TARGET_URL))

    def update_url(self, qurl):
        self.url_bar.setText(qurl.toString())

    def hard_reload(self):
        self.profile.clearHttpCache()
        self.browser.reload()

    def toggle_view_mode(self):
        if not self.is_mobile:
            self.setFixedSize(375, 812)  # أبعاد هاتف قياسية
            self.is_mobile = True
        else:
            self.setMinimumSize(800, 600)
            self.setMaximumSize(16777215, 16777215)
            self.resize(1280, 800)
            self.is_mobile = False

    def open_devtools(self):
        self.devtools_dialog = DevToolsDialog(self.browser.page(), self)
        self.devtools_dialog.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LocalhostBrowser()
    window.show()
    sys.exit(app.exec_())
