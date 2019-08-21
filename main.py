from blocket import blocket
from tradera import tradera


def main(request):

    if request.args.get("q"):
        q = request.args.get("q")
    else:
        q = ""

    if request.args.get("al"):
        al = True
    else:
        al = False

    if request.args.get("thn"):
        thn = True
    else:
        thn = False

    blocket(q, al, thn)
    tradera(q)
