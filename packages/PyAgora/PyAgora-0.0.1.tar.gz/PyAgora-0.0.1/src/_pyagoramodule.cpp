#define PY_SSIZE_T_CLEAN
#include "_pyagoramodule.h"
#include "_agoraobject.h"
#include <iostream>

#define min(a, b) (((a) < (b)) ? (a) : (b))

/************************************************************
 *
 * Table of Contents
 *
 * I. Exportable Method Definitions
 * II. Python Object Wrappers
 *     - AudioFrame
 *     - VideoFrame
 * III. Method Implementations
 * IV. Python Module Init
 *
 ************************************************************/

/************************************************************
 *
 * I. Exportable Python Methods
 *
 ************************************************************/

static PyMethodDef paMethods[] = {
    /* inits */
    {"initialize", pa_initialize, METH_VARARGS, "initialize agora engine"},
    {"terminate", pa_terminate, METH_VARARGS, "terminate agora engine"},

    /* version */
    {"getVersion", pa_getVersion, METH_VARARGS, "get version"},

    /*engine api */
    {"setLogPath", pa_setLogPath, METH_VARARGS, "set Log Path"},
    {"logOff", pa_logOff, METH_VARARGS, "Log off"},
    {"setChannelProfile", pa_setChannelProfile, METH_VARARGS,
     "set Channel Profile"},
    {"setClientRole", pa_setClientRole, METH_VARARGS, "set Client Role"},
    {"enableWebSdkInteroperability", pa_enableWebSdkInteroperability,
     METH_VARARGS, "enableWebSdkInteroperability"},

    {"setVideoProfile", pa_setVideoProfile, METH_VARARGS, "setVideoProfile"},
    {"setAudioProfile", pa_setAudioProfile, METH_VARARGS, "setAudioProfile"},

    {"joinChannel", pa_joinChannel, METH_VARARGS, "joinChannel"},
    {"leaveChannel", pa_leaveChannel, METH_VARARGS, "leaveChannel"},

    {"enableVideo", pa_enableVideo, METH_VARARGS, "enable Video"},
    {"enableAudio", pa_enableAudio, METH_VARARGS, "enable Audio"},
    {"muteLocalVideo", pa_muteLocalVideo, METH_VARARGS, "muteLocalVideo"},
    {"muteLocalAudio", pa_muteLocalAudio, METH_VARARGS, "muteLocalAudio"},
    {"muteAllRemoteVideoStreams", pa_muteAllRemoteVideoStreams, METH_VARARGS,
     "muteAllRemoteVideoStreams"},
    {"muteAllRemoteAudioStreams", pa_muteAllRemoteAudioStreams, METH_VARARGS,
     "muteAllRemoteAudioStreams"},
    {"enableDualStreamMode", pa_enableDualStreamMode, METH_VARARGS,
     "enableDualStreamMode"},

    {"setParameters", pa_setParameters, METH_VARARGS, "set Parameters"},
    {"addView", pa_addView, METH_VARARGS, "addView"},

    {"registerAudioObserver", pa_registerAudioObserver, METH_VARARGS,
     "register Audio Observer"},
    {"registerVideoObserver", pa_registerVideoObserver, METH_VARARGS,
     "register Video Observer"},

    {"setExternalVideoSource", pa_setExternalVideoSource, METH_VARARGS,
     "setExternalVideoSource"},
    {"pushVideoFrame", pa_pushVideoFrame, METH_VARARGS,
     "push Video Frame"},

    {NULL, NULL, 0, NULL}};

/************************************************************
 *
 * II. Python Object Wrappers
 *
 ************************************************************/
//
typedef struct {
  // clang-format off
  PyObject_HEAD
  agora::media::IAudioFrameObserver::AudioFrame audioFrame;
  // clang-format on
} _pyAudioFrame;

static PyObject *_pyAgora_pyAudioFrame_get_frame_type(_pyAudioFrame *self,
                                                      void *closure) {
  return PyLong_FromLong(self->audioFrame.type);
}

