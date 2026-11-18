#!/usr/bin/env -S PYTHONPATH=../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'vendor/miuicamera-gauguin',
]


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    # getANativeWindow(): pass a null producer listener to Surface::connect(),
    # the A12 IProducerListener subclass doesn't match the current libgui vtable
    ('system/lib64/libcamera_algoup_jni.xiaomi.so', 'system/lib64/libcamera_mianode_jni.xiaomi.so'): blob_fixup()
        .sig_replace('f6 03 00 f9 56 01 00 b4 c8 02 1d ca', 'ff 03 00 f9'),
    'system/lib64/libcamera_jpegutil_jni.xiaomi.so': blob_fixup()
        .remove_needed('libhidltransport.so'),
    'system/priv-app/MiuiCamera/MiuiCamera.apk': blob_fixup()
        .apktool_patch('patches'),
}  # fmt: skip

module = ExtractUtilsModule(
    'xiaomi',
    'miuicamera-gauguin',
    device_rel_path='vendor/miuicamera-gauguin',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
