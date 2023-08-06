from contextlib import contextmanager
import subprocess
import os
import ROOT as R


@contextmanager
def canvas_upload(name='c', title='', w=1600, h=900, ncols=1, nrows=1, local_path=None, remote_path='.', keep_local_file=False):
    c = R.TCanvas(name, title, w, h)
    c.Divide(ncols, nrows)
    yield c
    fname = local_path if local_path else name + '.pdf'
    c.SaveAs(fname)
    R.gDirectory.Delete(name)
    subprocess.run(f'{os.path.expanduser("~/dropbox_uploader.sh")} upload {fname} {remote_path}'.split())
    if not keep_local_file:
        os.remove(fname)


def pretty_draw(frame):
    frame.GetXaxis().CenterTitle()
    frame.GetYaxis().CenterTitle()
    frame.GetYaxis().SetMaxDigits(3)
    frame.Draw()

