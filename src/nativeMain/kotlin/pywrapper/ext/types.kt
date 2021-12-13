package pywrapper.ext

import kotlinx.cinterop.*
import python.*
import pywrapper.PyObjectT

internal val CPointer<PyObject>.kt
    get(): CPointer<KtPyObject> = reinterpret()

internal inline fun <reified T : Any> CPointer<KtPyObject>.cast(): T {
    val ref = this.pointed.ktObject!!.asStableRef<T>()
    return ref.get()
}

internal inline fun PyObjectT.addType(type: PyTypeObject): Int {
    memScoped {
        var status = PyType_Ready(type.ptr)
        if (status < 0) {
            PyErr_Print()
        } else {
            status = PyModule_AddType(this@addType, type.ptr)
        }
        return status
    }
}