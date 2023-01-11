from Python.gui.gui import ConverterWindow

class InvalidSegmentCount(Exception):
    pass
class Segment:

    # cur = current ind of seg, max = seg count
    # step = step size per seg, prev = progress when segs created
    def __init__(self, cur, max, step, prev):
        self.cur = cur
        self.max = max
        self.step = step
        self.prev = prev



class ProgressBar:

    data = []
    cur_segment = None
    title = ""
    subtext = ""
    progress = 0

    def __init__(self):
        pass
        
    def segment(self, count):
        if count <= 0:
            raise InvalidSegmentCount("You must have at least one segment!")
        if len(self.data) == 0:
            self.cur_segment = Segment(0, 1000, 1000 / count, 0)
            ConverterWindow.get_instance().connection.set_progress_max.emit(1000)
            ConverterWindow.get_instance().connection.set_progress.emit(0)
        else:
            s = self.cur_segment
            self.cur_segment = Segment(0, count, s.step / count, self.progress)

        self.updateText()
        self.data.append(self.cur_segment)

    def increment(self):
        if not self.data:
            return

        s = self.cur_segment
        if s.cur >= s.max - 1:
            self.data.pop()
            if self.data:
                self.cur_segment = self.data[-1]
                s = self.cur_segment
                self.increment()
            else:
                self.progress = s.max
                # self.setText("Done!")
        else:
            s.cur += 1
            self.progress = (s.cur * s.step) + s.prev

        ConverterWindow.get_instance().connection.set_progress.emit(int(self.progress))
        self.updateText()

    def reset(self):
        self.progress = 0
        self.data.clear()
        ConverterWindow.get_instance().connection.set_progress.emit(0)

    def setSubtext(self, txt):
        self.subtext = txt
        self.updateText()
        pass

    def updateText(self):
        suffix = (
            ""
            if len(self.data) <= 1
            else f" ({self.cur_segment.cur+1}/{self.cur_segment.max})"
        )
        ConverterWindow.get_instance().connection.update_text.emit(f"{self.title}{self.subtext}{suffix}")

    def setText(self, title="", text=""):
        self.title = title
        self.subtext = text
        self.updateText()

    def setTitle(self, txt):
        self.title = txt
        self.updateText()

    def inc(self):
        self.increment()