static PyObject *_pyAgora_pyAudioFrame_get_samples(_pyAudioFrame *self,
                                                   void *closure) {
  return PyLong_FromLong(self->audioFrame.samples);
}

static PyObject *_pyAgora_pyAudioFrame_get_bytesPerSample(_pyAudioFrame *self,
                                                          void *closure) {
  return PyLong_FromLong(self->audioFrame.bytesPerSample);
}

static PyObject *_pyAgora_pyAudioFrame_get_channels(_pyAudioFrame *self,
                                                    void *closure) {
  return PyLong_FromLong(self->audioFrame.channels);
}

static PyObject *_pyAgora_pyAudioFrame_get_samplesPerSec(_pyAudioFrame *self,
                                                         void *closure) {
  return PyLong_FromLong(self->audioFrame.samplesPerSec);
}

static PyObject *_pyAgora_pyAudioFrame_get_buffer(_pyAudioFrame *self,
                                                  void *closure) {
  return PyBytes_FromStringAndSize((char *)self->audioFrame.buffer,
                                   self->audioFrame.samples *
                                       self->audioFrame.bytesPerSample *
                                       self->audioFrame.channels);
}

static PyObject *_pyAgora_pyAudioFrame_get_renderTimeMs(_pyAudioFrame *self,
                                                        void *closure) {
  return PyLong_FromLongLong(self->audioFrame.renderTimeMs);
}

static int _pyAgora_pyAudioFrame_set_frame_type(_pyAudioFrame *self,
                                                PyObject *value,
                                                void *closure) {
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
    return -1;
  }

  if (!PyArg_ParseTuple(value, "i", &self->audioFrame.type)) {
    return -1;
  }
  return 0;
}

static int _pyAgora_pyAudioFrame_set_samples(_pyAudioFrame *self,
                                             PyObject *value, void *closure) {
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
    return -1;
  }

  if (!PyArg_ParseTuple(value, "i", &self->audioFrame.samples)) {
    return -1;
  }
  return 0;
}

static int _pyAgora_pyAudioFrame_set_bytesPerSample(_pyAudioFrame *self,
                                                    PyObject *value,
                                                    void *closure) {
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
    return -1;
  }

  if (!PyArg_ParseTuple(value, "i", &self->audioFrame.bytesPerSample)) {
    return -1;
  }
  return 0;
}

static int _pyAgora_pyAudioFrame_set_channels(_pyAudioFrame *self,
                                              PyObject *value, void *closure) {
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
    return -1;
  }

  if (!PyArg_ParseTuple(value, "i", &self->audioFrame.channels)) {
    return -1;
  }
  return 0;
}

static int _pyAgora_pyAudioFrame_set_samplesPerSec(_pyAudioFrame *self,
                                                   PyObject *value,
                                                   void *closure) {
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
    return -1;
  }

  if (!PyArg_ParseTuple(value, "i", &self->audioFrame.samplesPerSec)) {
    return -1;
  }
  return 0;
}

static int _pyAgora_pyAudioFrame_set_buffer(_pyAudioFrame *self,
                                            PyObject *value, void *closure) {
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
    return -1;
  }
  if (self->audioFrame.buffer) {
    delete self->audioFrame.buffer;
  }
  if (!PyArg_ParseTuple(value, "s", &self->audioFrame.buffer)) {
    return -1;
  }
  return 0;
}

static int _pyAgora_pyAudioFrame_set_renderTimeMs(_pyAudioFrame *self,
                                                  PyObject *value,
                                                  void *closure) {
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
    return -1;
  }

  if (!PyArg_ParseTuple(value, "i", &self->audioFrame.renderTimeMs)) {
    return -1;
  }
  return 0;
}

