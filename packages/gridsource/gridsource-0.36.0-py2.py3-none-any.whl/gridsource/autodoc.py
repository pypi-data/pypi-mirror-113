"""Autodoc to create automatic documentation
"""
import logging
import shlex
import shutil
import subprocess as sp
from pathlib import Path

import numpy as np
import pandas as pd
import tabulate

from gridsource import Data as IVData
from gridsource.validation import load_yaml

INDENT = "    "
HEADERS = ["=", "-", '"', "'", "~"]


# =============================================================================
# a few RST helpers
# =============================================================================
def _write(txt="", indent=0, header=None):
    if header:
        txt = "\n%s" % txt
        txt += "\n" + len(txt) * HEADERS[header - 1] + "\n"
    return INDENT * indent + txt + "\n"


def _indent(txt, indent):
    """
    :param txt:
    :param indent:
    :return:
    """
    if indent == 0:
        return txt
    else:
        indent = INDENT * indent
        if isinstance(txt, list):
            return ["".join([indent, line]) for line in txt]
        else:
            return "".join([indent, txt])


def _comment(txt):
    return _directive(content=txt)


def _include(filename, relative_to=False):
    if relative_to:
        filename = filename.relative_to(relative_to)
    return f"\n.. include:: {filename}\n\n"


def _directive(name="", arg=None, fields=None, content=None, indent=0):
    """
    :param name: the directive itself to use
    :param arg: the argument to pass into the directive
    :param fields: fields to append as children underneath the directive
    :param content: the text to write into this element
    :param indent: (optional default=0) number of characters to indent this element
    :return:

    Add a comment with a not-named directive:

    >>> print(_directive(content='bla'))
    ..
    <BLANKLINE>
        bla
    """
    o = list()
    if name:
        o.append(".. {0}::".format(name))
    else:
        o.append("..")

    if arg is not None:
        o[0] += " " + arg

    if fields is not None:
        for k, v in fields:
            o.append(_indent(":" + k + ": " + str(v), indent=1))

    if content is not None:
        o.append("")

        if isinstance(content, list):
            o.extend(_indent(content, 1))
        else:
            o.append(_indent(content, 1))
    return "\n".join(o)


