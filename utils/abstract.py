# To change this template, choose Tools | Templates
# and open the template in the editor.

def abstract(self):
        import inspect
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')