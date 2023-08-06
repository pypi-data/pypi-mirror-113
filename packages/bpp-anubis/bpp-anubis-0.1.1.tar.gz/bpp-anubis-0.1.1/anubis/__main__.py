# __main__.py
from datetime import datetime
import multiprocessing
from multiprocessing import Pool
import sys

# custom
from . import account_splitter
from . import feature_splitter
from . import arg_parser
from .parallelizer import command_generator
from . import results


def main():
    arguments = arg_parser.parse_arguments()
    # todo - create a temp directory that will store run data and be exported
    # delete old logs, results, and screenshots
    # for directory in ['logs', 'results', 'screenshots']:
    #     _empty_directory(
    #         directory_path=os.path.join('reports', directory),
    #         excluded_file_types=('.gitkeep', '.gitignore',)
    #     )

    # set up the multiple processes # todo - set spawn method based on os (macos -> fork; others -> default)
    multiprocessing.set_start_method('fork')
    pool = Pool(arguments.processes)

    # get account data available for parallel runs
    print('--- Parsing accounts')
    print(f'\tfile:              <{arguments.accounts_file}>')
    print(f'\tsection:           <{arguments.accounts_section}>')
    accounts_data = account_splitter.get_accounts(
        arguments.processes,
        arguments.accounts_file,
        arguments.accounts_section
    )

    # split up the features
    print('--- Grouping features')
    print(f'\tfeature directory: <{arguments.dir}>')
    print(f'\tincluded tags:     <{",".join([t for t in arguments.itags])}>')
    print(f'\texcluded tags:     <{",".join([t for t in arguments.etags])}>')
    account_feature_groups = feature_splitter.get_features(arguments, accounts_data)

    # run all the processes and save the locations of the result files
    print('--- Parallelizing')
    print(f'\tnum processes:     <{len(account_feature_groups)}>')
    res = pool.map(command_generator, account_feature_groups)

    # recombine everything
    print('---RECOMBINING RESULTS')
    try:
        results.create_aggregate(
            files=res,
            aggregate_out_file=arguments.res
        )
    except Exception as e:
        print(e)

    if arguments.sync_to:
        print(f'TODO: implement syncing to {arguments.sync_to}')

    if arguments.notify_to:
        print(f'TODO: implement notifying {arguments.notify_to}')


if __name__ == '__main__':
    args = arg_parser.parse_arguments()
    start = datetime.now()
    main()
    end = datetime.now()
    print('\n========================================')
    print(f'Envs:     <{",".join(args.env)}>')
    print(f'Browser:  <{args.browser}>')
    print(f'Branch:   <figure this out>')
    print(f'Run Time: <{(end - start)}>')
    print('========================================')

    sys.exit(0)
