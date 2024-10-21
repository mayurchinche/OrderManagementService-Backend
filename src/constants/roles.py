class Roles:

    EMPLOYEE = ['employee', 'manager', 'po_team']
    ONLY_MANAGER = ['manager']
    ONLY_PO_TEAM = ['po_team']
    MANAGER_AND_PO_TEAM = ['manager', 'po_team']


    def get_roles(self):
        return [self.EMPLOYEE, self.MANAGER, self.PO_TEAM]