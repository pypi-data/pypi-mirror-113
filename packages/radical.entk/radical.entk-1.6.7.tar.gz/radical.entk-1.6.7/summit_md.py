import os, json, time
from radical.entk import Pipeline, Stage, Task, AppManager

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') is None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

# Assumptions:
# - # of MD steps: 2
# - Each MD step runtime: 15 minutes
# - Summit's scheduling policy [1]
#
# Resource rquest:
# - 4 <= nodes with 2h walltime.
#
# Workflow [2]
#
# [1] https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-user-guide/scheduling-policy
# [2] https://docs.google.com/document/d/1XFgg4rlh7Y2nckH0fkiZTxfauadZn_zSn3sh51kNyKE/
#
RMQ_HOSTNAME = 'two.radical-project.org'
RMQ_PORT     = 33235
'''
export RADICAL_PILOT_DBURL=mongodb://hyperrct:h1p3rrc7@two.radical-project.org:27017/hyperrct
export RADICAL_PILOT_PROFILE=True
export RADICAL_ENTK_PROFILE=True
'''
#


N_jobs_MD = 12
N_jobs_ML = 10

hrs_wt = 2  # walltime in hours
queue = 'batch'

CUR_STAGE = 0
MAX_STAGE = 0  # 10
RETRAIN_FREQ = 5

LEN_initial = 10  # 100 initial stage sim time in ns
LEN_iter = 10


def generate_training_pipeline():
    """
    Function to generate the CVAE_MD pipeline
    """

    def generate_MD_stage(num_MD=1):
        """
        Function to generate MD stage.
        """
        s1 = Stage()
        s1.name = 'MD'

        # MD tasks
        for i in range(num_MD):
            t1 = Task()
            t1.executable = ['/bin/sleep']
            t1.arguments  = ['3']

            # assign hardware the task
            t1.cpu_reqs = {'processes': 1,
                           'process_type': None,
                           'threads_per_process': 4,
                           'thread_type': 'OpenMP'
                          }
            t1.gpu_reqs = {'processes': 1,
                           'process_type': None,
                           'threads_per_process': 1,
                           'thread_type': 'CUDA'
                          }

            # Add the MD task to the simulating stage
            s1.add_tasks(t1)
        return s1


    def generate_aggregating_stage():
        """
        Function to concatenate the MD trajectory (h5 contact map)
        """
        s2 = Stage()
        s2.name = 'aggregating'

        # Aggregation task
        t2 = Task()
        t2.executable = ['/bin/sleep']
        t2.arguments = ['3']

        # Add the aggregation task to the aggreagating stage
        s2.add_tasks(t2)
        return s2


    def generate_ML_stage(num_ML=1):
        """
        Function to generate the learning stage
        """
        s3 = Stage()
        s3.name = 'learning'

        # learn task
        time_stamp = int(time.time())
        for i in range(num_ML):
            t3 = Task()
            t3.executable = ['/bin/sleep']
            t3.arguments = ['3']
            t3.cpu_reqs = {'processes': 1,
                           'process_type': None,
                           'threads_per_process': 4,
                           'thread_type': 'OpenMP'
                          }
            t3.gpu_reqs = {'processes': 1,
                           'process_type': None,
                           'threads_per_process': 1,
                           'thread_type': 'CUDA'
                          }

            # Add the learn task to the learning stage
            s3.add_tasks(t3)

        # TICA jobs
        for i in range(num_ML):
            t3 = Task()
            t3.executable = ['/bin/sleep']
            t3.arguments = ['3']

            t3.cpu_reqs = {'processes': 1,
                           'process_type': None,
                           'threads_per_process': 4,
                           'thread_type': 'OpenMP'
                          }
            # Add the learn task to the learning stage
            s3.add_tasks(t3)

        return s3


    def generate_interfacing_stage():
        s4 = Stage()
        s4.name = 'scanning'

        # Scaning for outliers and prepare the next stage of MDs
        t4 = Task()
        t4.executable = ['/bin/sleep']
        t4.arguments = ['3']

        t4.cpu_reqs = {'processes': 1,
                       'process_type': None,
                       'threads_per_process': 12,
                       'thread_type': 'OpenMP'
                      }
        t4.gpu_reqs = {'processes': 1,
                       'process_type': None,
                       'threads_per_process': 1,
                       'thread_type': 'CUDA'
                      }
        s4.add_tasks(t4)
        s4.post_exec = func_condition

        return s4


    def func_condition():

        global CUR_STAGE, MAX_STAGE
        if CUR_STAGE < MAX_STAGE:
            func_on_true()
        else:
            func_on_false()


    def func_on_true():
        global CUR_STAGE, MAX_STAGE
        print ('finishing stage %d of %d' % (CUR_STAGE, MAX_STAGE) )

        # --------------------------
        # MD stage
        s1 = generate_MD_stage(num_MD=N_jobs_MD)
        # Add simulating stage to the training pipeline
        p.add_stages(s1)

        if CUR_STAGE % RETRAIN_FREQ == 0:
            # --------------------------
            # Aggregate stage
            s2 = generate_aggregating_stage()
            # Add the aggregating stage to the training pipeline
            p.add_stages(s2)

            # --------------------------
            # Learning stage
            s3 = generate_ML_stage(num_ML=N_jobs_ML)
            # Add the learning stage to the pipeline
            p.add_stages(s3)

        # --------------------------
        # Outlier identification stage
        s4 = generate_interfacing_stage()
        p.add_stages(s4)

        CUR_STAGE += 1

    def func_on_false():
        print ('Done' )


    global CUR_STAGE

    p = Pipeline()
    p.name = 'MD_ML'

    func_on_true()

    return p


if __name__ == '__main__':

    # Create a dictionary to describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {
            'resource': 'local.localhost',
          # 'queue'   : queue,
            'schema'  : 'local',
            'walltime': 60 * hrs_wt,
            'cpus'    : N_jobs_MD * 7,
            'gpus'    : N_jobs_MD,  # 6 * 2,

          # 'resource': 'ornl.summit',
          # 'queue'   : queue,
          # 'schema'  : 'local',
          # 'walltime': 60 * hrs_wt,
          # 'cpus'    : N_jobs_MD * 7,
          # 'gpus'    : N_jobs_MD,  # 6 * 2,
          # 'project' : 'LRN005',
    }

    # Create Application Manager
    # appman = AppManager()
    appman = AppManager(hostname=RMQ_HOSTNAME, port=RMQ_PORT)
    appman.resource_desc = res_dict

    p1 = generate_training_pipeline()

    appman.workflow = [p1]

    appman.run()

