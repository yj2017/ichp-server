class Record(object):
    def __init__(self, rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str):
        self.rec_id = rec_id
        self.recorder = recorder
        self.title = title
        self.url = url
        self.type = type
        self.addr = addr
        self.appr_num = appr_num
        self.comm_num = comm_num
        self.issue_date = issue_date.timestamp()
        self.discribe = discribe
        self.labels_id_str=labels_id_str
    def __eq__(self,other):
        return self.rec_id==other.rec_id
    def __hash__(self):
        return self.rec_id

