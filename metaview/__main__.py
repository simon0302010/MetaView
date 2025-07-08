from . import app
import sys

if __name__ == "__main__":
    metaview = app.MetaView(application_id="de.simon0302010.MetaView")
    metaview.run(sys.argv)