static PyGetSetDef _pyAgora_pyAudioFrame_getsetters[] = {
    {"type", (getter)_pyAgora_pyAudioFrame_get_frame_type,
     (setter)_pyAgora_pyAudioFrame_set_frame_type, "frame type", NULL},
    {"samples", (getter)_pyAgora_pyAudioFrame_get_samples,
     (setter)_pyAgora_pyAudioFrame_set_samples, "samples", NULL},
    {"bytesPerSample", (getter)_pyAgora_pyAudioFrame_get_bytesPerSample,
     (setter)_pyAgora_pyAudioFrame_set_bytesPerSample, "bytesPerSample", NULL},
    {"channels", (getter)_pyAgora_pyAudioFrame_get_channels,
     (setter)_pyAgora_pyAudioFrame_set_channels, "channels", NULL},
    {"samplesPerSec", (getter)_pyAgora_pyAudioFrame_get_samplesPerSec,
     (setter)_pyAgora_pyAudioFrame_set_samplesPerSec, "samplesPerSec", NULL},
    {"buffer", (getter)_pyAgora_pyAudioFrame_get_buffer,
     (setter)_pyAgora_pyAudioFrame_set_buffer, "buffer", NULL},
    {"renderTimeMs", (getter)_pyAgora_pyAudioFrame_get_renderTimeMs,
     (setter)_pyAgora_pyAudioFrame_set_renderTimeMs, "renderTimeMs", NULL},
    {NULL} /* Sentinel */
};

static void _pyAgora_paAudioFrame_dealloc(_pyAudioFrame *self) {
  Py_TYPE(self)->tp_free((PyObject *)self);
}
static _pyAudioFrame *_create_paAudioFrame_object(void);

// static PyTypeObject _pyAgora_pyAudioFrameType = {
//     PyVarObject_HEAD_INIT(NULL, 0)
//     .tp_name = "agora.AudioFrame",
//     .tp_doc = "Agora Audio Frame",
//     .tp_basicsize = sizeof(_pyAudioFrame),
//     .tp_itemsize = 0,
//     .tp_flags = Py_TPFLAGS_DEFAULT,
//     //.tp_new = _create_paAudioFrame_object,
//     .tp_dealloc = (destructor)_pyAgora_paAudioFrame_dealloc,
//     .tp_getset = _pyAgora_pyAudioFrame_getsetters,
// };
static _pyAudioFrame *_create_paAudioFrame_object(void);

static PyTypeObject _pyAgora_pyAudioFrameType = {
    // clang-format off
    PyVarObject_HEAD_INIT(NULL, 0)
    // clang-format on
    "agora.AudioFrame",                        /*tp_name*/
    sizeof(_pyAudioFrame),                     /*tp_basicsize*/
    0,                                         /*tp_itemsize*/
    (destructor)_pyAgora_paAudioFrame_dealloc, /*tp_dealloc*/
    0,                                         /*tp_print*/
    0,                                         /*tp_getattr*/
    0,                                         /*tp_setattr*/
    0,                                         /*tp_compare*/
    0,                                         /*tp_repr*/
    0,                                         /*tp_as_number*/
    0,                                         /*tp_as_sequence*/
    0,                                         /*tp_as_mapping*/
    0,                                         /*tp_hash */
    0,                                         /*tp_call*/
    0,                                         /*tp_str*/
    0,                                         /*tp_getattro*/
    0,                                         /*tp_setattro*/
    0,                                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,                        /*tp_flags*/
    "Agora Audio Frame",                       /* tp_doc */
    0,                                         /* tp_traverse */
    0,                                         /* tp_clear */
    0,                                         /* tp_richcompare */
    0,                                         /* tp_weaklistoffset */
    0,                                         /* tp_iter */
    0,                                         /* tp_iternext */
    0,                                         /* tp_methods */
    0,                                         /* tp_members */
    _pyAgora_pyAudioFrame_getsetters,          /* tp_getset */
    0,                                         /* tp_base */
    0,                                         /* tp_dict */
    0,                                         /* tp_descr_get */
    0,                                         /* tp_descr_set */
    0,                                         /* tp_dictoffset */
    0,                                         /* tp_init */
    0,                                         /* tp_alloc */
    PyType_GenericNew,                         /* tp_new */
};

static _pyAudioFrame *_create_paAudioFrame_object(void) {
  _pyAudioFrame *obj;

  /* don't allow subclassing */
  obj =
      (_pyAudioFrame *)PyObject_New(_pyAudioFrame, &_pyAgora_pyAudioFrameType);
  return obj;
}

