# from pylint import epylint as lint  #TODO do we want to use pylint
# pep8 and autopep8 might be easier to start with
from analysis_bot import AnalysisBot


class StylistBot(AnalysisBot):
    """Check for bad coding style against style guides

    Current goal: check modified .py files in a pull request against
    PEP8 and prepare to leave a general comment in the pull request
    regarding whether the updated files passes the PEP8 check

    TODOs:
    need to investigate GitHub web-hooks
    need to know information about what pull request to work on and
    style to check against and decide how to retrieve such information
    (if we use web-hooks then info about the pull request probably need
    to be in the control flow and the interface will need to change)
    """

    def __init__(self, account):
        AnalysisBot.__init__(self, account, "StylistBot")

    def ready_to_analyze(self, project):
        # TODO probably makes sense to have the runtime pass in information
        # about the pull request to work on
        pass

    def analyze(self, project):
        # TODO probably makes sense to have the runtime pass in information
        # about the pull request to work on
        pass
