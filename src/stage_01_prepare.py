import argparse
import os
import shutil
import subprocess
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
from src.utils.data_mgmt import process_posts
import random

#Intiliaze logger and Stages

STAGE = "One"

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    filemode="a",
)

# intilize main function

def main(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    source_data = config["source_path"]
    input_data = config["param_path"]

    split = params["prepare"]["split"]
    input_data = os.path.join(source_data['data_dir'],source_data['data_file'])

    split = params["prepare"]["split"]
    seed = params["prepare"]["seed"]

    random.seed(seed)

    artifacts = config["artifacts"]
    prepared_data_dir = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["PREPARED_DATA"])
    create_directories(prepared_data_dir)

    # Create train, val, test splits

    train_data_dir = os.path.join(prepared_data_dir, artifacts["TRAIN_DATA"])
    test_data_dir = os.path.join(prepared_data_dir, artifacts["TEST_DATA"])


    encode = "utf-8"
    with open(input_data, "r", encoding=encode) as fd_in:
        with open(os.path.join(train_data_dir, "train.txt"), "w", encoding=encode) as  fd_out_train:
            with open(os.path.join(test_data_dir, "test.txt"), "w", encoding=encode) as fd_out_test:
                process_posts(fd_in, fd_out_train, fd_out_test, "<python>", split)


if __name__ == "__main__":
     parser = argparse.ArgumentParser(description="Prepare data for training")
     parser.add_argument("--config", "-c", default="configs/config.yaml", help="Path to config file")
     parser.add_argument("--params","-p", default="params.yaml", help="Path to params file")
     parsed_args = parser.parse_args()

     try:
         logging.info("\n****************")
         logging.info(f">>> stage {STAGE} started <<<< ")
         main(config_path=parsed_args.config, params_path=parsed_args.params)
         logging.info(f">>>> stage {STAGE} completed!<<<<")
        
     except Exception as e:
         logging.exception(e)
         raise e