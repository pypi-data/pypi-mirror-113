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


import linecache

from birdseye import eye

from pyls_livepy.utils import logger


def get_traces(results):
    """Get traces from results dict."""
    traces = {}

    for name, res in results.items():
        traces[name] = res["traces"]
    return traces


def run_trace(source, path):
    """Trace the decorated callables in the given source."""
    filename = (path or "") + "<*>"

    try:
        code_obj = compile(source, filename, "exec")
        linecache.cache[filename] = (
            len(source),
            None,
            [line + '\n' for line in source.splitlines()],
            filename,
        )
        exec(code_obj, {"eye": eye})

    except Exception as e:
        logger.exception(f"{repr(e)}\n\n")
        return repr(e)
    return "Run OK"


def trace_and_report(source, doctest, path):
    # NOTE: temp until superceded by pysnooper-backed version
    #     - need to revise this
    defs = [
        # "class",
        "def",
        # "async",
    ]
    plt = "pyls_livepy.eye\n"
    ex_sources = [ex.source for ex in doctest.examples]
    modded_source = source + "\n\n" + "\n".join(ex_sources or [])

    for line in modded_source.splitlines():
        d_cnt = 0

        if line and line.split(" ")[0] in defs:
            n_line = f"@{plt}{line}"

            if d_cnt == 0:
                n_line = "import pyls_livepy\n\n" + n_line
            modded_source = modded_source.replace(line, n_line)
            d_cnt += 1
    report = run_trace(modded_source, path)
    return report


def patch_read_source_file():
    """Patch birdseye module if not yet updated.

    NOTE: This can be removed once birdseye ^0.9.2 is released
    """
    from birdseye import utils as bu

    if hasattr(bu, "linecache"):
        return

    def _patched_rsf(filename):
        import linecache
        from lib2to3.pgen2.tokenize import cookie_re

        if filename.endswith('.pyc'):
            filename = filename[:-1]

        return ''.join([
            '\n' if i < 2 and cookie_re.match(line)
            else line
            for i, line in enumerate(linecache.getlines(filename))
        ])
    setattr(bu, "read_source_file", _patched_rsf)
    return


patch_read_source_file()
