class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file="./config/skin/white.qss"):
        with open(qss_file, 'r', encoding='utf-8') as f:
            return f.read()