/************************************************************
 *
 * III. Agora Method Implementations
 *
 ************************************************************/

/*************************************************************
 * Init
 *************************************************************/

static PyObject *pa_initialize(PyObject *self, PyObject *args) {
  char *str;
  if (!PyArg_ParseTuple(args, "s", &str)) {
    return NULL;
  }
  CAgoraObject::getInstance()->init(string(str));

  PyObject *result = NULL;
  Py_INCREF(Py_None);
  result = Py_None;
  return result;
}

static PyObject *pa_terminate(PyObject *self, PyObject *args) {
  if (!PyArg_ParseTuple(args, "")) {
    return NULL;
  }
  CAgoraObject::getInstance()->destroy();
  PyObject *result = NULL;
  Py_INCREF(Py_None);
  result = Py_None;
  return result;
}

/*************************************************************
 * Version Info
 *************************************************************/

static PyObject *pa_getVersion(PyObject *self, PyObject *args) {
  if (!PyArg_ParseTuple(args, "")) {
    return NULL;
  }

  return PyBytes_FromString(
      CAgoraObject::getInstance()->getSDKVersion().c_str());
}

/*************************************************************
 * engine api
 *************************************************************/

static PyObject *pa_setLogPath(PyObject *self, PyObject *args) {
  char *str;
  if (!PyArg_ParseTuple(args, "s", &str)) {
    return NULL;
  }

  return PyBool_FromLong(CAgoraObject::getInstance()->setLogPath(string(str)));
}

static PyObject *pa_logOff(PyObject *self, PyObject *args) {
  if (!PyArg_ParseTuple(args, "")) {
    return NULL;
  }

  return PyBool_FromLong(CAgoraObject::getInstance()->logOff());
}

static PyObject *pa_setChannelProfile(PyObject *self, PyObject *args) {
  int profile;
  if (!PyArg_ParseTuple(args, "i", &profile)) {
    return NULL;
  }

  return PyBool_FromLong(
      CAgoraObject::getInstance()->setChannelProfile(profile));
}

static PyObject *pa_setClientRole(PyObject *self, PyObject *args) {
  int role;
  if (!PyArg_ParseTuple(args, "i", &role)) {
    return NULL;
  }

  return PyBool_FromLong(CAgoraObject::getInstance()->setClientRole(role));
}

static PyObject *pa_enableWebSdkInteroperability(PyObject *self,
                                                 PyObject *args) {
  bool enable;
  if (!PyArg_ParseTuple(args, "p", &enable)) {
    return NULL;
  }

  return PyBool_FromLong(
      CAgoraObject::getInstance()->enableWebSdkInteroperability(enable));
}

static PyObject *pa_setVideoProfile(PyObject *self, PyObject *args) {
  int nWidth;
  int nHeight;
  int fps;
  int bitrate;

  if (!PyArg_ParseTuple(args, "iiii", &nWidth, &nHeight, &fps, &bitrate)) {
    return NULL;
  }

  return PyBool_FromLong(CAgoraObject::getInstance()->setVideoProfile(
      nWidth, nHeight, fps, bitrate));
}

static PyObject *pa_setAudioProfile(PyObject *self, PyObject *args) {
  int profile;
  int scenario;

  if (!PyArg_ParseTuple(args, "ii", &profile, &scenario)) {
    return NULL;
  }

  return PyBool_FromLong(
      CAgoraObject::getInstance()->setAudioProfile(profile, scenario));
}

static PyObject *pa_joinChannel(PyObject *self, PyObject *args) {
  char *key;
  char *channel;
  unsigned int uid;

  if (!PyArg_ParseTuple(args, "ssI", &key, &channel, &uid)) {
    return NULL;
  }

  return PyLong_FromLong(CAgoraObject::getInstance()->joinChannel(
      string(key), string(channel), uid));
}

static PyObject *pa_leaveChannel(PyObject *self, PyObject *args) {
  if (!PyArg_ParseTuple(args, "")) {
    return NULL;
  }

  return PyLong_FromLong(CAgoraObject::getInstance()->leaveChannel());
}

