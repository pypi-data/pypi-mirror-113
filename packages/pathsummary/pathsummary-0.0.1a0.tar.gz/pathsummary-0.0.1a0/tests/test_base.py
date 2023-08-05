from pathlib import Path
from pathsummary import _guess_mimetype, _make_raw_summary_table_from_path, \
    _split_mimetype_of_summary_table, summarize_folder_files


def test_image_mimetypes():
    expected_pairs = [
        ("image00.bmp", "image/bmp"),
        ("image00.jpeg", "image/jpeg"),
        ("image00.jpg", "image/jpeg"),
        ("image00.png", "image/png"),
        ("image00.tif", "image/tiff"),
        ("image00.tiff", "image/tiff"),
        ("image01.BMP", "image/bmp"),
        ("image01.JPEG", "image/jpeg"),
        ("image01.JPG", "image/jpeg"),
        ("image01.PNG", "image/png"),
        ("image01.TIF", "image/tiff"),
        ("image01.TIFF", "image/tiff"),
    ]
    for test_name, expected_mimetype in expected_pairs:
        guessed_mimetype, encoding = _guess_mimetype(Path(test_name))
        assert guessed_mimetype == expected_mimetype


def test_raw_summary_table_of_images():
    """

    >>> from doctestprinter import print_pandas
    >>> image_table = test_raw_summary_table_of_images()
    >>> print_pandas(image_table)
                 file_rootpath      filename    mimetype  encoding
     0  tests/resources/images   image00.bmp   image/bmp      None
     1  tests/resources/images  image00.jpeg  image/jpeg      None
     2  tests/resources/images   image00.jpg  image/jpeg      None
     3  tests/resources/images   image00.png   image/png      None
     4  tests/resources/images   image00.tif  image/tiff      None
     5  tests/resources/images  image00.tiff  image/tiff      None
     6  tests/resources/images   image01.BMP   image/bmp      None
     7  tests/resources/images  image01.JPEG  image/jpeg      None
     8  tests/resources/images   image01.JPG  image/jpeg      None
     9  tests/resources/images   image01.PNG   image/png      None
    10  tests/resources/images   image01.TIF  image/tiff      None
    11  tests/resources/images  image01.TIFF  image/tiff      None

    """
    return _make_raw_summary_table_from_path(Path("tests/resources/images"))



def test_summary_table_of_images():
    """

    >>> from doctestprinter import print_pandas
    >>> image_table = test_summary_table_of_images()
    >>> print_pandas(image_table)
                 file_rootpath      filename  encoding  filetype  subtype
     0  tests/resources/images   image00.bmp      None     image      bmp
     1  tests/resources/images  image00.jpeg      None     image     jpeg
     2  tests/resources/images   image00.jpg      None     image     jpeg
     3  tests/resources/images   image00.png      None     image      png
     4  tests/resources/images   image00.tif      None     image     tiff
     5  tests/resources/images  image00.tiff      None     image     tiff
     6  tests/resources/images   image01.BMP      None     image      bmp
     7  tests/resources/images  image01.JPEG      None     image     jpeg
     8  tests/resources/images   image01.JPG      None     image     jpeg
     9  tests/resources/images   image01.PNG      None     image      png
    10  tests/resources/images   image01.TIF      None     image     tiff
    11  tests/resources/images  image01.TIFF      None     image     tiff

    """
    raw_table = _make_raw_summary_table_from_path(Path("tests/resources/images"))
    return _split_mimetype_of_summary_table(raw_table)


def test_summarize_folder_files():
    empty_dict = summarize_folder_files("/non/existing/path")
    assert len(empty_dict) == 0, "An empty dict was expected."

    empty_dict = summarize_folder_files("pathsummary.py")
    assert len(empty_dict) == 0, "An empty dict was expected."