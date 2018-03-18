class Comment(object):
    def __init__(self,comm_rec_id,rec_id,commer,content,appr_num,comm_date):
        self.comm_rec_id=comm_rec_id
        self.rec_id=rec_id
        self.commer=commer
        self.content=content
        self.appr_num=appr_num
        self.comm_date=comm_date.timestamp()