static PyObject *pa_enableVideo(PyObject *self, PyObject *args) {
  bool enable;

  if (!PyArg_ParseTuple(args, "p", &enable)) {
    return NULL;
  }

  return PyLong_FromLong(CAgoraObject::getInstance()->enableVideo(enable));
}

static PyObject *pa_enableAudio(PyObject *self, PyObject *args) {
  bool enable;

  if (!PyArg_ParseTuple(args, "p", &enable)) {
    return NULL;
  }

  return PyLong_FromLong(CAgoraObject::getInstance()->enableAudio(enable));
}

static PyObject *pa_muteLocalVideo(PyObject *self, PyObject *args) {
  bool mute;

  if (!PyArg_ParseTuple(args, "p", &mute)) {
    return NULL;
  }

  return PyBool_FromLong(CAgoraObject::getInstance()->muteLocalVideo(mute));
}

static PyObject *pa_muteLocalAudio(PyObject *self, PyObject *args) {
  bool mute;

  if (!PyArg_ParseTuple(args, "p", &mute)) {
    return NULL;
  }

  return PyBool_FromLong(CAgoraObject::getInstance()->muteLocalAudio(mute));
}

static PyObject *pa_muteAllRemoteVideoStreams(PyObject *self, PyObject *args) {
  bool mute;

  if (!PyArg_ParseTuple(args, "p", &mute)) {
    return NULL;
  }

  return PyBool_FromLong(
      CAgoraObject::getInstance()->muteAllRemoteVideoStreams(mute));
}

static PyObject *pa_muteAllRemoteAudioStreams(PyObject *self, PyObject *args) {
  bool mute;

  if (!PyArg_ParseTuple(args, "p", &mute)) {
    return NULL;
  }

  return PyBool_FromLong(
      CAgoraObject::getInstance()->muteAllRemoteAudioStreams(mute));
}

static PyObject *pa_enableDualStreamMode(PyObject *self, PyObject *args) {
  bool enable;

  if (!PyArg_ParseTuple(args, "p", &enable)) {
    return NULL;
  }

  return PyBool_FromLong(
      CAgoraObject::getInstance()->getRtcEngine()->enableDualStreamMode(enable));
}

static PyObject *pa_setParameters(PyObject *self, PyObject *args) {
  char *str;

  if (!PyArg_ParseTuple(args, "s", &str)) {
    return NULL;
  }
  CAgoraObject::getInstance()->setParameters(string(str));
  PyObject *result = NULL;
  Py_INCREF(Py_None);
  result = Py_None;
  return result;
}

static PyObject *pa_addView(PyObject *self, PyObject *args) {
  int handler;

  if (!PyArg_ParseTuple(args, "i", &handler)) {
    return NULL;
  }
  CAgoraObject::getInstance()->addView((void *)handler);
  PyObject *result = NULL;
  Py_INCREF(Py_None);
  result = Py_None;
  return result;
}

/*************************************************************
 * Stream
 *************************************************************/

typedef struct {
  PyObject *callback;
  long main_thread_id;
} PyCallbackContext;

static PyObject *pa_registerAudioObserver(PyObject *self, PyObject *args) {
  PyObject *stream_callback = NULL;

  if (!PyArg_ParseTuple(args, "O", &stream_callback)) {
    return NULL;
  }
  if (stream_callback && (PyCallable_Check(stream_callback) == 0)) {
    PyErr_SetString(PyExc_TypeError, "stream_callback must be callable");
    return NULL;
  }
  if (stream_callback) {
    Py_INCREF(stream_callback);
    // memory leak
    PyCallbackContext *context =
        (PyCallbackContext *)malloc(sizeof(PyCallbackContext));
    ;
    context->callback = stream_callback;
    context->main_thread_id = PyThreadState_Get()->thread_id;
    CAgoraObject::getInstance()->registerAudioFrameObserver(
        _stream_callback_cfunction, context);
  }

  PyObject *result = NULL;
  Py_INCREF(Py_None);
  result = Py_None;
  return result;
}

