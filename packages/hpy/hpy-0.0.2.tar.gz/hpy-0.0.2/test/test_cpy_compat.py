from .support import HPyTest


class TestCPythonCompatibility(HPyTest):

    # One note about the supports_refcounts() in the tests below: on
    # CPython, handles are actually implemented as INCREF/DECREF, so we can
    # check e.g. after an HPy_Dup the refcnt is += 1. However, on PyPy they
    # are implemented in a completely different way which is unrelated to the
    # refcnt (this is the whole point of HPy, after all :)). So in many of the
    # following ttests, checking the actual result of the function doesn't
    # really make sens on PyPy. We still run the functions to ensure they do
    # not crash, though.

    def test_frompyobject(self):
        mod = self.make_module("""
            #include <Python.h>
            HPyDef_METH(f, "f", f_impl, HPyFunc_NOARGS)
            static HPy f_impl(HPyContext ctx, HPy self)
            {
                PyObject *o = PyList_New(0);
                Py_ssize_t initial_refcount = o->ob_refcnt;
                HPy h = HPy_FromPyObject(ctx, o);
                Py_ssize_t final_refcount = o->ob_refcnt;

                PyList_Append(o, PyLong_FromLong(1234));
                PyList_Append(o, PyLong_FromSsize_t(final_refcount -
                                                    initial_refcount));
                Py_DECREF(o);
                return h;
            }
            @EXPORT(f)
            @INIT
        """)
        x = mod.f()
        assert x[0] == 1234
        assert len(x) == 2
        if self.supports_refcounts():
            assert x == [1234, +1]

    def test_aspyobject(self):
        mod = self.make_module("""
            #include <Python.h>
            HPyDef_METH(f, "f", f_impl, HPyFunc_O)
            static HPy f_impl(HPyContext ctx, HPy self, HPy arg)
            {
                PyObject *o = HPy_AsPyObject(ctx, arg);
                long val = PyLong_AsLong(o);
                Py_DecRef(o);
                return HPyLong_FromLong(ctx, val*2);
            }
            @EXPORT(f)
            @INIT
        """)
        assert mod.f(21) == 42

    def test_aspyobject_custom_class(self):
        mod = self.make_module("""
            #include <Python.h>
            HPyDef_METH(f, "f", f_impl, HPyFunc_O)
            static HPy f_impl(HPyContext ctx, HPy self, HPy arg)
            {
                PyObject *o = HPy_AsPyObject(ctx, arg);
                PyObject *o_res = PyObject_CallMethod(o, "foo", "");
                HPy h_res = HPy_FromPyObject(ctx, o_res);
                Py_DecRef(o);
                Py_DecRef(o_res);
                return h_res;
            }
            @EXPORT(f)
            @INIT
        """)
        class MyClass:
            def foo(self):
                return 1234
        obj = MyClass()
        assert mod.f(obj) == 1234

    def test_hpy_close(self):
        mod = self.make_module("""
            #include <Python.h>
            HPyDef_METH(f, "f", f_impl, HPyFunc_NOARGS)
            static HPy f_impl(HPyContext ctx, HPy self)
            {
                PyObject *o = PyList_New(0);

                HPy h = HPy_FromPyObject(ctx, o);
                Py_ssize_t initial_refcount = o->ob_refcnt;
                HPy_Close(ctx, h);
                Py_ssize_t final_refcount = o->ob_refcnt;

                Py_DECREF(o);
                return HPyLong_FromLong(ctx, (long)(final_refcount -
                                                    initial_refcount));
            }
            @EXPORT(f)
            @INIT
        """)
        x = mod.f()
        if self.supports_refcounts():
            assert x == -1

    def test_hpy_dup(self):
        mod = self.make_module("""
            #include <Python.h>
            HPyDef_METH(f, "f", f_impl, HPyFunc_NOARGS)
            static HPy f_impl(HPyContext ctx, HPy self)
            {
                PyObject *o = PyList_New(0);

                HPy h = HPy_FromPyObject(ctx, o);
                Py_ssize_t initial_refcount = o->ob_refcnt;
                HPy h2 = HPy_Dup(ctx, h);
                Py_ssize_t final_refcount = o->ob_refcnt;

                HPy_Close(ctx, h);
                HPy_Close(ctx, h2);
                Py_DECREF(o);
                return HPyLong_FromLong(ctx, (long)(final_refcount -
                                                    initial_refcount));
            }
            @EXPORT(f)
            @INIT
        """)
        x = mod.f()
        if self.supports_refcounts():
            assert x == +1

    def test_many_handles(self):
        mod = self.make_module("""
            #include <Python.h>
            #define NUM_HANDLES  10000

            HPyDef_METH(f, "f", f_impl, HPyFunc_NOARGS)
            static HPy f_impl(HPyContext ctx, HPy self)
            {
                PyObject *o = PyList_New(0);

                Py_ssize_t result = -42;
                HPy handles[NUM_HANDLES];
                int i;
                Py_ssize_t initial_refcount = o->ob_refcnt;
                for (i = 0; i < NUM_HANDLES; i++)
                    handles[i] = HPy_FromPyObject(ctx, o);
                for (i = 0; i < NUM_HANDLES; i++)
                    if (HPy_IsNull(handles[i]))
                        goto error;
                for (i = 0; i < NUM_HANDLES; i++)
                    HPy_Close(ctx, handles[i]);
                Py_ssize_t final_refcount = o->ob_refcnt;
                result = final_refcount - initial_refcount;

             error:
                return HPyLong_FromLong(ctx, (long)result);
            }
            @EXPORT(f)
            @INIT
        """)
        assert mod.f() == 0

    def test_legacy_methods(self):
        mod = self.make_module("""
            #include <Python.h>

            static PyObject *f(PyObject *self, PyObject *args)
            {
                return PyLong_FromLong(1234);
            }
            static PyObject *g(PyObject *self, PyObject *arg)
            {
                long x = PyLong_AsLong(arg);
                return PyLong_FromLong(x * 2);
            }
            static PyObject *h(PyObject *self, PyObject *args)
            {
                long a, b, c;
                if (!PyArg_ParseTuple(args, "lll", &a, &b, &c))
                    return NULL;
                return PyLong_FromLong(100*a + 10*b + c);
            }
            static PyObject *k(PyObject *self, PyObject *args, PyObject *kwargs)
            {
                static char *kwlist[] = { "a", "b", "c", NULL };
                long a, b, c;
                if (!PyArg_ParseTupleAndKeywords(args, kwargs, "lll", kwlist, &a, &b, &c))
                    return NULL;
                return PyLong_FromLong(100*a + 10*b + c);
            }

            static PyMethodDef my_legacy_methods[] = {
                {"f", (PyCFunction)f, METH_NOARGS},
                {"g", (PyCFunction)g, METH_O},
                {"h", (PyCFunction)h, METH_VARARGS},
                {"k", (PyCFunction)k, METH_VARARGS | METH_KEYWORDS},
                {NULL}
            };

            @EXPORT_LEGACY(my_legacy_methods)
            @INIT
        """)
        assert mod.f() == 1234
        assert mod.g(45) == 90
        assert mod.h(4, 5, 6) == 456
        assert mod.k(c=6, b=5, a=4) == 456

    def test_legacy_slots(self):
        mod = self.make_module("""
            #include <Python.h>

            static PyObject *Dummy_repr(PyObject *self)
            {
                return PyUnicode_FromString("myrepr");
            }

            static PyObject *Dummy_add(PyObject *self, PyObject *other)
            {
                return Py_BuildValue("OO", self, other);
            }

            HPyDef_SLOT(Dummy_abs, Dummy_abs_impl, HPy_nb_absolute);
            static HPy Dummy_abs_impl(HPyContext ctx, HPy self)
            {
                return HPyLong_FromLong(ctx, 1234);
            }

            static HPyDef *Dummy_defines[] = {
                &Dummy_abs,
                NULL
            };
            static PyType_Slot Dummy_type_slots[] = {
                {Py_tp_repr, Dummy_repr},
                {Py_nb_add, Dummy_add},
                {0, 0},
            };
            static HPyType_Spec Dummy_spec = {
                .name = "mytest.Dummy",
                .legacy_slots = Dummy_type_slots,
                .defines = Dummy_defines
            };

            @EXPORT_TYPE("Dummy", Dummy_spec)
            @INIT
        """)
        d = mod.Dummy()
        assert repr(d) == 'myrepr'
        assert d + 42 == (d, 42)
        assert abs(d) == 1234

    def test_legacy_slots_methods(self):
        mod = self.make_module("""
            #include <Python.h>

            static PyObject *Dummy_foo(PyObject *self, PyObject *arg)
            {
                Py_INCREF(arg);
                return arg;
            }

            HPyDef_METH(Dummy_bar, "bar", Dummy_bar_impl, HPyFunc_NOARGS)
            static HPy Dummy_bar_impl(HPyContext ctx, HPy self)
            {
                return HPyLong_FromLong(ctx, 1234);
            }

            static PyMethodDef dummy_methods[] = {
               {"foo", Dummy_foo, METH_O},
               {NULL, NULL}         /* Sentinel */
            };

            static PyType_Slot dummy_type_slots[] = {
                {Py_tp_methods, dummy_methods},
                {0, 0},
            };

            static HPyDef *dummy_type_defines[] = {
                    &Dummy_bar,
                    NULL
            };

            static HPyType_Spec dummy_type_spec = {
                .name = "mytest.Dummy",
                .legacy_slots = dummy_type_slots,
                .defines = dummy_type_defines
            };

            @EXPORT_TYPE("Dummy", dummy_type_spec)
            @INIT
        """)
        d = mod.Dummy()
        assert d.foo(21) == 21
        assert d.bar() == 1234

    def test_legacy_slots_members(self):
        import pytest
        mod = self.make_module("""
            #include <Python.h>
            #include "structmember.h"

            typedef struct {
                HPyObject_HEAD
                long x;
                long y;
            } PointObject;

            HPyDef_SLOT(Point_new, Point_new_impl, HPy_tp_new)
            static HPy Point_new_impl(HPyContext ctx, HPy cls, HPy *args,
                                      HPy_ssize_t nargs, HPy kw)
            {
                PointObject *point;
                HPy h_point = HPy_New(ctx, cls, &point);
                if (HPy_IsNull(h_point))
                    return HPy_NULL;
                point->x = 7;
                point->y = 3;
                return h_point;
            }

            HPyDef_MEMBER(Point_x, "x", HPyMember_LONG, offsetof(PointObject, x))

            // legacy members
            static PyMemberDef legacy_members[] = {
                {"y", T_LONG, offsetof(PointObject, y), 0},
                {"y_ro", T_LONG, offsetof(PointObject, y), READONLY},
                {NULL}
            };

            static PyType_Slot legacy_slots[] = {
                {Py_tp_members, legacy_members},
                {0, NULL}
            };

            static HPyDef *Point_defines[] = {
                &Point_new,
                &Point_x,
                NULL
            };
            static HPyType_Spec Point_spec = {
                .name = "mytest.Point",
                .basicsize = sizeof(PointObject),
                .defines = Point_defines,
                .legacy_slots = legacy_slots
            };

            @EXPORT_TYPE("Point", Point_spec)
            @INIT
        """)
        p = mod.Point()
        assert p.x == 7
        assert p.y == 3
        assert p.y_ro == 3
        p.x = 123
        p.y = 456
        with pytest.raises(AttributeError):
            p.y_ro = 789
        assert p.x == 123
        assert p.y == 456

    def test_legacy_slots_getsets(self):
        mod = self.make_module("""
            #include <Python.h>

            typedef struct {
                HPyObject_HEAD
                long x;
                long y;
            } PointObject;

            HPyDef_SLOT(Point_new, Point_new_impl, HPy_tp_new)
            static HPy Point_new_impl(HPyContext ctx, HPy cls, HPy *args,
                                      HPy_ssize_t nargs, HPy kw)
            {
                PointObject *point;
                HPy h_point = HPy_New(ctx, cls, &point);
                if (HPy_IsNull(h_point))
                    return HPy_NULL;
                point->x = 7;
                point->y = 3;
                return h_point;
            }

            static PyObject *z_get(PointObject *point, void *closure)
            {
                long z = point->x*10 + point->y + (long)closure;
                return PyLong_FromLong(z);
            }

            // legacy getsets
            static PyGetSetDef legacy_getsets[] = {
                {"z", (getter)z_get, NULL, NULL, (void *)2000},
                {NULL}
            };

            static PyType_Slot legacy_slots[] = {
                {Py_tp_getset, legacy_getsets},
                {0, NULL}
            };

            static HPyDef *Point_defines[] = {
                &Point_new,
                NULL
            };
            static HPyType_Spec Point_spec = {
                .name = "mytest.Point",
                .basicsize = sizeof(PointObject),
                .defines = Point_defines,
                .legacy_slots = legacy_slots
            };

            @EXPORT_TYPE("Point", Point_spec)
            @INIT
        """)
        p = mod.Point()
        assert p.z == 2073
