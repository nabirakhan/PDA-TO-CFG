import sys
from pda_processor import PDA 
from graphviz import Digraph
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg


class MainWindow:
    def setupUi(self, main_window):
        """Initialize the main window UI components."""
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        
        # Apply dark theme stylesheet
        self._apply_dark_theme(main_window)
        
        #central widget
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        
        #layout 
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(11, 11, 11, 11)
        self.main_layout.setSpacing(6)
        
        #svg display
        self.svg_display = QtSvg.QSvgWidget(self.central_widget)
        self.svg_display.setStyleSheet("background-color: #222222;")
        self.main_layout.addWidget(self.svg_display)
        
        main_window.setCentralWidget(self.central_widget)
        
        # Menu bar setup
        self._setup_menu_bar(main_window)
        self._setup_actions(main_window)
        self._connect_actions()
        self._setup_menu_hierarchy()
        
        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        
        # Initial state - disable export/convert until PDA is loaded
        self.set_menu_state(False)

    def _apply_dark_theme(self, window):
        """Apply dark theme styling to the application."""
        dark_palette = QtGui.QPalette()
        dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(30, 30, 30))
        dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
        dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(40, 40, 40))
        dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(50, 50, 50))
        dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 220))
        dark_palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 220))
        dark_palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
        dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(50, 50, 50))
        dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 200, 100))
        dark_palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 150, 0))
        dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(255, 150, 0))
        dark_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
        
        window.setPalette(dark_palette)
        window.setStyleSheet("""
            QMenuBar {
                background-color: #333333;
                color: #ffc864;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #555555;
            }
            QMenu {
                background-color: #333333;
                border: 1px solid #555555;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #ff9600;
                color: #000000;
            }
            QMessageBox {
                background-color: #333333;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
        """)

    def _setup_menu_bar(self, main_window):
        """Initialize the menu bar and its menus."""
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #333333;
                color: #ffc864;
                font-weight: bold;
            }
        """)
        
        self.file_menu = QtWidgets.QMenu("File", self.menu_bar)
        self.export_menu = QtWidgets.QMenu("Export as...", self.file_menu)
        self.help_menu = QtWidgets.QMenu("Help", self.menu_bar)
        self.pda_menu = QtWidgets.QMenu("PDA", self.menu_bar)
        
        main_window.setMenuBar(self.menu_bar)

    def _setup_actions(self, main_window):
        """Create all action items for the menus."""
        self.open_pda_action = QtWidgets.QAction("Open PDA", main_window)
        self.open_pda_action.setShortcut("Ctrl+O")
        
        self.exit_action = QtWidgets.QAction("Exit", main_window)
        self.exit_action.setShortcut("Ctrl+Q")
        
        self.about_action = QtWidgets.QAction("About", main_window)
        self.about_action.setShortcut("Ctrl+H")
        
        # Export actions
        self.export_gv_action = QtWidgets.QAction(".gv", main_window)
        self.export_pdf_action = QtWidgets.QAction(".pdf", main_window)
        self.export_png_action = QtWidgets.QAction(".png", main_window)
        self.export_svg_action = QtWidgets.QAction(".svg", main_window)
        
        self.convert_action = QtWidgets.QAction("Convert to CFG", main_window)

    def _connect_actions(self):
        """Connect actions to their respective handlers."""
        self.open_pda_action.triggered.connect(self.open_pda)
        self.exit_action.triggered.connect(sys.exit)
        self.about_action.triggered.connect(self.show_about)
        
        self.export_gv_action.triggered.connect(lambda: self.export_graph('gv'))
        self.export_pdf_action.triggered.connect(lambda: self.export_graph('pdf'))
        self.export_png_action.triggered.connect(lambda: self.export_graph('png'))
        self.export_svg_action.triggered.connect(lambda: self.export_graph('svg'))
        
        self.convert_action.triggered.connect(self.convert_to_cfg)

    def _setup_menu_hierarchy(self):
        """Organize actions into menu hierarchy."""
        self.export_menu.addAction(self.export_gv_action)
        self.export_menu.addAction(self.export_pdf_action)
        self.export_menu.addAction(self.export_png_action)
        self.export_menu.addAction(self.export_svg_action)
        
        self.file_menu.addAction(self.open_pda_action)
        self.file_menu.addMenu(self.export_menu)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
        
        self.help_menu.addAction(self.about_action)
        self.pda_menu.addAction(self.convert_action)
        
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.pda_menu)
        self.menu_bar.addMenu(self.help_menu)

    def retranslateUi(self, main_window):
        """Set display text for UI elements."""
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "PDA to CFG Converter"))

    def set_menu_state(self, enabled):
        """Enable/disable menu items based on whether PDA is loaded."""
        self.export_gv_action.setEnabled(enabled)
        self.export_pdf_action.setEnabled(enabled)
        self.export_png_action.setEnabled(enabled)
        self.export_svg_action.setEnabled(enabled)
        self.convert_action.setEnabled(enabled)

    def open_pda(self):
        """Load a PDA from XML file and display its graph."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.central_widget, 
            'Open PDA file...', 
            '.', 
            'XML Files (*.xml)'
        )

        if not file_name:
            return

        self.set_menu_state(True)
        self.pda = PDA(file_name)
        
        # Create and render PDA visualization with orange theme
        graph = Digraph('pda_machine', filename='pda_tmp.gv', format='svg')
        graph.attr('graph', rankdir='LR', size='8,5', bgcolor='#222222')
        graph.attr('node', fontcolor='white', fontname='Arial')
        graph.attr('edge', fontcolor='white', fontname='Arial')

        # Initial state with arrow
        graph.attr('node', shape='plaintext', color='#ff9600')
        graph.node('start')
        graph.attr('node', shape='circle', style='filled', fillcolor='#ff9600', color='#ff9600', fontcolor='black')
        graph.node(self.pda.initial_state)
        graph.edge('start', self.pda.initial_state, color='#ff9600')

        # Final states (double circle)
        graph.attr('node', shape='doublecircle', style='filled', fillcolor='#ff9600', color='#ff9600', fontcolor='black')
        for final_state in self.pda.final_states:
            graph.node(final_state)

        # Regular states and transitions
        graph.attr('node', shape='circle', style='filled', fillcolor='#ff9600', color='#ff9600', fontcolor='black')
        for transition in self.pda.transitions:
            label = f"{PDA.lambda_symbol(transition['input'])},{PDA.lambda_symbol(transition['stack_read'])},{PDA.lambda_symbol(transition['stack_write'])}"
            graph.edge(transition['source'], transition['destination'], label=label, color='#ff9600', fontcolor='white')

        graph.render()
        self.svg_display.load('pda_tmp.gv.svg')
        self.current_graph = graph

    def export_graph(self, file_type):
        """Export the current graph to specified file format."""
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.central_widget,
            f'Export as {file_type}',
            '',
            f'{file_type.upper()} Files (*.{file_type})'
        )

        if file_name:
            self.current_graph.format = file_type
            self.current_graph.render(file_name)

    def convert_to_cfg(self):
        """Convert loaded PDA to CFG and display results."""
        cfg_rules = self.pda.convert_to_cfg()
        
        message_box = QtWidgets.QMessageBox()
        message_box.setStyleSheet("""
            QMessageBox {
                background-color: #333333;
            }
            QMessageBox QLabel {
                color: #ffc864;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #505050;
                color: white;
                border: 1px solid #666;
                padding: 5px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #ff9600;
                color: black;
            }
        """)
        message_box.setText('<br>'.join(cfg_rules))
        message_box.setWindowTitle('Resulting CFG Rules')
        message_box.exec_()

    def show_about(self):
        """Display about dialog."""
        QtWidgets.QMessageBox.information(
            self.central_widget,
            'About',
            'PDA to CFG Converter\nDeveloped by: Nabira Khan, Rameen Zehra, Aisha Asif',
            QtWidgets.QMessageBox.Ok
        )