static PyObject *pa_registerVideoObserver(PyObject *self, PyObject *args) {
  PyObject *stream_callback = NULL;

  if (!PyArg_ParseTuple(args, "O", &stream_callback)) {
    return NULL;
  }
  if (stream_callback && (PyCallable_Check(stream_callback) == 0)) {
    PyErr_SetString(PyExc_TypeError, "stream_callback must be callable");
    return NULL;
  }
  if (stream_callback) {
    Py_INCREF(stream_callback);
    // memory leak
    PyCallbackContext *context =
        (PyCallbackContext *)malloc(sizeof(PyCallbackContext));
    ;
    context->callback = stream_callback;
    context->main_thread_id = PyThreadState_Get()->thread_id;
    CAgoraObject::getInstance()->registerVideoFrameObserver(
        _stream_callback_cfunction, context);
  }

  PyObject *result = NULL;
  Py_INCREF(Py_None);
  result = Py_None;
  return result;
}

static PyObject *pa_setExternalVideoSource(PyObject *self, PyObject *args) {
  bool enable;
  bool texture;

  if (!PyArg_ParseTuple(args, "pp", &enable, &texture)) {
    return NULL;
  }
  CAgoraObject::getInstance()->setExternalVideoSource(enable, texture);
  PyObject *result = NULL;
  Py_INCREF(Py_None);
  result = Py_None;
  return result;    
}

static PyObject *pa_pushVideoFrame(PyObject *self, PyObject *args) {

  agora::media::ExternalVideoFrame frame;
  frame.type = agora::media::ExternalVideoFrame::VIDEO_BUFFER_RAW_DATA;
  frame.format = agora::media::ExternalVideoFrame::VIDEO_PIXEL_I420;
  unsigned int buff_len = 0;
  const char * buff = nullptr;
  if (!PyArg_ParseTuple(args, "z#iiiL", &buff,
                        &buff_len, &frame.stride, &frame.height,
                        &frame.rotation, &frame.timestamp)) {
    std::cout << "PyArg_ParseTuple error" << std::endl;
    return NULL;
  }

  frame.buffer = (void*)buff;
  frame.cropBottom = 0;
  frame.cropLeft = 0;
  frame.cropRight = 0;
  frame.cropTop = 0;

  CAgoraObject::getInstance()->pushVideoFrame(&frame);

  PyObject *result = NULL;
  Py_INCREF(Py_None);
  result = Py_None;
  return result;
}

