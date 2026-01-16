"""
Helper Functions and Utilities
==============================

Common functions used across the application.
"""

from PySide6.QtWidgets import QComboBox, QFileDialog


def create_combo_box(items):
    """
    Create a combo box with the given items.
    
    Args:
        items (list): List of string items to add to combo box
        
    Returns:
        QComboBox: Configured combo box widget
    """
    combo = QComboBox()
    combo.addItems(items)
    return combo


def browse_file(parent, line_edit, title="Select File", file_filter="All Files (*)"):
    """
    Open a file browser dialog and set the selected path to a line edit.
    
    Args:
        parent: Parent widget for the dialog
        line_edit: QLineEdit to update with selected path
        title (str): Dialog window title
        file_filter (str): File type filter
    """
    path, _ = QFileDialog.getOpenFileName(parent, title, "", file_filter)
    if path:
        line_edit.setText(path)


def save_file_dialog(parent, default_name="inputFile.txt", file_filter="Text Files (*.txt);;All Files (*)"):
    """
    Open a save file dialog.
    
    Args:
        parent: Parent widget for the dialog
        default_name (str): Default filename
        file_filter (str): File type filter
        
    Returns:
        str: Selected file path, or None if cancelled
    """
    path, _ = QFileDialog.getSaveFileName(parent, "Save Input File", default_name, file_filter)
    return path if path else None
