class SentenceInfo:
    def __init__(self, index, audio, ans, scp, fail, need_cut, status, **kwargs):
        self.index = index
        self.ans = self.ans_raw = ans
        self.itn = ''
        self.scp = scp
        self.audio_location = '/'.join([audio, scp])
        self.fail = fail
        self.need_cut = need_cut
        self.error = False
        self.status = status
        self.cutter_id = None

    def set_itn(self, value):
        self.itn = value
        return self

    def set_cutter_id(self, value):
        self.cutter_id = value
        return self

    def set_scp(self, value):
        self.scp = value
        return self

    def set_error(self):
        self.error = True
        return self

    def set_root_ans(self, value):
        self.root_ans = value
        return self

    def set_fail(self, value):
        self.fail = value
        return self

    def set_need_cut(self, value):
        self.need_cut = value
        return self

    def __str__(self):
        return f'{self.index} - {self.scp}: {self.ans}.\nLocation: {self.audio_location}'


