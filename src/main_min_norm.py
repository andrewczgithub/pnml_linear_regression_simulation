import argparse
import json
import os.path as osp

from experimnet_utils import execute_x_vec
from logger_utils import Logger
from pnml_min_norm_utils import PnmlMinNorm


def execute_experiment(params):
    # Create logger and save params to output folder
    logger = Logger(experiment_type='pnml_min_norm', output_root=params['output_dir_base'])
    logger.info('OutputDirectory: %s' % logger.output_folder)
    with open(osp.join(logger.output_folder, 'params.json'), 'w', encoding='utf8') as outfile:
        outfile.write(json.dumps(params, indent=4, sort_keys=True))
    logger.info(json.dumps(params, indent=4, sort_keys=True))

    # Build pNML
    pnml_h = PnmlMinNorm()

    # Iterate on poly degree
    for poly_degree in params['poly_degree_list']:
        execute_x_vec(pnml_h, poly_degree, lamb=0.0, params=params, out_dir=logger.output_folder)
    logger.info('Finished. Save to: %s' % logger.output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-config',
                        default=osp.join('..', 'configs', 'min_norm_simulation.json'),
                        help='path to configuration file')
    args = parser.parse_args()

    with open(args.config) as file:
        params_user = json.load(file)
    execute_experiment(params_user)
