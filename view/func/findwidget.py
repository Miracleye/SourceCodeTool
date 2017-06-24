import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox, QToolTip

from core.common import App
from core.common.config import FontHolder
from core.common.uilang import UILangHolder
from view.func.combobox import FilterComboBox
from view.func.edit import DirEdit, FilterEdit


class FindWidget(QtWidgets.QWidget):
    # represent the state of current task
    IDLE = False
    BUSY = True

    def __init__(self, controller, parent=None):
        super(FindWidget, self).__init__(parent)
        self.controller = controller
        self._state = self.IDLE
        self._setup_ui(self)
        self._update_ui()
        self._start_btn_clickable()
        self.reset_ui()
        self._init_signals()

    def _setup_ui(self, FindWidget):
        self.grid_layout = QtWidgets.QGridLayout(FindWidget)
        self.target_label = QtWidgets.QLabel(FindWidget)
        self.target_label.setMinimumSize(QtCore.QSize(0, 31))
        self.target_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.grid_layout.addWidget(self.target_label, 2, 0, 1, 1)
        self.start_btn = QtWidgets.QPushButton(FindWidget)
        self.start_btn.setMinimumSize(QtCore.QSize(0, 31))
        self.grid_layout.addWidget(self.start_btn, 0, 2, 1, 1)
        self.dir_edit = DirEdit(self)
        self.dir_edit.setMinimumSize(QtCore.QSize(0, 31))
        self.dir_edit.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.dir_edit.setAutoFillBackground(False)
        self.dir_edit.setFrame(True)
        self.dir_edit.setClearButtonEnabled(True)
        self.grid_layout.addWidget(self.dir_edit, 0, 1, 1, 1)
        self.target_edit = QtWidgets.QLineEdit(FindWidget)
        self.target_edit.setMinimumSize(QtCore.QSize(0, 31))
        self.target_edit.setClearButtonEnabled(True)
        self.grid_layout.addWidget(self.target_edit, 2, 1, 2, 1)
        self.filter_label = QtWidgets.QLabel(FindWidget)
        self.filter_label.setMinimumSize(QtCore.QSize(0, 31))
        self.filter_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.filter_label.setScaledContents(False)
        self.grid_layout.addWidget(self.filter_label, 4, 0, 1, 1)
        self.dir_label = QtWidgets.QLabel(FindWidget)
        self.dir_label.setMinimumSize(QtCore.QSize(0, 31))
        self.grid_layout.addWidget(self.dir_label, 0, 0, 1, 1)
        self.filter_edit = FilterEdit(self)
        self.filter_edit.setMinimumSize(QtCore.QSize(0, 31))
        self.grid_layout.addWidget(self.filter_edit, 4, 1, 1, 1)
        self.filter_box = FilterComboBox(self)
        self.filter_box.setMinimumSize(QtCore.QSize(0, 31))
        self.filter_box.setFrame(False)
        self.grid_layout.addWidget(self.filter_box, 4, 2, 1, 1)
        self.regex_btn = QtWidgets.QCheckBox(FindWidget)
        self.regex_btn.setMinimumSize(QtCore.QSize(0, 31))
        self.grid_layout.addWidget(self.regex_btn, 2, 2, 1, 1)
        # table settings
        self.result_table = QtWidgets.QTableView(FindWidget)
        self.result_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.result_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.result_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.result_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.result_table.setTextElideMode(QtCore.Qt.ElideLeft)
        self.result_table.resizeRowsToContents()
        self.result_table.setMouseTracking(True)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setCornerButtonEnabled(False)
        self.result_table.setSortingEnabled(True)
        self.result_table.horizontalHeader().setDefaultSectionSize(200)
        self.result_table.horizontalHeader().setHighlightSections(False)
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.verticalHeader().setVisible(True)
        self.result_table.verticalHeader().setCascadingSectionResizes(False)
        self.result_table.verticalHeader().setDefaultSectionSize(30)
        self.result_table.verticalHeader().setHighlightSections(False)
        self.grid_layout.addWidget(self.result_table, 5, 0, 1, 3)
        QtCore.QMetaObject.connectSlotsByName(FindWidget)

    def _update_ui(self):
        font = FontHolder.get()
        self.dir_label.setFont(font)
        self.dir_label.setText(UILangHolder.get(App.DIR_LABEL))
        self.dir_edit.setFont(font)
        self.dir_edit.update_lang()
        self.start_btn.setFont(font)
        self.start_btn.setText(UILangHolder.get(App.START))
        self.target_label.setFont(font)
        self.target_label.setText(UILangHolder.get(App.TARGET_LABEL))
        self.target_edit.setFont(font)
        self.regex_btn.setFont(font)
        self.regex_btn.setText(UILangHolder.get(App.REGEX))
        self.filter_label.setFont(font)
        self.filter_label.setText(UILangHolder.get(App.FILTER_LABEL))
        self.filter_edit.setFont(font)
        self.result_table.setFont(font)

    def _init_signals(self):
        self.dir_edit.textChanged.connect(self._start_btn_clickable)
        self.target_edit.textChanged.connect(self._start_btn_clickable)
        self.start_btn.clicked.connect(self._do_prepare)
        self.filter_box.currentIndexChanged.connect(self._filter_edit_changed)
        self.result_table.entered.connect(self._show_content)

    def reset_ui(self):
        """ Reset the ui state to IDLE, enable all components.
        """
        self.set_state(self.IDLE)
        self.dir_edit.setEnabled(True)
        self.start_btn.setText(UILangHolder.get(App.START))
        self.target_edit.setEnabled(True)
        self.regex_btn.setEnabled(True)
        self.filter_edit.setEnabled(True)
        self.filter_box.setEnabled(True)
        self.result_table.setSortingEnabled(True)

    def set_ui(self):
        """ Set the ui state to BUSY, disable all components.
        """
        self.set_state(self.BUSY)
        self.dir_edit.setEnabled(False)
        self.start_btn.setText(UILangHolder.get(App.STOP))
        self.target_edit.setEnabled(False)
        self.regex_btn.setEnabled(False)
        self.filter_edit.setEnabled(False)
        self.filter_box.setEnabled(False)
        self.result_table.setSortingEnabled(False)

    def _show_content(self, current_index):
        if not current_index.isValid():
            return
        content = self.result_table.model().data(current_index)
        QToolTip.showText(QCursor.pos(), content)

    def _start_btn_clickable(self):
        if self.dir_edit.text() and self.target_edit.text():
            self.start_btn.setEnabled(True)
        else:
            self.start_btn.setEnabled(False)

    def _filter_edit_changed(self, index):
        """ The slot for Qt signal. Add a filter to the @self.filter_edit, if the filter exists, does nothing.
        :param index: the index of @self.filter_box
        """
        if index:
            pre_text = self.filter_edit.text().strip()
            text = self.filter_box.get_filter_text(index)
            if pre_text:
                if pre_text.find(text) != -1:
                    return
                cur_text = ';'.join([pre_text, text])
                self.filter_edit.setText(cur_text)
            else:
                self.filter_edit.setText(text)

    def _do_prepare(self):
        """ Do preparations before calling the @self.controller.do_request method, at the same time,
            this method update the UI state...
        """
        base_dir = self.dir_edit.text()
        target_str = self.target_edit.text()
        if not target_str:
            return
        if os.path.isdir(base_dir):
            if self.get_state() == self.IDLE:
                self.set_ui()
                self.controller.do_request()
            elif self.get_state() == self.BUSY:
                self.controller.stop_operation()
                self.reset_ui()
        else:
            QMessageBox.critical(None, "Directory doesn't exist", base_dir,
                                 QMessageBox.Yes, QMessageBox.Yes)

    def get_dir(self):
        return self.dir_edit.text()

    def get_target_string(self):
        return self.target_edit.text()

    def is_regex_enable(self):
        return self.regex_btn.isChecked()

    def get_filters(self):
        """ Return the filters set. if error occurred while parsing, or the filter text is empty, return None
        """
        filter_text = self.filter_edit.text().strip()
        if not filter_text:
            return None
        try:
            filters_list = filter_text.split(';')
            filters = set()
            for each in filters_list:
                filters.add(each.strip().replace('*', ''))
            return filters
        except Exception:
            return None

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def set_result_table(self, model):
        self.result_table.setModel(model)
