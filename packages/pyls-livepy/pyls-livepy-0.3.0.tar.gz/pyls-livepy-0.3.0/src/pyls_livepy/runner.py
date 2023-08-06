# Copyright (c) 2021  Andrew Phillips <skeledrew@gmail.com>

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

"""


import doctest
import json
from pathlib import Path
import shlex
import subprocess as sp
import sys
import types

from pyls_livepy import __version__ as plr_version
from pyls_livepy.tracer import trace_and_report, get_traces
from pyls_livepy.utils import (
    _mark_err,
    LivepyError,
    logger,
    set_log_level,
)


class PytestException(BaseException):
    """Signal exceptions specific to the pytest case runner."""
    pass


class PytestCaseRunnerSuccess(BaseException):
    """Signal successful case run.

    A hack to avoid the failure message, caused by the report output.
    """
    # TODO: find a proper way to ignore a passing result
    pass


class CapDocTestRunner(doctest.DocTestRunner):
    def report_failure(self, out, test, example, got):
        res = {
            "type": "failure",
            "test": test,
            "example": example,
            "got": got,
        }
        out(res)
        return

    def report_unexpected_exception(self, out, test, example, exc_info):
        res = {
            "type": "exception",
            "test": test,
            "example": example,
            "exc_info": exc_info,
        }
        out(res)
        return

    def report_success(self, out, test, example, got):
        res = {
            "type": "success",
            "test": test,
            "example": example,
            "got": got,
        }
        out(res)
        return

    def report_start(self, out, test, example):
        return


class PytestCaseRunner:
    _mut = None
    mname = __name__

    def __call__(self, argstr):
        return _run_pytest_case(argstr, self._mut)

    def set_mut(self, module):
        self._mut = module
        return


def _get_stdin():
    return "".join([ln for ln in sys.stdin])


def _put_stdout(out):
    sys.stdout.write(out)
    return


def capout(hold=None):
    """Capture values as a callable and return them elsewhere."""
    hold = hold or []

    def inner(val=NotImplemented):
        nonlocal hold
        if val is NotImplemented:
            return hold

        else:
            hold.append(val)
        return

    return inner


def run_doctests(src, mut_path, which=None):
    """Run the doctests in a document."""
    run_env = sp.run(
        ["bash", "-c", "which pyls-livepy-runner"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    logger.info(f'Runner at "{run_env}"')
    mod = types.ModuleType("rdt_mut")  # TODO: get name from document
    mod.__file__ = mut_path
    w_path = "\n  ".join(sys.path)
    logger.info(f"Working PATH:\n  {w_path}\n")

    try:
        exec(src, mod.__dict__)

    except Exception as e:
        logger.exception(f"Exception while exec'ing MUT: {repr(e)}")
        return {}
    doctests = doctest.DocTestFinder().find(mod)
    runner = CapDocTestRunner()
    results = {}

    for dt in doctests:
        # TODO: allow filtering by 'which'
        if not dt.examples:
            continue
        _maybe_update(dt, mod)
        co = capout()
        res = runner.run(dt, out=co)._asdict()
        bad = [
            tr for tr in co()
            if tr["type"] in ["failure", "exception"]
            and (
                not isinstance(tr["exc_info"][1], PytestCaseRunnerSuccess)
                if "exc_info" in tr else True
            )
        ]
        res["out"] = bad
        res["traces"] = {
            "name": dt.name,
            "data": trace_and_report(src, dt, mut_path),
        }
        results[dt.name] = res
    return results


def create_markers(results):
    """Create diagnostic lint markers for failing doctests."""
    err_msg = f"Expected a dict but got {type(results).__name__}"
    assert isinstance(results, dict), err_msg
    markers = []

    for name, res in results.items():
        out = res["out"]

        for tr in out:
            ex = tr["example"]
            lineno = tr["test"].lineno + ex.lineno
            offset = ex.indent + 4
            err_range = {
                "start": {"line": lineno, "character": offset},
                "end": {
                    "line": lineno,
                    "character": offset + len(ex.source) - 1,
                },
            }
            rtype = tr['type']
            lim = 79

            if rtype == "exception":
                msg = str(tr["exc_info"][1])
                msg = msg[:lim-3] + "..." if len(msg) > lim else msg

            elif rtype == "failure":
                msg = "failure in doctest"
                got = tr["got"]
                logger.info(f"{msg}\n\nWANT:\n{ex.want}\n\nGOT:\n{got}")
                ok = len(got) <= lim and "\n" not in got
                msg = f"GOT: {got}" if ok else msg + "; see log"
            marker = {
                "source": "livepy",
                "range": err_range,
                "message": msg,
                "severity": 1,  # lsp.DiagnosticSeverity.Error,
            }
            markers.append(marker)
    return markers


def run():
    """Run doctests and print diagnostic markers.

    Only accepts input from stdin and writes output as JSON to stdout."""
    run_data = json.loads(_get_stdin().rpartition("\n")[2])
    src = run_data["source"]
    plp_version = run_data["plp_version"]
    log_level = run_data["log_level"]
    mut_path = run_data["mut_path"]
    set_log_level(log_level, logger)
    logger.debug(f'sys.prefix = "{sys.prefix}"')
    logger.info(f'Runner active at "{Path(__file__).parent}"')

    if plp_version == plr_version:
        t_results = run_doctests(src, mut_path)
        markers = create_markers(t_results)
        traces = get_traces(t_results)
        results = {
            "markers": markers,
            "traces": traces,
        }

    else:
        err = "version mismatch error; "
        err += f"plugin: {plp_version} vs runner: {plr_version}"
        logger.error(repr(LivepyError(err)))
        results = [_mark_err(src, err)]
    _put_stdout("\n\n" + json.dumps(results))
    return


def _perform_collect_wrapper(self, args=None, genitems=True):
    """Modify wrapped's return value."""
    try:
        items = self._wrapped_perform_collect(args, genitems)
        mut = self._mut
        assert mut is not None, "MUT transfer failed"
        # NOTE: assumes MUT name is MUT tester name with test prepended
        # TODO: should prob get the name from sys.modules or so
        mutt_name = items[0].module.__name__

        mut_name = mutt_name.partition("_")[2]
        mut.__name__ = getattr(items[0].module, mut_name).__name__
        mut.__file__ = getattr(items[0].module, mut_name).__file__
        setattr(items[0].module, mut_name, mut)
        items[0]._reportscap = self._reportscap

    except Exception as e:
        logger.exception(repr(e))
        raise
    return items


