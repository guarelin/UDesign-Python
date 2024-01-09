from keyframes import Keyframe, KeyframePosition, KeyframeColor
from timeline import FRAME_RATE

class Channel:
    keyframes: [Keyframe]

    keyframe1_idx: int
    keyframe2_idx: int

    def __init__(self, performer, timeline):
        self.keyframes = []
        self.performer = performer
        self.timeline = timeline

        self.keyframe1_idx = -1
        self.keyframe2_idx = -1

    def insert_keyframe(self, keyframe: Keyframe):
        if self.keyframe1_idx > -1:
            k1 = self.keyframes[self.keyframe1_idx]

        current_frame = self.timeline.get_current_frame()
        keyframe.set_frame(current_frame)
        keyframe.set_count(self.timeline.get_current_count())

        if self.keyframe1_idx < 0:
            # No first keyframe so we are either:
            # Before any keyframes or there are none
            action = 'insert' if self.keyframe2_idx >= 0 else 'append'
        else:
            # We know keyframe1 is valid so we are after it
            frame1 = k1.get_frame()
            if self.keyframe2_idx < 0:
                # There is no second keyframe
                # If we are after the current frame, append
                # If we are on it, replace
                action = 'append' if frame1 < current_frame else 'replace'
            else:
                # There is a second keyframe
                # If we are before the first frame, we insert
                # If not, we replace
                action = 'insert' if frame1 < current_frame else 'replace'

        print(action)

        if action == 'append':
            # Add to the end
            # Left keyframe becomes the new one
            self.keyframes.append(keyframe)
            self.keyframe1_idx = len(self.keyframes) - 1
        elif action == 'replace':
            # Replace the current keyframe
            self.keyframes[self.keyframe1_idx] = keyframe
        elif action == 'insert':
            # Insert after keyframe1
            # Left keyframe becomes new keyframe (we are on it)
            self.keyframes.insert(self.keyframe1_idx + 1, keyframe)
            self.keyframe1_idx += 1

    def set_frame(self, current_frame: int):
        print(f'setting frame {current_frame}, {self.keyframe1_idx}, {self.keyframe2_idx}')
        while self.keyframe2_idx >= 0 and self.keyframes[self.keyframe2_idx].get_frame() <= current_frame:
            # move forward in time
            self.keyframe1_idx = self.keyframe2_idx
            self.keyframe2_idx += 1
            if self.keyframe2_idx >= len(self.keyframes):
                self.keyframe2_idx = -1
            print(f'move forward, {self.keyframe1_idx}, {self.keyframe2_idx}')

        while self.keyframe1_idx >= 0 and self.keyframes[self.keyframe1_idx].get_frame() > current_frame:
            # move backward in time
            self.keyframe2_idx = self.keyframe1_idx
            self.keyframe1_idx -= 1
            print(f'move backward, {self.keyframe1_idx}, {self.keyframe2_idx}')

        # Now, four possibilities
        if self.keyframe1_idx >= 0 and self.keyframe2_idx >= 0:
            # Between two keyframes, so we tween
            self.keyframes[self.keyframe1_idx].use_as_1()
            self.keyframes[self.keyframe2_idx].use_as_2()

            time1 = self.keyframes[self.keyframe1_idx].get_frame() / FRAME_RATE
            time2 = self.keyframes[self.keyframe2_idx].get_frame() / FRAME_RATE

            t = (self.timeline.get_current_time() - time1) / (time2 - time1)
            self.tween(t)
        elif self.keyframe1_idx >= 0:
            # Only using keyframe 1
            self.keyframes[self.keyframe1_idx].use_only()
        elif self.keyframe2_idx >= 0:
            # Only using keyframe 2
            self.keyframes[self.keyframe2_idx].use_only()

    def clear_keyframe(self):
        # There is no keyframe1
        if self.keyframe1_idx < 0:
            return
        else:
            k1 = self.keyframes[self.keyframe1_idx]

        count_kf1 = k1.get_count()
        curr_count = self.timeline.get_current_count()

        if count_kf1 != curr_count:
            return

        del self.keyframes[self.keyframe1_idx]
        self.keyframe1_idx -= 1

        if self.keyframe2_idx >= 0:
            self.keyframe2_idx -= 1

    def tween(self, t):
        pass

    def draw_keyframes(self):
        pass


class ChannelPosition(Channel):
    holding: bool

    def __init__(self, performer, timeline):
        super().__init__(performer, timeline)

        self.holding = False
        self.pos = (0, 0)

    def set_keyframe(self, pos):
        new_keyframe = KeyframePosition(channel=self, pos=pos)
        self.insert_keyframe(new_keyframe)

    def tween(self, t):
        k1, k2 = self.keyframes[self.keyframe1_idx], self.keyframes[self.keyframe2_idx]

        if self.holding:
            self.pos = k1.get_pos()
        else:
            a_x, a_y = k1.get_pos()
            b_x, b_y = k2.get_pos()

            self.pos = (a_x + t * (b_x - a_x), a_y + t * (b_y - a_y))
            print(self.pos)
            self.performer.setPos(self.pos[0], self.pos[1])

    def get_pos(self):
        return self.pos

    def draw_keyframes(self):
        # as a placeholder, we'll return a string
        k_strs = []
        for i, k in enumerate(self.keyframes):
            k_strs.append(f'({i}, {k.count}, {k.frame}, ({k.pos[0]}, {k.pos[1]}))')
        return ','.join(k_strs)
