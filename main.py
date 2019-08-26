from blocket import blocket
from tradera import tradera


def main(request):

    if request.args.get("q"):
        q = request.args.get("q")
    elif request.args.get("q") == "":
        return ("Specify query")
    else:
        return ("Specify query")

    if request.args.get("lan") not in [1, 2, 3] or not request.args.get("lan"):
        lan = 3
    else:
        lan = request.args.get("lan")

    blocket(q, lan)
    tradera(q)
