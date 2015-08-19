from abc import ABCMeta, abstractmethod


class AnalysisBot(metaclass=ABCMeta):
    """Base class for different kinds of Analysis Bots
    """

    # TODO: probably want factory method to instantiate the 
    #       different bots to load bots dynamically and 
    #       avoid multiple instances of the same bot 

    def __init__(self, account, name):
        self.account = account
        self.name = name

    def get_name(self):
        """return string - the name of the analysis"""
        return name

    @abstractmethod
    def ready_to_analyze(self, repo):
        """return True if a repo is ready to be analyzed
        or return what needs to be done for it to be ready

        TODO maybe change this so that it returns the operations needed
        for it to be ready to analyze
        """
        pass

    @abstractmethod
    def analyze(self, repo): 
        """analyze the repo and puts necessary information into 
        the datastore for further operations to be carried out

        assumes self.ready_to_analyze(repo)
        information stored in the datastore will let the runtime
        know to create pull request or comment or whatever

        how to store the information, the format, and how the runtime
        will handle the different possible formats used by different 
        bots are yet to be determined
        """
        pass