
import subprocess
import os
import time
from utils.system import decorate_exception


class SerialDownloader(object):

    def __init__(self):
        self.pre_bin_path = r""
        self.root_path = os.getcwd()
        self.script_path = os.path.join(self.root_path, "Utility")
        self.logs_path = os.path.join(self.root_path, "Logs", "Two_step")
        self.orig_log_folders = list()
        self.latest_log_folders = list()
        self.log_file = None
        self.log_path = None

    def get_orig_logs(self):
        log_dirs = os.listdir(self.logs_path)
        for item in log_dirs:
            if os.path.isfile(os.path.join(self.logs_path, item)):
                self.orig_log_folders.append(os.path.join(self.logs_path, item))

    def gen_cmd_line(self, com_port, fw_path, oakgate, pre_bin_path):
        command_line = "cd /d {} && python two_step_download.py --oakgate={} --firmwarePath={} --preBinPath={} --serialPort={}"\
            .format(self.script_path, oakgate, fw_path, pre_bin_path, com_port)
        return command_line

    def execute_command(self, cmd):
        ret = os.system(cmd)
        unused_err = ""
        return ret, unused_err

    def get_bin_path(self, fw_path, vol, commit):
        if os.path.isfile(fw_path):
            bin_path = fw_path
        else:
            bin_path = self.get_fw_path(fw_path, vol, commit)
        return bin_path

    def get_fw_path(self, fw_path, vol, commit):
        for file_name in os.listdir(fw_path):
            if os.path.isfile(os.path.join(fw_path, file_name)):
                if "_{}_".format(vol) in file_name and commit in file_name and file_name.endswith(".bin"):
                    return os.path.join(fw_path, file_name)
        return None

    def get_new_log(self):
        self.latest_log_folders = os.listdir(self.logs_path)
        new_logs = list()
        for item in self.latest_log_folders:
            log_item = os.path.join(self.logs_path, item)
            if os.path.isfile(log_item):
                if log_item not in self.orig_log_folders:
                    new_logs.append(log_item)
        return new_logs


    def create_error_log(self, content):
        error_log = os.path.join(self.logs_path, "error_{}.log".format(time.time()))
        err_file = open(error_log, "w")
        try:
            if type(content) is bytes:
                err_file.write(content.decode('utf-8', 'ignore'))
            else:
                err_file.write(str(content))
        except Exception as e:
            print("Write error failed", e)
        err_file.close()
        return error_log

    @decorate_exception
    def run(self, parameters):
        com_port = parameters["com"]
        fw_path = parameters["fw_path"]
        oakgate = parameters["ogt"]
        pre_bin_path = parameters["pre_bin"]
        vol = parameters["vol"]
        commit = parameters["commit"]
        self.get_orig_logs()
        bin_path = self.get_bin_path(fw_path, vol, commit)
        if bin_path is not None:
            command_line = self.gen_cmd_line(com_port, bin_path, oakgate, pre_bin_path)
            print(command_line)
            ret, unused_err = self.execute_command(command_line)
        else:
            ret = 1
            unused_err = ("Did not find fw bin at: {}".format(fw_path))
        error_log = self.create_error_log(unused_err)
        logs = self.get_new_log()
        logs.append(error_log)
        return ret, logs
