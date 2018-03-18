class User(object):
    def __init__(self,user_id,role,telephone,image_src,name,sign,acc_point,account_name,reg_date):
        self.user_id=user_id
        self.role=role
        self.telephone=telephone
        self.image_src=image_src
        self.name=name
        self.sign=sign
        self.acc_point=acc_point
        self.account_name=account_name
        self.reg_date=reg_date.timestamp()