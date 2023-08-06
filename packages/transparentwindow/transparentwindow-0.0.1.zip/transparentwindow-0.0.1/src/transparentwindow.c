#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <windows.h>
#include "resource.h"

static HINSTANCE hinstDLL;
static const wchar_t CLASS_NAME[] = L"Transparent_Window@Python";

BOOL WINAPI DllMain(HINSTANCE hinst, DWORD fdwReason, LPVOID lpReserved)
{
    if (fdwReason == DLL_PROCESS_ATTACH)
    {
        hinstDLL = hinst;
    }
    return TRUE;
}

static INT_PTR CALLBACK DialogProc(HWND hwndDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    static HWND hwnd;
    static int diff_x, diff_y, diff_w, diff_h;
    POINT cli_point = {0};
    RECT cli_rect = {0};
    RECT wnd_rect = {0};
    int result = 0;
    switch (uMsg)
    {
    case WM_INITDIALOG:
        hwnd = GetParent(hwndDlg);
        ClientToScreen(hwnd, &cli_point);
        SetDlgItemInt(hwndDlg, IDC_EDIT_X, cli_point.x, TRUE);
        SetDlgItemInt(hwndDlg, IDC_EDIT_Y, cli_point.y, TRUE);
        GetClientRect(hwnd, &cli_rect);
        SetDlgItemInt(hwndDlg, IDC_EDIT_W, cli_rect.right, TRUE);
        SetDlgItemInt(hwndDlg, IDC_EDIT_H, cli_rect.bottom, TRUE);
        GetWindowRect(hwnd, &wnd_rect);
        diff_x = wnd_rect.left - cli_point.x;
        diff_y = wnd_rect.top - cli_point.y;
        diff_w = (wnd_rect.right - wnd_rect.left) - (cli_rect.right);
        diff_h = (wnd_rect.bottom - wnd_rect.top) - (cli_rect.bottom);
        break;
    case WM_CLOSE:
        EndDialog(hwndDlg, IDOK);
        return 1;
    case WM_COMMAND:
        switch (LOWORD(wParam))
        {
        case IDOK:
            cli_point.x = GetDlgItemInt(hwndDlg, IDC_EDIT_X, &result, TRUE);
            if (result == FALSE)
                break;
            cli_point.y = GetDlgItemInt(hwndDlg, IDC_EDIT_Y, &result, TRUE);
            if (result == FALSE)
                break;
            cli_rect.left = GetDlgItemInt(hwndDlg, IDC_EDIT_W, &result, TRUE);
            if (result == FALSE)
                break;
            cli_rect.bottom = GetDlgItemInt(hwndDlg, IDC_EDIT_H, &result, TRUE);
            if (result == FALSE)
                break;
            SetWindowPos(
                hwnd, HWND_TOPMOST, cli_point.x + diff_x, cli_point.y + diff_y, cli_rect.left + diff_w, cli_rect.bottom + diff_h, 0);
            SetFocus(hwndDlg);
            PostMessageW(hwndDlg, WM_COMMAND, ID_UPDATE_PROP, 0);
            break;
        case ID_UPDATE_PROP:
            ClientToScreen(hwnd, &cli_point);
            SetDlgItemInt(hwndDlg, IDC_EDIT_X, cli_point.x, TRUE);
            SetDlgItemInt(hwndDlg, IDC_EDIT_Y, cli_point.y, TRUE);
            GetClientRect(hwnd, &cli_rect);
            SetDlgItemInt(hwndDlg, IDC_EDIT_W, cli_rect.right, TRUE);
            SetDlgItemInt(hwndDlg, IDC_EDIT_H, cli_rect.bottom, TRUE);
            break;
        }
    }
    return 0;
}

static LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    static HMENU cMenu_tmp, cMenu;
    static MINMAXINFO *mInfo;
    static PyObject *callback;
    POINT point = {0};
    switch (uMsg)
    {
    case WM_CREATE:
        callback = (PyObject *)((CREATESTRUCTW *)lParam)->lpCreateParams;
        cMenu_tmp = LoadMenuW(hinstDLL, MAKEINTRESOURCEW(IDC_CONTEXTMENU));
        cMenu = GetSubMenu(cMenu_tmp, 0);
        break;
    case WM_GETMINMAXINFO:
        mInfo = (MINMAXINFO *)lParam;
        mInfo->ptMinTrackSize.x = 66;
        mInfo->ptMinTrackSize.y = 56; /* タイトルバーの高さと同じ */
        break;
    case WM_RBUTTONDOWN:
        point.x = LOWORD(lParam);
        point.y = HIWORD(lParam);
        ClientToScreen(hwnd, &point);
        TrackPopupMenu(cMenu, TPM_LEFTALIGN, point.x, point.y, 0, hwnd, NULL);
        break;
    case WM_COMMAND:
        switch (LOWORD(wParam))
        {
        case IDM_PROPERTY:
            DialogBoxW(hinstDLL, MAKEINTRESOURCEW(IDD_DIALOG1), hwnd, DialogProc);
            break;
        case IDM_CLOSE:
            DestroyWindow(hwnd);
            break;
        }
        break;
    case WM_KEYDOWN:
        if (PyCallable_Check(callback))
        {
            PyObject *ret = PyObject_CallFunction(callback, "i", wParam);
            if (ret != NULL)
                Py_DECREF(ret);
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

static int __show(HWND hWndParent, int width, int height, wchar_t title[], PyObject *callback)
{
    HWND hwnd = CreateWindowExW(
        WS_EX_NOREDIRECTIONBITMAP | WS_EX_PALETTEWINDOW | WS_EX_APPWINDOW, // Optional window styles.
        CLASS_NAME,                                                        // Window class
        title,                                                             // Window text
        WS_CAPTION | WS_SIZEBOX | WS_SYSMENU,                              // Window style
        /* x, y, width, height */
        CW_USEDEFAULT, CW_USEDEFAULT, width, height,
        hWndParent,      // Parent window
        NULL,            // Menu
        hinstDLL,        // Instance handle
        (LPVOID)callback // Additional application data
    );

    HACCEL hAccelTable = LoadAccelerators(hinstDLL, MAKEINTRESOURCEW(IDC_ACCELERATORS));

    UpdateWindow(hwnd);
    ShowWindow(hwnd, SW_SHOW);

    MSG msg = {0};
    while (GetMessageW(&msg, NULL, 0, 0))
    {
        if (!TranslateAcceleratorW(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessageW(&msg);
        }
    }

    return 0;
}

static PyObject *show(PyObject *self, PyObject *args, PyObject *keywds)
{
    HWND hWndParent = NULL;
    int width = 640;
    int height = 480;
    PyObject *pre_title = NULL;
    PyObject *callback = NULL;
    static char *kwlist[] = {"hwnd", "width", "height", "title", "callback", NULL};

    /* borrowed references; do not decrement their reference count! */
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "|KiiUO", kwlist, &hWndParent, &width, &height, &pre_title, &callback))
        return NULL;

    wchar_t *title = NULL;
    if (pre_title != NULL)
    {
        title = PyUnicode_AsWideCharString(pre_title, NULL);
    }

    __show(hWndParent, width, height, title, callback);

    if (title != NULL)
    {
        PyMem_Free(title);
        title = NULL;
    }

    return Py_None;
}

static PyMethodDef Methods_THIS[] = {
    {"show",
     (PyCFunction)(void (*)(void))show,
     METH_VARARGS | METH_KEYWORDS,
     "show(hwnd: int = 0, width:int = 640, height:int = 480, title: str = None, callback: Callable = None)"},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef thismodule = {
    PyModuleDef_HEAD_INIT,
    "_transparentwindow",
    "Python Extension Module (for windows)",
    -1,
    Methods_THIS};

PyMODINIT_FUNC PyInit__transparentwindow(void)
{
    /* ウィンドウクラスの登録 */
    WNDCLASSW wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hinstDLL;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursorW(NULL, IDC_CROSS); /* User32.dll の関数 */
    RegisterClassW(&wc);                       /* User32.dll の関数 */
    /* User32.dll の関数を DLLMain で呼び出してはならない. */
    /* https://docs.microsoft.com/ja-jp/windows/win32/dlls/dynamic-link-library-best-practices */

    return PyModule_Create(&thismodule);
}
