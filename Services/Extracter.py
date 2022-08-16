import os
import patoolib
from shutil import rmtree

class Extracter:
    @staticmethod
    def extract(archive, verbosity=0, outdir=None, program=None):
        if outdir:
            if os.path.exists(outdir):
                rmtree(outdir)
        patoolib.extract_archive(archive, verbosity, outdir, program)