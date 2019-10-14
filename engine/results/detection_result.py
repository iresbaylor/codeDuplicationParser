"""Module containing the `DetectionResult` class for final results of detection."""

from json import dumps as json_dumps


class DetectionResult:
    """
    Representation of the final result of a detection query.

    For now it only contains a list of detected clones,
    but more information may be added in the future.

    Attributes:
        clones {list[DetectedClone]} -- List of detected code clones ordered
                                        by their significance (see __init__).

    """

    def __init__(self, clones):
        """
        Initialize a new detection result given the list of detected clones.

        The list of code clones will be copied and the copy will be sorted by
        the clones' weight of their matching subtrees.
        The original list of clones will not be modified in any way.

        Arguments:
            clones {list[DetectedClone]} -- List of detected code clones.

        """
        self.clones = clones.copy()
        self.clones.sort(reverse=True, key=lambda c: c.match_weight)

    def json(self):
        """
        Convert the detection result into a JSON.

        This includes information about all detected code clones.

        Returns:
            string -- JSON representation of the detection result.

        """
        return json_dumps([c.dict() for c in self.clones])