int _stream_callback_cfunction(int streamType, unsigned int uid, void *data,
                               void *userData) {
  int return_val = -1;
  PyGILState_STATE _state = PyGILState_Ensure();
  PyCallbackContext *context = (PyCallbackContext *)userData;
  PyObject *py_callback = context->callback;
  long main_thread_id = context->main_thread_id;
  PyObject *py_result = nullptr;
  PyObject *py_uid = nullptr;
  PyObject *py_streamType = nullptr;
  PyObject *py_samples = nullptr;
  PyObject *py_channels = nullptr;
  PyObject *py_samplesPerSec = nullptr;
  PyObject *py_inbuffer = nullptr;

  PyObject *py_width = nullptr;
  PyObject *py_height = nullptr;
  PyObject *py_yBuffer = nullptr;
  PyObject *py_uBuffer = nullptr;
  PyObject *py_vBuffer = nullptr;

  const char *outbuffer = nullptr;
  unsigned output_len;
  const char *outbuffer_1 = nullptr;
  unsigned output_len_1;
  const char *outbuffer_2 = nullptr;
  unsigned output_len_2;

  switch (streamType) {
  case STREAM_AUDIO_RECORD:
  case STREAM_AUDIO_PLAYBACK:
  case STREAM_AUDIO_MIX:
  case STREAM_AUDIO_PLAYBACK_BEFORE_MIX: {
    agora::media::IAudioFrameObserver::AudioFrame *pdata =
        (agora::media::IAudioFrameObserver::AudioFrame *)data;
    py_uid = PyLong_FromLong(uid);
    py_streamType = PyLong_FromLong(streamType);
    py_samples = PyLong_FromLong(pdata->samples);
    py_channels = PyLong_FromLong(pdata->channels);
    py_samplesPerSec = PyLong_FromLong(pdata->samplesPerSec);
    py_inbuffer = PyBytes_FromStringAndSize(
        (const char *)pdata->buffer,
        pdata->samples * pdata->bytesPerSample * pdata->channels);
    py_result = PyObject_CallFunctionObjArgs(
        py_callback, py_streamType, py_uid, py_samples, py_channels,
        py_samplesPerSec, py_inbuffer, NULL);

    if (py_result == NULL) {
#ifdef VERBOSE
      fprintf(stderr, "An error occured while using the stream\n");
      fprintf(stderr, "Error message: Could not call callback function\n");
#endif
      PyObject *err = PyErr_Occurred();

      if (err) {
        PyThreadState_SetAsyncExc(main_thread_id, err);
        // Print out a stack trace to help debugging.
        // TODO: make VERBOSE a runtime flag so users can control
        // the amount of logging.
        PyErr_Print();
      }

      goto end;
    }

    // clang-format off
  if (!PyArg_ParseTuple(py_result,
                        "z#",
                        &outbuffer,
                        &output_len)) {
// clang-format on
#ifdef VERBOSE
      fprintf(stderr, "An error occured while using the portaudio stream\n");
      fprintf(stderr, "Error message: Could not parse callback return value\n");
#endif

      PyObject *err = PyErr_Occurred();

      if (err) {
        PyThreadState_SetAsyncExc(main_thread_id, err);
        // Print out a stack trace to help debugging.
        // TODO: make VERBOSE a runtime flag so users can control
        // the amount of logging.
        PyErr_Print();
      }

      return_val = -1;
      goto end;
    }
    if (output_len > 0) {
      agora::media::IAudioFrameObserver::AudioFrame *pdata =
          (agora::media::IAudioFrameObserver::AudioFrame *)data;
      memcpy(pdata->buffer, outbuffer,
             min(output_len,
                 pdata->samples * pdata->bytesPerSample * pdata->channels));
      if (output_len <
          (pdata->samples * pdata->bytesPerSample * pdata->channels)) {
        memset((char *)pdata->buffer + output_len, 0,
               (pdata->samples * pdata->bytesPerSample * pdata->channels) -
                   output_len);
      }
    }
    break;
  }

  case STREAM_VIDEO_CAPTURE:
  case STREAM_VIDEO_RENDER: {
    agora::media::IVideoFrameObserver::VideoFrame *pdata =
        (agora::media::IVideoFrameObserver::VideoFrame *)data;
    py_uid = PyLong_FromLong(uid);
    py_streamType = PyLong_FromLong(streamType);
    py_width = PyLong_FromLong(pdata->width);
    py_height = PyLong_FromLong(pdata->height);
    py_yBuffer = PyBytes_FromStringAndSize((const char *)pdata->yBuffer,
                                           pdata->width * pdata->height);
    py_uBuffer = PyBytes_FromStringAndSize((const char *)pdata->uBuffer,
                                           pdata->width * pdata->height / 4);
    py_vBuffer = PyBytes_FromStringAndSize((const char *)pdata->vBuffer,
                                           pdata->width * pdata->height / 4);
    py_result = PyObject_CallFunctionObjArgs(py_callback, py_streamType, py_uid,
                                             py_width, py_height, py_yBuffer,
                                             py_uBuffer, py_vBuffer, NULL);

    if (py_result == NULL) {
#ifdef VERBOSE
      fprintf(stderr, "An error occured while using the stream\n");
      fprintf(stderr, "Error message: Could not call callback function\n");
#endif
      PyObject *err = PyErr_Occurred();

      if (err) {
        PyThreadState_SetAsyncExc(main_thread_id, err);
        // Print out a stack trace to help debugging.
        // TODO: make VERBOSE a runtime flag so users can control
        // the amount of logging.
        PyErr_Print();
      }

      goto end;
    }

    // clang-format off
  if (!PyArg_ParseTuple(py_result,
                        "z#z#z#",
                        &outbuffer,
                        &output_len,
                        &outbuffer_1,
                        &output_len_1,
                        &outbuffer_2,
                        &output_len_2)) {
// clang-format on
#ifdef VERBOSE
      fprintf(stderr, "An error occured while using the portaudio stream\n");
      fprintf(stderr, "Error message: Could not parse callback return value\n");
#endif

      PyObject *err = PyErr_Occurred();

      if (err) {
        PyThreadState_SetAsyncExc(main_thread_id, err);
        // Print out a stack trace to help debugging.
        // TODO: make VERBOSE a runtime flag so users can control
        // the amount of logging.
        PyErr_Print();
      }

      return_val = -1;
      goto end;
    }

    if (output_len > 0) {
      int buflen = pdata->width * pdata->height;
      memcpy(pdata->yBuffer, outbuffer, min(output_len, buflen));
      if (output_len < buflen) {
        memset((char *)pdata->yBuffer + output_len, 0, buflen - output_len);
      }
    }
    if (output_len_1 > 0) {
      int buflen = pdata->width * pdata->height / 4;
      memcpy(pdata->uBuffer, outbuffer_1, min(output_len_1, buflen));
      if (output_len_1 < buflen) {
        memset((char *)pdata->uBuffer + output_len_1, 0, buflen - output_len_1);
      }
    }
    if (output_len_2 > 0) {
      int buflen = pdata->width * pdata->height / 4;
      memcpy(pdata->vBuffer, outbuffer_2, min(output_len_2, buflen));
      if (output_len_2 < buflen) {
        memset((char *)pdata->vBuffer + output_len_2, 0, buflen - output_len_2);
      }
    }

    break;
  }
  default:
    break;
  }

end:
  Py_XDECREF(py_result);
  Py_XDECREF(py_uid);
  Py_XDECREF(py_streamType);
  Py_XDECREF(py_samples);
  Py_XDECREF(py_channels);
  Py_XDECREF(py_samplesPerSec);
  Py_XDECREF(py_inbuffer);

  Py_XDECREF(py_width);
  Py_XDECREF(py_height);
  Py_XDECREF(py_yBuffer);
  Py_XDECREF(py_uBuffer);
  Py_XDECREF(py_vBuffer);

  PyGILState_Release(_state);
  return return_val;
}

