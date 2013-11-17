import os
import sys
import cPickle as pickle
import logging
import tarfile
import cPickle as pickle

def do_work_on_compute_node(work_dir):
    print "HOLY CRAP LOAD THE DATA AND DO THE THING"
    
    # Extract the necessary dependencies
    extract_packages_archive(work_dir)

    # Open up the pickle file with the work to be done
    os.chdir(work_dir)
    with open("job-instance.pickle", "r") as f:
        job = pickle.load(f)

    # Do the work contained
    job.work()

def extract_packages_archive(work_dir):
    package_file = os.path.join(work_dir, "packages.tar")
    if not os.path.exists(package_file):
        return

    curdir = os.path.abspath(os.curdir)

    os.chdir(work_dir)
    tar = tarfile.open(package_file)
    for tarinfo in tar:
        tar.extract(tarinfo)
    tar.close()
    if '' not in sys.path:
        sys.path.insert(0, '')

    os.chdir(curdir)


def main(args=sys.argv):
    """Run the work() method from the class instance in the file "job-instance.pickle".
    """
    try:
        # Set up logging.
        work_dir = args[1]
        assert os.path.exists(work_dir), "First argument to lsf_runner.py must be a directory that exists"
        do_work_on_compute_node(work_dir)
    except Exception, exc:
        # Dump encoded data that we will try to fetch using mechanize
        print(exc)
        raise

if __name__ == '__main__':
    main()