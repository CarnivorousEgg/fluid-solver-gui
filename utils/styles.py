"""
Application Styling and Theme Configuration
============================================

This file contains all styling for the Solver GUI application.

CUSTOMIZATION:
- Change colors in APP_STYLESHEET
- Modify fonts in the QWidget section
- Add custom styles for new widgets
"""

# ============================================================
# COLOR PALETTE
# ============================================================
# Change these values to modify the entire application theme

COLORS = {
    'background': '#f7f9fc',      # Main background color
    'primary': '#3b82f6',         # Primary button color
    'primary_hover': '#2563eb',   # Button hover color
    'primary_pressed': '#1d4ed8', # Button pressed color
    'secondary_bg': '#eff6ff',    # Secondary button background
    'secondary_text': '#1e40af',  # Secondary button text
    'border': '#cbd5e1',          # Border color
    'text': '#222',               # Main text color
    'title': '#1e3a8a',           # Title text color
    'danger': '#ef4444',          # Delete button color
    'danger_hover': '#fee2e2',    # Delete button hover
}

# ============================================================
# APPLICATION STYLESHEET
# ============================================================

APP_STYLESHEET = f"""
    /* Main widget styling */
    QWidget {{ 
        background: {COLORS['background']}; 
        color: {COLORS['text']}; 
        font-family: 'Segoe UI', Arial, sans-serif; 
        font-size: 11pt; 
    }}
    
    /* Title label styling */
    QLabel#title {{ 
        font-size: 20pt; 
        font-weight: 700; 
        color: {COLORS['title']}; 
        padding: 10px; 
    }}
    
    /* Group box styling */
    QGroupBox {{ 
        font-weight: 600; 
        border: 1px solid {COLORS['border']}; 
        border-radius: 8px; 
        background: #ffffff; 
        margin-top: 24px; 
        padding-top: 25px; 
        padding-bottom: 15px; 
    }}
    QGroupBox::title {{ 
        subcontrol-origin: margin; 
        left: 10px; 
        padding: 0 5px; 
    }}
    
    /* Input field styling */
    QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox {{ 
        min-height: 30px; 
        max-height: 30px; 
        padding: 4px; 
        border: 1px solid {COLORS['border']}; 
        border-radius: 4px; 
        background: white; 
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{ 
        border: 1px solid {COLORS['primary']}; 
    }}
    
    /* Primary button styling */
    QPushButton {{ 
        min-height: 32px; 
        background-color: {COLORS['primary']}; 
        color: white; 
        border-radius: 6px; 
        font-weight: 600; 
        padding: 0 15px; 
        border: none; 
    }}
    QPushButton:hover {{ 
        background-color: {COLORS['primary_hover']}; 
    }}
    QPushButton:pressed {{ 
        background-color: {COLORS['primary_pressed']}; 
    }}
    
    /* Secondary button styling */
    QPushButton[secondary='true'] {{ 
        background-color: {COLORS['secondary_bg']}; 
        color: {COLORS['secondary_text']}; 
        border: 1px solid #bfdbfe; 
    }}
    QPushButton[secondary='true']:hover {{ 
        background-color: #dbeafe; 
    }}
    
    /* Danger/Delete button styling */
    QPushButton[danger='true'] {{ 
        background-color: transparent; 
        color: {COLORS['danger']}; 
        font-weight: bold; 
        font-size: 14pt; 
        min-width: 30px; 
    }}
    QPushButton[danger='true']:hover {{ 
        background-color: {COLORS['danger_hover']}; 
        border-radius: 4px; 
    }}
    
    /* Tab widget styling */
    QTabWidget::pane {{ 
        border: 0; 
    }}
    QTabBar::tab {{ 
        background: #e2e8f0; 
        padding: 8px 20px; 
        margin-right: 2px; 
        border-top-left-radius: 6px; 
        border-top-right-radius: 6px; 
        color: #64748b; 
    }}
    QTabBar::tab:selected {{ 
        background: {COLORS['primary']}; 
        color: white; 
        font-weight: bold; 
    }}
    QTabBar::tab:hover:!selected {{ 
        background: {COLORS['border']}; 
    }}
"""


def get_stylesheet():
    """
    Get the application stylesheet.
    
    Returns:
        str: Complete CSS stylesheet for the application
    """
    return APP_STYLESHEET
