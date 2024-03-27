import wx

APP_NAME = "复制搜索后台"

class AppFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title=APP_NAME, size=(600, 400))
        
def main():
    app = wx.App()
    frame = AppFrame()
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
