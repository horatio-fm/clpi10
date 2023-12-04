
import argparse
import os


from clpi.version import version
__version__ = version


from clpi.pipes.dna import dna_pipe

def perform_analysis(list_of_tasks_to_execute):
    for task_iter, pipe_task in enumerate(list_of_tasks_to_execute):
        pipe_task.execute()


def main():

    parser = argparse.ArgumentParser(description='Description of clpi')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()

    out_dir = os.path.join(os.path.dirname(__file__), "..", "out")
    os.makedirs(out_dir, exist_ok=True)
    os.chdir(out_dir)
    perform_analysis(dna_pipe)


if __name__ == '__main__':
    main()

