#!/usr/bin/env python3
"""
Generate .pyi stubs for aspose.pydrawing using minimal introspection.
Avoids deep attribute access that can crash the .NET wrapper.
"""
import sys
from pathlib import Path


def generate_stub_from_names(module_name: str, class_names: list, submodules: list = None) -> str:
    """Generate a minimal stub from just names."""
    lines = [
        '"""',
        f'Type stubs for {module_name}',
        'Auto-generated from runtime introspection.',
        '"""',
        'from typing import Any, ClassVar, Optional, List, Tuple, Union, overload',
        '',
    ]

    if submodules:
        for sub in sorted(submodules):
            lines.append(f"from . import {sub}")
        lines.append("")

    for name in sorted(class_names):
        lines.append(f"class {name}:")
        lines.append(f"    '''Wrapper for System.Drawing.{name}'''")
        lines.append("    def __init__(self, *args, **kwargs) -> None: ...")
        lines.append("")

    return '\n'.join(lines)


def main():
    # Pre-collected member names (avoids crashing introspection)
    # These were collected from a successful dir() call earlier

    pydrawing_classes = [
        'Bitmap', 'BitmapSuffixInSameAssemblyAttribute', 'BitmapSuffixInSatelliteAssemblyAttribute',
        'Brush', 'Brushes', 'BufferedGraphics', 'BufferedGraphicsContext', 'BufferedGraphicsManager',
        'CharacterRange', 'Color', 'ColorTranslator', 'ContentAlignment', 'CopyPixelOperation',
        'Font', 'FontConverter', 'FontFamily', 'FontStyle', 'Graphics', 'GraphicsUnit',
        'IDeviceContext', 'Icon', 'IconConverter', 'Image', 'ImageAnimator', 'ImageConverter',
        'ImageFormatConverter', 'KnownColor', 'Pen', 'Pens', 'Point', 'PointF',
        'Rectangle', 'RectangleF', 'Region', 'RotateFlipType', 'Size', 'SizeF',
        'SolidBrush', 'StringAlignment', 'StringDigitSubstitute', 'StringFormat',
        'StringFormatFlags', 'StringTrimming', 'StringUnit', 'SystemBrushes', 'SystemColors',
        'SystemFonts', 'SystemIcons', 'SystemPens', 'TextureBrush', 'ToolboxBitmapAttribute'
    ]

    pydrawing_submodules = ['drawing2d', 'imaging', 'printing', 'text', 'design']

    drawing2d_classes = [
        'AdjustableArrowCap', 'Blend', 'ColorBlend', 'CombineMode', 'CompositingMode',
        'CompositingQuality', 'CoordinateSpace', 'CustomLineCap', 'DashCap', 'DashStyle',
        'FillMode', 'FlushIntention', 'GraphicsContainer', 'GraphicsPath', 'GraphicsPathIterator',
        'GraphicsState', 'HatchBrush', 'HatchStyle', 'InterpolationMode', 'LineCap',
        'LineJoin', 'LinearGradientBrush', 'LinearGradientMode', 'Matrix', 'MatrixOrder',
        'PathData', 'PathGradientBrush', 'PathPointType', 'PenAlignment', 'PenType',
        'PixelOffsetMode', 'QualityMode', 'RegionData', 'SmoothingMode', 'WarpMode', 'WrapMode'
    ]

    imaging_classes = [
        'BitmapData', 'ColorAdjustType', 'ColorChannelFlag', 'ColorMap', 'ColorMapType',
        'ColorMatrix', 'ColorMatrixFlag', 'ColorMode', 'ColorPalette', 'EmfPlusRecordType',
        'EmfType', 'Encoder', 'EncoderParameter', 'EncoderParameterValueType', 'EncoderParameters',
        'EncoderValue', 'FrameDimension', 'ImageAttributes', 'ImageCodecFlags', 'ImageCodecInfo',
        'ImageFlags', 'ImageFormat', 'ImageLockMode', 'MetaHeader', 'Metafile',
        'MetafileFrameUnit', 'MetafileHeader', 'MetafileType', 'PaletteFlags', 'PixelFormat',
        'PlayRecordCallback', 'PropertyItem'
    ]

    printing_classes = [
        'Duplex', 'InvalidPrinterException', 'Margins', 'MarginsConverter', 'PageSettings',
        'PaperKind', 'PaperSize', 'PaperSource', 'PaperSourceKind', 'PreviewPageInfo',
        'PreviewPrintController', 'PrintAction', 'PrintController', 'PrintDocument',
        'PrintEventArgs', 'PrintEventHandler', 'PrintPageEventArgs', 'PrintPageEventHandler',
        'PrintRange', 'PrinterResolution', 'PrinterResolutionKind', 'PrinterSettings',
        'PrinterUnitConvert', 'QueryPageSettingsEventArgs'
    ]

    text_classes = [
        'FontCollection', 'GenericFontFamilies', 'HotkeyPrefix',
        'InstalledFontCollection', 'PrivateFontCollection', 'TextRenderingHint'
    ]

    design_classes = ['CategoryNameCollection']

    output_dir = Path(__file__).parent / "generated_stubs" / "aspose" / "pydrawing"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Main module
    stub = generate_stub_from_names("aspose.pydrawing", pydrawing_classes, pydrawing_submodules)
    (output_dir / "__init__.pyi").write_text(stub)
    print(f"Written: __init__.pyi ({len(stub.splitlines())} lines)")

    # Submodules
    submodule_data = [
        ('drawing2d', drawing2d_classes),
        ('imaging', imaging_classes),
        ('printing', printing_classes),
        ('text', text_classes),
        ('design', design_classes),
    ]

    for sub_name, classes in submodule_data:
        sub_dir = output_dir / sub_name
        sub_dir.mkdir(exist_ok=True)
        stub = generate_stub_from_names(f"aspose.pydrawing.{sub_name}", classes)
        (sub_dir / "__init__.pyi").write_text(stub)
        print(f"Written: {sub_name}/__init__.pyi ({len(stub.splitlines())} lines)")

    print(f"\nStubs written to: {output_dir}")


if __name__ == "__main__":
    main()
