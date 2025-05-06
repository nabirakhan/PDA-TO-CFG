import sys
from pda_processor import PDA 
from graphviz import Digraph
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtCore import Qt

class MainWindow:
    def setupUi(self, main_window):
        """Initialize the main window UI components."""
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        
        # Apply dark theme with doodle pattern
        self._apply_dark_theme_with_doodles(main_window)
        
        # Central widget with vertical layout
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        
        # Main vertical layout
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(11, 11, 11, 11)
        self.main_layout.setSpacing(6)
        
        # Container for SVG display with centered alignment
        self.svg_container = QtWidgets.QWidget()
        self.svg_container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.svg_layout = QtWidgets.QVBoxLayout(self.svg_container)
        self.svg_layout.setContentsMargins(0, 0, 0, 0)
        self.svg_layout.setAlignment(Qt.AlignCenter)
        
        # SVG display (initially hidden)
        self.svg_display = QtSvg.QSvgWidget()
        self.svg_display.setStyleSheet("background-color: transparent;")
        self.svg_display.hide()
        self.svg_layout.addWidget(self.svg_display)
        
        self.main_layout.addWidget(self.svg_container, 1)  # Add stretch factor to take available space
        
        # Button container with horizontal layout
        self.button_container = QtWidgets.QWidget()
        self.button_container.setFixedHeight(80)  # Fixed height for button bar
        self.button_layout = QtWidgets.QHBoxLayout(self.button_container)
        self.button_layout.setContentsMargins(20, 10, 20, 20)
        self.button_layout.setSpacing(20)
        
        # Create buttons with orange style
        self.open_pda_button = self._create_button("Open PDA", self.open_pda)
        self.convert_button = self._create_button("Convert to CFG", self.convert_to_cfg)
        self.export_button = self._create_button("Export Graph", self.show_export_menu)
        self.help_button = self._create_button("Help", self.show_about)
        
        # Add stretch to center buttons
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.open_pda_button)
        self.button_layout.addWidget(self.convert_button)
        self.button_layout.addWidget(self.export_button)
        self.button_layout.addWidget(self.help_button)
        self.button_layout.addStretch()
        
        # Add button container to main layout (will stay at bottom)
        self.main_layout.addWidget(self.button_container, 0, Qt.AlignBottom)
        
        main_window.setCentralWidget(self.central_widget)
        
        # Menu bar setup (hidden)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        main_window.setMenuBar(self.menu_bar)
        self.menu_bar.hide()
        
        # Export menu (for the export button)
        self.export_menu = QtWidgets.QMenu()
        self._setup_export_menu()
        
        # Initial state - disable buttons until PDA is loaded
        self.set_buttons_state(False)

    def _create_button(self, text, callback):
        """Create a styled orange button with white text."""
        button = QtWidgets.QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #ff9600;
                color: white;
                border: 2px solid #ff9600;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #ffaa33;
                border: 2px solid #ffaa33;
            }
            QPushButton:pressed {
                background-color: #e08500;
                border: 2px solid #e08500;
            }
            QPushButton:disabled {
                background-color: #666666;
                border: 2px solid #666666;
                color: #aaaaaa;
            }
        """)
        button.clicked.connect(callback)
        return button

    def _apply_dark_theme_with_doodles(self, window):
        """Apply dark theme with doodle pattern background."""
        # Set dark palette
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
        
        # Create doodle pattern
        self.doodle_pattern = QtGui.QPixmap(800, 600)
        self.doodle_pattern.fill(Qt.transparent)
        
        painter = QtGui.QPainter(self.doodle_pattern)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(80, 80, 80, 50), 1))
        
        # Draw random doodles
        import random
        for _ in range(50):
            x1 = random.randint(0, 800)
            y1 = random.randint(0, 600)
            x2 = random.randint(0, 800)
            y2 = random.randint(0, 600)
            
            # Randomly choose between line, circle or arc
            choice = random.randint(0, 2)
            if choice == 0:
                painter.drawLine(x1, y1, x2, y2)
            elif choice == 1:
                radius = random.randint(5, 30)
                painter.drawEllipse(x1, y1, radius, radius)
            else:
                span = random.randint(30, 270)
                painter.drawArc(x1, y1, x2, y2, 0, span * 16)
        
        painter.end()
        
        # Apply the pattern as background
        window.setAutoFillBackground(True)
        palette = window.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(self.doodle_pattern))
        window.setPalette(palette)

    def _setup_export_menu(self):
        """Setup the export menu options."""
        self.export_gv_action = QtWidgets.QAction(".gv", self.central_widget)
        self.export_pdf_action = QtWidgets.QAction(".pdf", self.central_widget)
        self.export_png_action = QtWidgets.QAction(".png", self.central_widget)
        self.export_svg_action = QtWidgets.QAction(".svg", self.central_widget)
        
        self.export_gv_action.triggered.connect(lambda: self.export_graph('gv'))
        self.export_pdf_action.triggered.connect(lambda: self.export_graph('pdf'))
        self.export_png_action.triggered.connect(lambda: self.export_graph('png'))
        self.export_svg_action.triggered.connect(lambda: self.export_graph('svg'))
        
        self.export_menu.addAction(self.export_gv_action)
        self.export_menu.addAction(self.export_pdf_action)
        self.export_menu.addAction(self.export_png_action)
        self.export_menu.addAction(self.export_svg_action)

    def set_buttons_state(self, enabled):
        """Enable/disable buttons based on whether PDA is loaded."""
        self.convert_button.setEnabled(enabled)
        self.export_button.setEnabled(enabled)

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

        self.set_buttons_state(True)
        self.pda = PDA(file_name)
        
        # Create and render PDA visualization with orange theme
        graph = Digraph('pda_machine', filename='pda_tmp.gv', format='svg')
        graph.attr('graph', rankdir='LR', size='8,5', bgcolor='transparent')
        graph.attr('node', fontcolor='white', fontname='Arial')
        graph.attr('edge', fontcolor='white', fontname='Arial')
        
        # Add PDF-specific attributes for black background
        graph.attr('graph', _attributes={'bgcolor': '#000000'})  # Black background for PDF
        graph.attr('node', _attributes={'color': '#ff9600', 'fontcolor': 'white'})
        graph.attr('edge', _attributes={'color': '#ff9600', 'fontcolor': 'white'})

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
        
        # Show the SVG display (buttons remain visible)
        self.svg_display.setMinimumSize(600, 400)  # Set minimum size for the SVG display
        self.svg_display.show()

    def show_export_menu(self):
        """Show the export menu at the button position."""
        self.export_menu.exec_(QtGui.QCursor.pos())

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
