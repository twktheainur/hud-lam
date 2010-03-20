from Name import Name
from matcher.RegExpMatcher import RegExpMatcher
class ModuleName(Name):
    string = "<module_name>"
    matcher = RegExpMatcher("[a-z_]+")
    def __init__(self,symbolStr):
        super(ModuleName,self).__init__(symbolStr)

    