/************************************************************
 *
 * IV. Python Module Init
 *
 ************************************************************/
#if PY_MAJOR_VERSION >= 3
#define ERROR_INIT NULL
#else
#define ERROR_INIT /**/
#endif

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = { //
    PyModuleDef_HEAD_INIT,
    "_pyagorasdk",
    NULL,
    -1,
    paMethods,
    NULL,
    NULL,
    NULL,
    NULL};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit__pyagorasdk(void)
#else
init_pyagorasdk(void)
#endif
{
  PyObject *m;

  PyEval_InitThreads();

  if (PyType_Ready(&_pyAgora_pyAudioFrameType) < 0) {
    return ERROR_INIT;
  }
#if PY_MAJOR_VERSION >= 3
  m = PyModule_Create(&moduledef);
#else
  m = Py_InitModule("_pyagorasdk", paMethods);
#endif

  Py_INCREF(&_pyAgora_pyAudioFrameType);
  PyModule_AddIntConstant(m, "StreamAudioRecord", STREAM_AUDIO_RECORD);
  PyModule_AddIntConstant(m, "StreamAudioPlay", STREAM_AUDIO_PLAYBACK);
  PyModule_AddIntConstant(m, "StreamAudioMix", STREAM_AUDIO_MIX);
  PyModule_AddIntConstant(m, "StreamAudioPlayBeforeMix", STREAM_AUDIO_PLAYBACK_BEFORE_MIX);
  PyModule_AddIntConstant(m, "StreamVideoCap", STREAM_VIDEO_CAPTURE);
  PyModule_AddIntConstant(m, "StreamVideoRender", STREAM_VIDEO_RENDER);

#if PY_MAJOR_VERSION >= 3
  return m;
#endif
}