def _runtestprotocol_wrapper(item, log=True, nextitem=None):
    """Capture test results from runtestprotocol."""
    import _pytest.runner

    reports = _pytest.runner._wrapped_runtestprotocol(item, log, nextitem)
    item._reportscap(reports)
    return reports


def _maybe_update(doctest, module):
    """Maybe apply changes to the doctest before running it."""
    import ast

    upd = False
    rpc_imp = ""

    for ex in doctest.examples:
        pex = ast.parse(ex.source)

        for node in ast.walk(pex):
            imp = isinstance(node, ast.Import)
            impf = isinstance(node, ast.ImportFrom)
            impf = impf and node.module == "pyls_livepy"
            rpc_call = isinstance(node, ast.Call)
            rpc_call = rpc_call and getattr(node.func, "id") == rpc_imp

            if rpc_call:
                ex.want = ""
                break

            if imp or impf and any([
                    n.name in [
                        "run_pytest_case",
                        "pyls_livepy.run_pytest_case",
                    ]
                    for n in node.names
            ]):
                rpc_imp = [
                    n.asname if n.asname else n.name
                    for n in node.names if n.name in [
                            "run_pytest_case",
                            "pyls_livepy.run_pytest_case",
                    ]
                ][0]
                exec(ex.source, doctest.globs)
                rpc = doctest.globs[rpc_imp]
                rpc.set_mut(module)
                assert rpc._mut, "MUT set failed or none given"
                upd = True
                break
    return upd


def _run_pytest_case(argstr, mut):
    """Run the pytest case specified by argstr.

    Patches pytest to insert the updated module and collect the test result.

    >>> from pyls_livepy import run_pytest_case
    >>> run_pytest_case("-k run_doctests")
    """

    try:
        import _pytest
        # NOTE: hack to prevent AttributeError
        import _pytest.main as pm
        pm

    except ModuleNotFoundError:
        raise PytestException("pytest must be installed to use this function")
    Session = _pytest.main.Session
    runner = _pytest.runner
    reportscap = capout()
    Session._reportscap = lambda *a: reportscap(a[1] if a else NotImplemented)

    Session._wrapped_perform_collect = Session.perform_collect
    Session.perform_collect = _perform_collect_wrapper
    Session._mut = mut
    runner._wrapped_runtestprotocol = runner.runtestprotocol
    runner.runtestprotocol = _runtestprotocol_wrapper
    args = shlex.split(argstr)
    _pytest.config.main(args)
    Session.perform_collect = Session._wrapped_perform_collect
    del Session._wrapped_perform_collect
    runner.runtestprotocol = runner._wrapped_runtestprotocol
    del runner._wrapped_runtestprotocol
    captured = reportscap()

    if len(captured) != 1:
        raise PytestException(f"{len(captured)} reports captured")
    reports = captured[0]

    for rep in reports:
        if rep.longrepr:
            try:
                inf = rep.longrepr.chain[0][1]
                raise PytestException(f"Line: {inf.lineno + 1}; {inf.message}")

            except PytestException:
                raise

            except Exception as e:
                logger.error(repr(e))
                raise LivepyError(str(e))
    raise PytestCaseRunnerSuccess()  # NOTE: signal test case passed


run_pytest_case = PytestCaseRunner()
run_pytest_case.name = "pyls_livepy.run_pytest_case"
