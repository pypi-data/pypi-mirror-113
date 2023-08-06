# encoding: UTF-8
import cmd
import os
import platform
import subprocess
import sys

from xhdata import __version__
from QUANTAXIS.QAUtil import QA_util_log_info
from xhdata.Command import save_tdx
from xhdata.Command import save_akshare
from xhdata.Command import save_jq


class CLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "XHData> "  # 定义命令行提示符

    def do_shell(self, arg):
        """run a shell commad"""
        print(">", arg)
        sub_cmd = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
        print(sub_cmd.communicate()[0])

    def do_version(self, arg):
        print(__version__)

    def help_version(self):
        print(
            "syntax: version [message]",
        )
        print("-- prints a version message")

    def do_quit(self, arg):  # 定义quit命令所执行的操作
        sys.exit(1)

    def help_quit(self):  # 定义quit命令的帮助输出
        print(
            "syntax: quit",
        )
        print("-- terminates the application")

    def do_clean(self, arg):
        try:
            if platform.system() == "Windows":
                os.popen("del back*csv")
                os.popen("del *log")
            else:
                os.popen("rm -rf back*csv")
                os.popen("rm -rf  *log")
        except:
            pass
        self.lastcmd = ""

    def help_clean(self):
        print("Clean the old backtest reports and logs")

    def do_exit(self, arg):  # 定义quit命令所执行的操作
        sys.exit(1)

    def help_exit(self):
        print("syntax: exit")
        print("-- terminates the application")

    def do_ls(self, arg):
        QA_util_log_info(os.path.dirname(os.path.abspath(__file__)))


def command():
    cli = CLI()
    cli.cmdloop()


# TDX通达信
class TdxCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "XHData-tdx> "  # 定义命令行提示符

    def print_save_usage(self):
        print(
            "Usage: \n\
            命令格式：save all \n\
            @XHData\n\
            "
        )

    def do_exit(self, arg):  # 定义quit命令所执行的操作
        sys.exit(1)

    def do_quit(self, arg):  # 定义quit命令所执行的操作
        sys.exit(1)

    def do_save(self, arg):
        arg = arg.split(" ")

        if len(arg) == 1 and arg[0] == "all":
            save_tdx.save_stock_list()
            save_tdx.save_stock_info()

            save_tdx.save_stock_day()
            save_tdx.save_stock_xdxr()

            save_tdx.save_etf_list()
            save_tdx.save_etf_day()

            save_tdx.save_index_list()
            save_tdx.save_index_day()
        else:
            try:
                eval("save_%s()" % (arg[0]))
            except:
                print("❌命令格式不正确！")
                self.print_save_usage()


def Tdx():
    cli = TdxCmd()
    cli.cmdloop()


# Tushare
class TushareCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "XHData-tushare> "  # 定义命令行提示符


def Tushare():
    cli = TushareCmd()
    cli.cmdloop()


# AKShare
class AKShareCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "XHData-akshare> "  # 定义命令行提示符

    def print_save_usage(self):
        print(
            "Usage: \n\
            命令格式：save all \n\
            @XHData\n\
            "
        )

    def do_exit(self, arg):  # 定义quit命令所执行的操作
        sys.exit(1)

    def do_quit(self, arg):  # 定义quit命令所执行的操作
        sys.exit(1)

    def do_save(self, arg):
        arg = arg.split(" ")

        if len(arg) == 1 and arg[0] == "all":
            # stock
            save_akshare.save_stock_list()
            save_akshare.save_stock_day()
            save_akshare.save_stock_fq_factor()

            # fund
            save_akshare.save_fund_list()
            save_akshare.save_fund_day()

            # index
            save_akshare.save_index_list()
            save_akshare.save_index_day()
        else:
            try:
                eval("save_%s()" % (arg[0]))
            except:
                print("❌命令格式不正确！")
                self.print_save_usage()


def AKShare():
    cli = AKShareCmd()
    cli.cmdloop()


# jq
class JqCmd(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "XHData-jq> "  # 定义命令行提示符

    def print_save_usage(self):
        print(
            "Usage: \n\
            命令格式：save all \n\
            @XHData\n\
            "
        )

    def do_exit(self, arg):  # 定义quit命令所执行的操作
        sys.exit(1)

    def do_quit(self, arg):  # 定义quit命令所执行的操作
        sys.exit(1)

    def do_save(self, arg):
        arg = arg.split(" ")

        if len(arg) == 1 and arg[0] == "all":
            save_jq.save_all_securities()

        else:
            try:
                eval("save_%s()" % (arg[0]))
            except:
                print("❌命令格式不正确！")
                self.print_save_usage()


def Jq():
    cli = JqCmd()
    cli.cmdloop()

