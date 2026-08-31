import sys
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QLineEdit, 
    QMessageBox, QStyle, QDialog, QVBoxLayout, QTabWidget,
    QFileDialog, QToolButton, QMenu
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings
)

DEFAULT_URL = "http://localhost:3000"
MOBILE_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"

# تصميم واجهة مستخدم داكنة (Dark Theme QSS)
DARK_STYLE = """
QMainWindow {
    background-color: #1e1e2e;
}
QToolBar {
    background-color: #181825;
    border-bottom: 1px solid #313244;
    spacing: 5px;
    padding: 5px;
}
QToolButton {
    background-color: transparent;
    color: #cdd6f4;
    border-radius: 4px;
    padding: 5px;
}
QToolButton:hover {
    background-color: #313244;
}
QToolButton:pressed {
    background-color: #45475a;
}
QLineEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
    selection-background-color: #89b4fa;
}
QLineEdit:focus {
    border: 1px solid #89b4fa;
}
QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    background-color: #181825;
    color: #a6adc8;
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    min-width: 120px;
    max-width: 200px;
}
QTabBar::tab:selected {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border-bottom: 2px solid #89b4fa;
}
QTabBar::tab:hover {
    background-color: #313244;
}
QTabBar::close-button {
    subcontrol-position: right;
    margin: 2px;
}
"""

class CustomWebPage(QWebEnginePage):
    """تخصيص الصفحة لفتح الروابط التي تطلب نافذة جديدة داخل تبويب جديد"""
    def __init__(self, profile, parent=None, browser_window=None):
        super().__init__(profile, parent)
        self.browser_window = browser_window

    def createWindow(self, _type):
        if self.browser_window:
            return self.browser_window.add_new_tab().page()
        return super().createWindow(_type)

class DevToolsDialog(QDialog):
    """نافذة أدوات التطوير وفحص العناصر (DevTools)"""
    def __init__(self, target_page, parent=None):
        super().__init__(parent)
        self.setWindowTitle("أدوات التطوير - DevTools")
        self.resize(1000, 600)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.dev_view = QWebEngineView()
        target_page.setDevToolsPage(self.dev_view.page())
        layout.addWidget(self.dev_view)

class LocalhostBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevBrowser Engine")
        self.setGeometry(100, 100, 1280, 850)
        self.setStyleSheet(DARK_STYLE)
        
        self.is_mobile = False

        # إعداد بروفايل الويب العام واسترجاع User-Agent الصحيح
        self.profile = QWebEngineProfile.defaultProfile()
        self.default_user_agent = self.profile.httpUserAgent()

        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # إنشاء نظام التبويبات (Tabs)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.tabs)

        # زر إضافة تبويب جديد
        add_tab_btn = QToolButton()
        add_tab_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        add_tab_btn.setToolTip("تبويب جديد")
        add_tab_btn.clicked.connect(lambda: self.add_new_tab())
        self.tabs.setCornerWidget(add_tab_btn, Qt.TopLeftCorner)

        # إنشاء شريط الأدوات
        self.create_toolbar()

        # فتح التبويب الأول تلقائياً
        self.add_new_tab(QUrl(DEFAULT_URL), "Localhost:3000")

    def create_toolbar(self):
        toolbar = QToolBar("أدوات التحكم")
        toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(toolbar)

        # أزرار التنقل
        act_back = QAction(self.style().standardIcon(QStyle.SP_ArrowBack), "رجوع", self)
        act_back.triggered.connect(lambda: self.current_browser().back() if self.current_browser() else None)
        toolbar.addAction(act_back)

        act_forward = QAction(self.style().standardIcon(QStyle.SP_ArrowForward), "تقدم", self)
        act_forward.triggered.connect(lambda: self.current_browser().forward() if self.current_browser() else None)
        toolbar.addAction(act_forward)

        act_reload = QAction(self.style().standardIcon(QStyle.SP_BrowserReload), "تحديث", self)
        act_reload.triggered.connect(lambda: self.current_browser().reload() if self.current_browser() else None)
        toolbar.addAction(act_reload)

        act_home = QAction(self.style().standardIcon(QStyle.SP_DirHomeIcon), "الرئيسية (Localhost)", self)
        act_home.triggered.connect(self.go_home)
        toolbar.addAction(act_home)

        toolbar.addSeparator()

        # شريط العنوان
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("أدخل رابط موقع أو http://localhost:3000...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        toolbar.addSeparator()

        # أزرار التكبير والتصغير
        act_zoom_in = QAction(self.style().standardIcon(QStyle.SP_ArrowUp), "تكبير", self)
        act_zoom_in.triggered.connect(self.zoom_in)
        toolbar.addAction(act_zoom_in)

        act_zoom_out = QAction(self.style().standardIcon(QStyle.SP_ArrowDown), "تصغير", self)
        act_zoom_out.triggered.connect(self.zoom_out)
        toolbar.addAction(act_zoom_out)

        toolbar.addSeparator()

        # قائمة الأدوات المساعدة
        tools_menu = QMenu(self)
        
        act_hard_reload = QAction(self.style().standardIcon(QStyle.SP_DialogResetButton), "تحديث نقي (Hard Reload)", self)
        act_hard_reload.triggered.connect(self.hard_reload)
        tools_menu.addAction(act_hard_reload)

        act_toggle_dark = QAction(self.style().standardIcon(QStyle.SP_DesktopIcon), "تبديل الثيم الداكن للموقع", self)
        act_toggle_dark.triggered.connect(self.toggle_web_dark_mode)
        tools_menu.addAction(act_toggle_dark)

        act_screenshot = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), "أخذ لقطة شاشة (Screenshot)", self)
        act_screenshot.triggered.connect(self.take_screenshot)
        tools_menu.addAction(act_screenshot)

        act_responsive = QAction(self.style().standardIcon(QStyle.SP_ComputerIcon), "تبديل قياس شاشة الهاتف", self)
        act_responsive.triggered.connect(self.toggle_responsive)
        tools_menu.addAction(act_responsive)

        tools_btn = QToolButton()
        tools_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        tools_btn.setText("أدوات")
        tools_btn.setPopupMode(QToolButton.InstantPopup)
        tools_btn.setMenu(tools_menu)
        toolbar.addWidget(tools_btn)

        # زر DevTools
        act_devtools = QAction(self.style().standardIcon(QStyle.SP_FileDialogContentsView), "فحص العناصر (DevTools)", self)
        act_devtools.triggered.connect(self.open_devtools)
        toolbar.addAction(act_devtools)

    def add_new_tab(self, qurl=None, title="تبويب جديد"):
        if qurl is None:
            qurl = QUrl(DEFAULT_URL)

        browser = QWebEngineView()
        page = CustomWebPage(self.profile, browser, browser_window=self)
        browser.setPage(page)

        index = self.tabs.addTab(browser, title)
        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda u: self.update_url_bar(u, browser))
        browser.titleChanged.connect(lambda t: self.tabs.setTabText(self.tabs.indexOf(browser), t[:18] + "..." if len(t) > 18 else t))
        browser.loadFinished.connect(lambda ok: self.tabs.setTabIcon(self.tabs.indexOf(browser), browser.icon()))

        browser.setUrl(qurl)
        return browser

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def current_browser(self):
        return self.tabs.currentWidget()

    def on_tab_changed(self, index):
        browser = self.current_browser()
        if browser:
            self.update_url_bar(browser.url(), browser)

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        
        if not (text.startswith("http://") or text.startswith("https://") or text.startswith("file://")):
            if text.startswith("localhost") or text.startswith("127.0.0.1"):
                text = "http://" + text
            else:
                text = "https://" + text

        browser = self.current_browser()
        if browser:
            browser.setUrl(QUrl(text))

    def update_url_bar(self, qurl, browser=None):
        if browser == self.current_browser():
            self.url_bar.setText(qurl.toString())
            self.url_bar.setCursorPosition(0)

    def go_home(self):
        browser = self.current_browser()
        if browser:
            browser.setUrl(QUrl(DEFAULT_URL))

    def zoom_in(self):
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(browser.zoomFactor() + 0.1)

    def zoom_out(self):
        browser = self.current_browser()
        if browser:
            browser.setZoomFactor(max(0.2, browser.zoomFactor() - 0.1))

    def hard_reload(self):
        self.profile.clearHttpCache()
        browser = self.current_browser()
        if browser:
            browser.reload()

    def toggle_web_dark_mode(self):
        js_code = """
        (function() {
            let style = document.getElementById('__custom_dark_style');
            if (style) {
                style.remove();
            } else {
                style = document.createElement('style');
                style.id = '__custom_dark_style';
                style.innerHTML = 'html { filter: invert(0.9) hue-rotate(180deg) !important; } img, video, canvas { filter: invert(1) hue-rotate(180deg) !important; }';
                document.head.appendChild(style);
            }
        })();
        """
        browser = self.current_browser()
        if browser:
            browser.page().runJavaScript(js_code)

    def take_screenshot(self):
        browser = self.current_browser()
        if browser:
            file_path, _ = QFileDialog.getSaveFileName(self, "حفظ لقطة الشاشة", "screenshot.png", "PNG Images (*.png)")
            if file_path:
                pixmap = browser.grab()
                pixmap.save(file_path)
                QMessageBox.information(self, "تم الحفظ", f"تم حفظ لقطة الشاشة في:\n{file_path}")

    def toggle_responsive(self):
        if not self.is_mobile:
            self.profile.setHttpUserAgent(MOBILE_USER_AGENT)
            self.setFixedSize(375, 812)
            self.is_mobile = True
        else:
            self.profile.setHttpUserAgent(self.default_user_agent)
            self.setMinimumSize(800, 600)
            self.setMaximumSize(16777215, 16777215)
            self.resize(1280, 850)
            self.is_mobile = False
        
        browser = self.current_browser()
        if browser:
            browser.reload()

    def open_devtools(self):
        browser = self.current_browser()
        if browser:
            self.devtools_dialog = DevToolsDialog(browser.page(), self)
            self.devtools_dialog.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LocalhostBrowser()
    window.show()
    sys.exit(app.exec_())