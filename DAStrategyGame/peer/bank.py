class Bank():
    def __init__(self):
        self.cdkey_list = dict()

    # create balance record
    def create_balance(self, cdkey, balance):
        try:
            # 0 and no this key can created
            if cdkey in self.cdkey_list:
                if self.cdkey_list[cdkey] != 0:
                    return "active number get used"
            self.cdkey_list[cdkey] = balance
            return "succeed creating"
        except Exception, e:
            print e

    # activate balance record
    def activate_cdkey(self, cdkey):
        try:
            # 0-used, other- active
            if cdkey not in self.cdkey_list:
                return "invalid active number"
            if self.cdkey_list[cdkey] != 0:
                balance = self.cdkey_list[cdkey]
                self.cdkey_list[cdkey] = 0
                return balance
            else:
                return "active number has been used by others"
        except Exception, e:
            print e

    # delete balance record
    def delete_balance(self, cdkey):
        try:
            # 0-used, other- active
            if cdkey not in self.cdkey_list:
                return "invalid active number"
            del(self.cdkey_list[cdkey])
            return "delete active_no"
        except Exception, e:
            print e