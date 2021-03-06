# Copyright (C) 2015-2018 Jurriaan Bremer.
# Copyright (C) 2018 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker
from sflock.exception import UnpackException


class Zip7File(Unpacker):
    name = "7zfile"
    exe = "/usr/bin/7z"
    exts = b".7z", b".iso", b".img", b".xz"
    # TODO Should we use "isoparser" (check PyPI) instead of 7z?
    magic = "7-zip archive", "ISO 9660", "UDF filesystem data", "XZ compressed data"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        # if password:
        # raise UnpackException(
        #    "Currently password-protected .7z files are not supported "
        #    "due to a ZipJail-related monitoring issue (namely, due to "
        #    "7z calling clone(2) when a password has been provided)."
        # )

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(b".7z")
            temporary = True
        if password:
            ret = self.zipjail_clone_one(filepath, dirpath, "x", "-mmt1", "-o%s", "-p%s" % dirpath, filepath, password)
        else:
            ret = self.zipjail_clone_one(filepath, dirpath, "x", "-mmt1", "-o%s" % dirpath, filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class GzipFile(Unpacker):
    name = "gzipfile"
    exe = "/usr/bin/7z"
    exts = b".gzip"
    magic = "gzip compressed data, was"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".7z")
            temporary = True

        ret = self.zipjail_clone_one(filepath, dirpath, "x", "-mmt1", "-o%s" % dirpath, filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class LzhFile(Unpacker):
    name = "lzhfile"
    exe = "/usr/bin/7z"
    exts = b".lzh", b".lha"
    magic = "LHa ("

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".7z")
            temporary = True

        ret = self.zipjail(filepath, dirpath, "x", "-o%s" % dirpath, filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)


class VHDFile(Unpacker):
    name = "vhdfile"
    exe = "/usr/bin/7z"
    exts = b".vhd"
    magic = "Microsoft Disk Image, Virtual Server or Virtual PC"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = self.f.filepath
            temporary = False
        else:
            filepath = self.f.temp_path(".vhd")
            temporary = True

        ret = self.zipjail_clone_one(filepath, dirpath, "x", "-o%s" % dirpath, filepath)
        if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)
