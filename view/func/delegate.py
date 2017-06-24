from PyQt5.QtWidgets import QStyleOptionViewItem, QStyle, QAbstractItemDelegate


class NoFocusDelegate(QAbstractItemDelegate):
    def __init__(self):
        super(NoFocusDelegate, self).__init__()

    def paint(self, painter, option, index):
        item_option = QStyleOptionViewItem(option)
        if item_option.state and QStyle.State_HasFocus:
            item_option.state = item_option.state ^ QStyle.State_HasFocus
        # QStyledItemDelegate.paint(painter, item_option, index)
        super(NoFocusDelegate, self).paint(painter, item_option, index)
