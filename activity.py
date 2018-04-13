class Activity(object):
    def __init__(self,act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date,image_src,labels_id_str):
        self.act_id=act_id
        self.publisher=publisher
        self.title=title
        self.content=content
        self.hold_date=hold_date.timestamp()
        self.hold_addr=hold_addr
        self.act_src=act_src
        self.issue_date=issue_date.timestamp()
        self.image_src=image_src
        self.labels_id_str=labels_id_str
    