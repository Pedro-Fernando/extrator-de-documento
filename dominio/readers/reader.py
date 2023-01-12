
class TxtReader:
    def __init__(self, path):
        self.path = path
        self.text = None

    def read_txt(self):
        try:
            with open(self.path, "r") as f:
                self.text = f.read()
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")