class VDataAutodoc:
    """Document a set of columns (aka `tab`)"""

    def __init__(self, ivdata_obj, target_dir=None):
        self.schemas = ivdata_obj._schemas
        if not target_dir:
            target_dir = Path.home()
        if isinstance(target_dir, str):
            target_dir = Path(target_dir)
        self.target_dir = target_dir
        logging.info(f"output in {target_dir}")
        if not self.exists():
            if self.target_dir.exists():
                raise FileExistsError(
                    "target {target_dir} exists and is not a proper Sphynx folder"
                )
            else:
                logging.warning("Sphynx project does not exist. Please run `.create`")
        else:
            self.src_dir = self.target_dir / "source"

    def create(self, project_name, author, version, lang="en", exist_ok=False):
        if self.target_dir.exists():
            if not exist_ok:
                raise FileExistsError(f"target {self.target_dir} exists")
            else:
                shutil.rmtree(self.target_dir)
        # -----------------------------------------------------------------
        # create project structure
        cmd = f"sphinx-quickstart --sep -p {project_name} -a {author} -v {version} -l {lang} {self.target_dir} -q"
        args = shlex.split(cmd)
        ret = sp.run(args)
        index_content = (
            f"Welcome to {project_name}'s documentation!\n"
            "===========================================\n"
            "\n"
            ".. toctree::\n"
            "   :maxdepth: 2\n"
            "   :caption: Contents:\n"
            "\n"
            "   input_data.rst\n"
        )
        self.src_dir = self.target_dir / "source"
        with open(self.src_dir / "index.rst", "w") as fh:
            fh.write(index_content)

    def exists(self):
        if not self.target_dir.exists():
            return False
        # we detect if sphynx project based on:
        conf = self.target_dir / "source" / "conf.py"
        makefile = self.target_dir / "Makefile"
        return conf.exists() and makefile.exists()

    def dump_data(
        self,
        skip_tabs=(),
        drop_columns=(),
        rename_columns=(),
        order_columns=("column",),
    ):
        # =====================================================================
        # index.rst call master file `input_data.rst`
        # =====================================================================
        # Private master file `.input_data.rst` is created from scratch
        _master_file = self.src_dir / ".input_data.rst"
        with open(_master_file, "w") as fh:
            fh.write(_write("Expected Input Data", header=2))
            fh.write(_write("The following sections describe the expected data."))
        # ---------------------------------------------------------------------
        # Public master file is called "input_data.rst" and is created only
        # if it doesn't exist
        master_file = self.src_dir / "input_data.rst"
        if not master_file.exists():
            with open(master_file, "w") as fh:
                fh.write(_write("User Input", header=1))
                fh.write(_write("Introduction", header=2))
                fh.write(_write("Write your static introduction here..."))
                fh.write(_include(_master_file, relative_to=self.src_dir))
        # =====================================================================
        # processing tabs
        # =====================================================================
        tabdir = self.src_dir / "tabs"
        tabdir.mkdir(exist_ok=True)
        for tab, schema in self.schemas.items():
            # if tab == "dimensionalities":
            #     self._write_dimensionalities(schema)
            #     continue
            if tab in skip_tabs:
                continue
            # -----------------------------------------------------------------
            # update private master file
            with open(_master_file, "a") as fh:
                fh.write(_include(tabdir / f".{tab}.rst", relative_to=self.src_dir))
            # -----------------------------------------------------------------
            # create public tab description file `source/tabs/<tab>.rst`
            filename = tabdir / f"{tab}.rst"
            if not filename.exists():
                with open(filename, "w") as fh:
                    fh.write(
                        _write(
                            f"Please edit ``{filename}`` to provide adequate description"
                        )
                    )
            # -----------------------------------------------------------------
            # create private tab description file `source/tabs/.<tab>.rst`
            _filename = tabdir / f".{tab}.rst"
            with open(_filename, "w") as fh:
                fh.write(_write(f"Tab ``{tab}``", header=2))
                fh.write(_write(f"Specifications", header=3))
                # include public tab description file `source/tabs/<tab>.rst`
                fh.write(_include(filename, relative_to=self.src_dir))
                fh.write(_write("Data Types", header=3))
                # =================================================================
                # columns description
                # =================================================================
                columns = {k: v["items"] for k, v in schema.columns_specs.items()}
                df = pd.DataFrame.from_dict(columns, orient="index")
                # -----------------------------------------------------------------
                # make anyOf more readable
                if "anyOf" in df:
                    anyOf = df.anyOf.explode().dropna().apply(lambda row: row["type"])

                    anyOf = anyOf.replace("null", np.NaN).dropna()
                    anyOf = anyOf.groupby(level=0).apply(lambda x: "/".join(x))
                    df.loc[anyOf.index, "type"] = anyOf
                    df.drop(columns="anyOf", inplace=True)
                    df = df.fillna("")
                df.index.names = ["column"]
                # -------------------------------------------------------------
                # process special columns
                mandatory = dict(zip(schema.required, [True] * len(schema.required)))
                _uniq = dict(schema.uniqueness_sets)
                if _uniq:
                    uniq = {}
                    for id, cols in _uniq.items():
                        for col in cols:
                            uniq[col] = id
                    df["set"] = pd.Series(uniq)
                    df["set"] = df.set.fillna("")
                if mandatory:
                    df["mandatory"] = pd.Series(mandatory)
                    df["mandatory"] = df.mandatory.fillna("")
                if "type" in df.columns:
                    df["type"] = df["type"].replace(
                        {
                            "number": "``float``",
                            "integer": "``int``",
                            "string": "``str``",
                        }
                    )
                # -------------------------------------------------------------
                # bold index
                df.reset_index(inplace=True)
                df["column"] = "**" + df["column"].astype(str) + "**"
                # -------------------------------------------------------------
                # order columns
                cols = list(order_columns)
                cols += [c for c in df if c not in cols]  # append remaining columns
                cols = [c for c in cols if c in df]  # ensure all columns are exiting
                df = df[cols]
                # -------------------------------------------------------------
                # drop columns
                _drop_columns = [c for c in drop_columns if c in df]
                if _drop_columns:
                    df = df.drop(columns=_drop_columns)
                # -------------------------------------------------------------
                # rename columns
                _rename_columns = {
                    prev: new for prev, new in rename_columns.items() if prev in df
                }
                if _rename_columns:
                    df = df.rename(columns=_rename_columns)
                # -------------------------------------------------------------
                # clean and order
                df = df.fillna("")
                table = tabulate.tabulate(
                    df, headers="keys", tablefmt="rst", showindex=False
                )
                fh.write(_write(table))
                if _uniq:
                    fh.write(
                        _write(
                            "the following sets of columns combination need to be **unique**:"
                        )
                    )
                for uniq, cols in _uniq.items():
                    columns = ", ".join([f"``{c}``" for c in cols])
                    fh.write(_write(f"  * ``{uniq}``: {columns}"))


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
