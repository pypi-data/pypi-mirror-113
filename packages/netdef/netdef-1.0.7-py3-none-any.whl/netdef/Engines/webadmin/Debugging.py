import tracemalloc
import gc
import os
import time

from flask_admin import expose
from netdef.Engines.webadmin.MyBaseView import MyBaseView
from netdef.Engines.webadmin import Views

@Views.register("Debugging")
def setup(admin, view=None):
    section = "webadmin"
    config = admin.app.config['SHARED'].config.config
    on = config(section, "debugging_on", 1)
    proj_path = os.path.join(config("proj", "path", "."), "log")


    if on:
        if not view:
            view = Debugging(
                name='Debugging',
                endpoint='debugging'
            )
            view.proj_path = proj_path
        admin.add_view(view)

class Debugging(MyBaseView):
    sn1 = None
    sn2 = None
    trace_type = "lineno"
    proj_path = "."
    @expose("/")
    def index(self):
        return self.render(
            'debugging.html'
        )

    @expose("/set_trace_type/<trace_type>")
    def set_trace_type(self, trace_type):
        if trace_type == "lineno":
            self.trace_type = "lineno"
            return "<p>trace_type changed to lineno </p>"
        elif trace_type == "filename":
            self.trace_type = "filename"
            return "<p>trace_type changed to filename </p>"
        elif trace_type == "traceback":
            self.trace_type = "traceback"
            return "<p>trace_type changed to traceback </p>"
        else:
            return "<p> supported types: lineno, filename, traceback  </p>"

    @expose("/traceback_current/<lineno>")
    def traceback_current(self, lineno):
        if self.sn1 is None:
            return "<p>take snapshot first</p>"

        lineno = int(lineno)

        traces = self.sn1.statistics(self.trace_type)
        traces_len = len(traces)
        help_str = "<p>lineno must be between 0 and {} </p>\n".format(traces_len)
        if lineno < -1 or lineno >= traces_len:
           return help_str
        elif (lineno == -1):
             return help_str + "<br>\n".join( ["<a href='./{0}'>{0}</a>: {1}".format(i, l) for i, l in enumerate(traces[:1000])] )

        stat = traces[lineno]
        retn = str(stat) + "<br>\n"
        for line in stat.traceback.format():
            retn += (line + "<br>\n")
        return retn

    @expose("/traceback_compare/<lineno>")
    def traceback_compare(self, lineno):
        if self.sn2 is None:
            return "<p>take two snapshots first</p>"

        lineno = int(lineno)
        traces = self.sn1.compare_to(self.sn2, self.trace_type)
        traces_len = len(traces)
        help_str = "<p>lineno must be between 0 and {} </p>\n".format(traces_len)
        if lineno < -1 or lineno >= traces_len:
           return help_str
        elif (lineno == -1):
             return help_str + "<br>\n".join( ["<a href='./{0}'>{0}</a>: {1}".format(i, l) for i, l in enumerate(traces[:1000])] )

        stat = traces[lineno]
        retn = str(stat) + "<br>\n"
        for line in stat.traceback.format():
            retn += (line + "<br>\n")
        return retn


    @expose("/trace_top_50/")
    def trace_top_50(self):
        if self.sn1 is None:
            return "<p>take snapshot first</p>"
        top_stats = self.sn1.statistics(self.trace_type)
        return "<br>\n".join( [str(i) for i in top_stats[:50]] )

    @expose("/take_snapshot/")
    def take_snapshot(self):
        if not tracemalloc.is_tracing():
            return "<p>tracemalloc is not running </p>"
        self.sn2 = self.sn1
        self.sn1 = tracemalloc.take_snapshot()
        top_stats = self.sn1.statistics(self.trace_type)
        return "<br>\n".join( [str(i) for i in top_stats[:50]] )

    @expose("/compare_top_50/")
    def compare_top_50(self):
        if self.sn2 is None:
            return "<p>take two snapshots first</p>"
        top_stats = self.sn1.compare_to(self.sn2, self.trace_type)
        return "<br>\n".join( [str(i) for i in top_stats[:50]] )

    @expose("/save_snapshot/")
    def save_snapshot(self):
        if self.sn1 is None:
            return "<p>take snapshot first</p>"
        fn = os.path.join(self.proj_path, time.strftime("%Y_%m_%d_%H_%M_%S") + ".tracedump")
        self.sn1.dump(fn)
        return "<p> saved at: {} </p>".format(fn)

    @expose("/trace_start/")
    def trace_start(self):
        tracemalloc.start(10)
        return "<p>tracemalloc started</p>"

    @expose("/trace_stop/")
    def trace_stop(self):
        tracemalloc.stop()
        return "<p>tracemalloc stopped</p>"

    @expose("/gc_collect/")
    def gc_collect(self):
        res = gc.collect()
        return "<p>res: {}</p>".format(res)
