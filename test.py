def _set_shortcut(self):
    """
    set ctrl-c/ctrl-v, etc...
    """
    copy_action = qt.QAction(self)
    copy_action.setObjectName('action_copy')
    copy_action.triggered.connect(self.slot_copy)
    copy_action.setShortcut(qt.QKeySequence(qt.QKeySequence.Copy))
    copy_action.setShortcutContext(qt.Qt.WidgetWithChildrenShortcut)
    self.addAction(copy_action)

    paste_action = qt.QAction(self)
    paste_action.setObjectName('action_paste')
    paste_action.triggered.connect(self.slot_paste)
    paste_action.setShortcut(qt.QKeySequence(qt.QKeySequence.Paste))
    paste_action.setShortcutContext(qt.Qt.WidgetWithChildrenShortcut)
    self.addAction(paste_action)

