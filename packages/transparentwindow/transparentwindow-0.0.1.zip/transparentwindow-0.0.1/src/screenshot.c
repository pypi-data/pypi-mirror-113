#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <windows.h>

static PyObject *screenshot(PyObject *self, PyObject *args, PyObject *keywds)
{
    int x = 0;
    int y = 0;
    int width = 640;
    int height = 480;
    static char *kwlist[] = {"x", "y", "width", "height", NULL};
    if (!PyArg_ParseTupleAndKeywords(
            args, keywds, "|iiii", kwlist, &x, &y, &width, &height))
    {
        return NULL;
    }

    HWND hwndDesktop = GetDesktopWindow();

    /* DIB の情報を設定 */
    BITMAPINFO bmpInfo = {0};
    bmpInfo.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bmpInfo.bmiHeader.biWidth = width;
    bmpInfo.bmiHeader.biHeight = height;
    bmpInfo.bmiHeader.biPlanes = 1;
    bmpInfo.bmiHeader.biBitCount = 32;        /* ピクセルあたりのビット数 */
    bmpInfo.bmiHeader.biCompression = BI_RGB; /* 圧縮なし */

    /* デバイスコンテキストの取得・作成 */
    LPDWORD lpPixel = NULL;
    HDC hdcScreen = GetDC(hwndDesktop);
    HDC hdcBack = CreateCompatibleDC(hdcScreen);
    HBITMAP hBitmap = CreateDIBSection(hdcScreen, &bmpInfo, DIB_RGB_COLORS, (void **)&lpPixel, NULL, 0);
    SelectObject(hdcBack, hBitmap);

    /* デスクトップ画面全体より指定領域だけをキャプチャ */
    BitBlt(hdcBack, 0, 0, width, height, hdcScreen, x, y, SRCCOPY);

    /* ファイルサイズの計算 */
    DWORD dwHeadSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    DWORD dwBmpSize = ((width * bmpInfo.bmiHeader.biBitCount + 31) / 32) * 4 * height;
    DWORD dwFileSize = dwHeadSize + dwBmpSize;

#ifdef DEBUG
    /* BITMAPFILEHEADER 構造体の初期化 */
    BITMAPFILEHEADER bmfHeader;
    bmfHeader.bfType = 0x4D42;
    bmfHeader.bfSize = dwFileSize;
    bmfHeader.bfOffBits = dwHeadSize;

    /* bmp に保存 */
    HANDLE hFile = CreateFileW(L"DEBUG-capture.bmp", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    DWORD dwBytesWritten = 0;
    WriteFile(hFile, (LPSTR)&bmfHeader, sizeof(BITMAPFILEHEADER), &dwBytesWritten, NULL);
    WriteFile(hFile, (LPSTR)&bmpInfo.bmiHeader, sizeof(BITMAPINFOHEADER), &dwBytesWritten, NULL);
    WriteFile(hFile, (LPSTR)lpPixel, dwBmpSize, &dwBytesWritten, NULL);
    CloseHandle(hFile);
#endif

    /* 返り値の構成 */
    PyObject *ret = PyByteArray_FromStringAndSize((LPSTR)lpPixel, (Py_ssize_t)dwBmpSize);

    /* デバイスコンテキストの解放・削除 */
    DeleteObject(hBitmap);
    DeleteDC(hdcBack);
    ReleaseDC(hwndDesktop, hdcScreen);

    return ret;
}

static PyMethodDef Methods_THIS[] = {
    {"screenshot",
     (PyCFunction)(void (*)(void))screenshot,
     METH_VARARGS | METH_KEYWORDS,
     PyDoc_STR("screenshot(x:int, y:int, width:int, height:int) -> bytearray\n\n"
               "Return the raw data of a screen image.")},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef thismodule = {
    PyModuleDef_HEAD_INIT, "_screenshot",
    "Python Extension Module (for win_x64)",
    -1, Methods_THIS};

PyMODINIT_FUNC PyInit__screenshot(void)
{
    return PyModule_Create(&thismodule);
}
