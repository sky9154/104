from win10toast import ToastNotifier


def toast (message: str):
  '''
  發送通知
  '''

  toaster = ToastNotifier()

  toaster.show_toast(
    title='打卡上傳',
    msg=message,
    icon_path='favicon.ico',
    duration=3
  )