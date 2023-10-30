
class Keyframe:
    def __init__(self, channel):
        self.channel = channel
        self.count = -1
        self.frame = -1

    def use_as_1(self):
        pass

    def use_as_2(self):
        pass

    def use_only(self):
        pass

    def get_count(self):
        return self.count

    def set_count(self, count: int):
        self.count = count

    def get_frame(self):
        return self.frame

    def set_frame(self, frame: int):
        self.frame = frame


class KeyframePosition(Keyframe):

    def __init__(self, channel, pos):
        super().__init__(channel)
        self.pos = pos

    def get_pos(self):
        return self.pos

    def use_as_1(self):
        self.channel.keyframe1 = self

    def use_as_2(self):
        self.channel.keyframe2 = self

    def use_only(self):
        self.channel.pos = self.pos


class KeyframeColor(Keyframe):

    def __init__(self, color):
        pass

