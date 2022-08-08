import patoolib

class Extracter:
    @staticmethod
    def extract(archive_path, out_dir):
        patoolib.extract_archive(archive_path, outdir=out_dir)