from json import dumps as json_dumps


class DetectionResult:
    def __init__(self, clones):
        """
        Initializes a new detection result given the list of detected clones.

        Arguments:
            clones {list[Detectedlone]} -- List of detected code clones.
        """

        self.clones = clones

        # TODO: Sort the clones by similarity and weight.

    def json(self):
        return json_dumps(self.clones)
