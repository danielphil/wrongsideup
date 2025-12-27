from pdfmerger.reorder import two_sided_reorder_inplace
import wx
import threading
import os


def process_file(path: str) -> None:
    if not path.lower().endswith(".pdf"):
        raise ValueError("Please drop a PDF file.")
    
    two_sided_reorder_inplace(path)


class DropTarget(wx.FileDropTarget):
    def __init__(self, window, callback):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.callback = callback

    def OnDropFiles(self, x, y, filenames):
        if filenames:
            self.callback(filenames)
        return True


def run_gui():
    app = wx.App(False)
    frame = wx.Frame(None, title="Wrong Side Up", size=(600, 500))

    panel = wx.Panel(frame)
    main_sizer = wx.BoxSizer(wx.VERTICAL)

    header = wx.StaticText(panel, label="Drag and drop PDF files into this window to correctly order pages in a two sided scan.")
    main_sizer.Add(header, 0, wx.ALL | wx.ALIGN_CENTER, 10)

    # List control to show filename and status
    list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
    list_ctrl.InsertColumn(0, "Filename", width=420)
    list_ctrl.InsertColumn(1, "Status", width=120)
    # give the list more room than the error box (3:1)
    main_sizer.Add(list_ctrl, 3, wx.EXPAND | wx.ALL, 10)

    # Scrollable, read-only text control to display errors
    error_box = wx.TextCtrl(
        panel,
        style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_SUNKEN,
    )
    main_sizer.Add(error_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

    panel.SetSizer(main_sizer)

    # map path -> list index
    path_to_index: dict[str, int] = {}

    def append_error(path: str, message: str) -> None:
        name = os.path.basename(path)
        error_box.AppendText(f"{name}: {message}\n")

    def update_status(index: int, success: bool, message: str | None = None):
        mark = "✓" if success else "✗"
        list_ctrl.SetItem(index, 1, mark)
        # color status cell
        color = wx.Colour(0, 128, 0) if success else wx.Colour(192, 0, 0)
        list_ctrl.SetItemTextColour(index, color)
        if message:
            list_ctrl.SetItem(index, 1, message)

    def worker(path: str, index: int):
        try:
            process_file(path)
            wx.CallAfter(update_status, index, True, "Done")
        except Exception as e:
            wx.CallAfter(update_status, index, False, str(e))
            wx.CallAfter(append_error, path, str(e))

    def on_drop(paths: list[str]):
        list_ctrl.DeleteAllItems()

        for path in paths:
            filename = os.path.basename(path)
            idx = list_ctrl.InsertItem(list_ctrl.GetItemCount(), filename)
            list_ctrl.SetItem(idx, 1, "Processing...")
            path_to_index[path] = idx
            # start background thread for processing
            t = threading.Thread(target=worker, args=(path, idx), daemon=True)
            t.start()

    drop_target = DropTarget(panel, on_drop)
    panel.SetDropTarget(drop_target)

    frame.Show()
    app.MainLoop()