import ftplib

conn_params = {}


class FTPClient(object):

    def __init__(self, host=None, port=None, username=None, password=None, **kwargs):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def get_connect(self):
        try:
            ftp = ftplib.FTP()
            ftp.connect(host=self.host, port=self.port)
            ftp.login(self.username, self.password)
        except Exception as e:
            try:
                ftp.quit()
            except Exception:
                pass
            raise e
        return ftp

    def download_file(self, remotepath, localpath):
        bufsize = 1024
        ftp = self.get_connect()
        with open(localpath, 'wb') as f:
            try:
                ftp.retrbinary('RETR ' + remotepath, f.write, bufsize)
                ftp.set_debuglevel(0)
                ftp.quit()
            except Exception as e:
                ftp.quit()
                raise e

    def upload_file(self, remotepath, localpath):
        bufsize = 1024
        ftp = self.get_connect()
        with open(localpath, 'rb') as f:
            try:
                ftp.storbinary('STOR ' + remotepath, f, bufsize)
                ftp.set_debuglevel(0)
                ftp.quit()
            except Exception as e:
                ftp.quit()
                raise e

    def delete_file(self, remotepath):
        ftp = self.get_connect()
        try:
            ftp.delete(remotepath)
            ftp.set_debuglevel(0)
            ftp.quit()
        except Exception as e:
            ftp.quit()
            raise e
