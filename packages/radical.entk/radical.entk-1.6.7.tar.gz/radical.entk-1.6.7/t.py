#!/usr/bin/env python3

import radical.entk  as re

if __name__ == '__main__':

    pipelines = set()
    for i in range(128):
        t = re.Task()
        t.executable = '/bin/date'

        s = re.Stage()
        s.add_tasks(t)

        p = re.Pipeline()
        p.add_stages(s)

        pipelines.add(p)


    amgr = re.AppManager(autoterminate=True, hostname='localhost', port=5672)
    amgr.resource_desc = {'resource': 'local.localhost',
                          'walltime': 10,
                          'cpus'    : 4}

    amgr.workflow = set(pipelines)
    amgr.run()
    amgr.terminate()

