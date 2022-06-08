from PySide6 import QtWidgets, QtGui, QtCore
from gui.utilities.library_model import LibraryModel
from scripts.card.card_editor import Card, LIBRARY
from gui.card.card_editor_ui import CardEditor

class SearchFiles ( QtWidgets.QDialog ):

    def __init__ ( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.create_widgets()
        self.setWindowTitle( "Search Files" )
        self.setMinimumSize( QtCore.QSize( 400, 100 ) )
        self.setMaximumSize( QtCore.QSize( 600, 150 ) )

    def create_widgets ( self ):
        layout = QtWidgets.QGridLayout()

        enter_sl = QtWidgets.QLineEdit( placeholderText="C:\\", disabled=True )
        layout.addWidget( enter_sl, 0, 0 )
        self.enter_sl = enter_sl

        search_sl = QtWidgets.QPushButton( "Search", clicked=self.search_sl )
        layout.addWidget( search_sl, 0, 1 )
        self.sl_path = None

        enter_wa = QtWidgets.QLineEdit( placeholderText="C:\\", disabled=True )
        layout.addWidget( enter_wa, 1, 0 )
        self.enter_wa = enter_wa

        search_wa = QtWidgets.QPushButton( "Search", clicked=self.search_wa )
        layout.addWidget( search_wa, 1, 1 )
        self.wa_path = None

        confirm_files = QtWidgets.QPushButton( "Confirm", clicked=self.confirm_files )
        layout.addWidget( confirm_files, 2, 0, 1, 2 )

        self.setLayout( layout )

    def search_sl ( self ):
        sl_path = QtWidgets.QFileDialog.getOpenFileUrl( self.parent(), "Select SL File", filter="SLUS_014.11" )[0]

        if sl_path:
            self.enter_sl.setText( sl_path.path()[1:] )

    def search_wa ( self ):
        wa_path = QtWidgets.QFileDialog.getOpenFileUrl( self.parent(), "Select WA File", filter="WA_MRG.MRG" )[0]

        if wa_path:
            self.enter_wa.setText( wa_path.path()[1:] )

    def confirm_files ( self ):
        self.sl_path = self.enter_sl.text()
        self.wa_path = self.enter_wa.text()
        self.close()

class MainWindow ( QtWidgets.QMainWindow ):

    path_changed = QtCore.Signal()

    def __init__ ( self ):
        super().__init__()
        self.create_widgets()
        self.start_app()

    def create_widgets ( self ):
        # Main menu
        menu_bar = QtWidgets.QMenuBar( self )
        self.setMenuBar( menu_bar )

        file_menu = menu_bar.addMenu( "File" )
        file_menu.addAction( "Open...", self.open_file, QtGui.QKeySequence( "Ctrl+O" ) )
        file_menu.addAction( "Save...", self.save_file, QtGui.QKeySequence( "Ctrl+S" ) )
        file_menu.addAction( "Exit", self.stop_app )

        edit_menu = menu_bar.addMenu( "Edit" )
        edit_menu.addAction( "Edit Card", self.load_card_editor )
        edit_menu.addAction( "Edit Duelist", self.load_duelist_editor )
        edit_menu.addAction( "Edit Campaign", self.load_campaign_editor )
        edit_menu.addAction( "Edit Behavior", self.load_behavior_editor )

        help_menu = menu_bar.addMenu( "Help" )
        help_menu.addAction( "About", self.about_info )

        # Central widget
        main_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget( main_widget )

        card_editor = CardEditor()
        self.path_changed.connect( LibraryModel.update_library )
        main_widget.addWidget( card_editor )

        main_widget.addWidget( QtWidgets.QLabel( "Page 2" ) )
        main_widget.addWidget( QtWidgets.QLabel( "Page 3" ) )
        main_widget.addWidget( QtWidgets.QLabel( "Page 4" ) )

        # Status bar
        status_bar = QtWidgets.QStatusBar( self )
        self.setStatusBar( status_bar )

        # Custom widgets
        self.search_files = SearchFiles( parent=self, modal=True )

    def start_app ( self ):
        self.show()

    def stop_app ( self ):
        self.close()

    def about_info ( self ):
        QtWidgets.QMessageBox.information( self, "About Info", "Welcome to the beta version of Yu-Gi-Oh! Game Maker" )

    def open_file ( self ):
        self.search_files.exec()
        sl_path = self.search_files.sl_path
        wa_path = self.search_files.wa_path

        if sl_path and wa_path:
            LIBRARY.clear()
            Card.load_library( sl_path, wa_path )
            QtWidgets.QMessageBox.information( self, "Load Files", "Successfully loaded files for editing" )
            self.path_changed.emit()

    def save_file ( self ):
        self.search_files.exec()
        sl_path = self.search_files.sl_path
        wa_path = self.search_files.wa_path

        if sl_path and wa_path:
            Card.save_library( sl_path, wa_path )
            QtWidgets.QMessageBox.information( self, "Save Files", "Successfully saved changes in files" )

    def load_card_editor ( self ):
        self.centralWidget().setCurrentIndex( 0 )

    def load_duelist_editor ( self ):
        self.centralWidget().setCurrentIndex( 1 )

    def load_campaign_editor ( self ):
        self.centralWidget().setCurrentIndex( 2 )

    def load_behavior_editor ( self ):
        self.centralWidget().setCurrentIndex( 3 )

app = QtWidgets.QApplication([])
win = MainWindow()
app.exec()
