import patoolib

class Extracter:
    def __init__(self):
        pass

    @staticmethod
    def extract(self, archive_path, out_dir):
        patoolib.extract_archive(archive_path, outdir=out_dir)