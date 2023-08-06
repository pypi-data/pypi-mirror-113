#ifndef __PAMODULE_H__
#define __PAMODULE_H__
#include "Python.h"
#ifdef __cplusplus
extern "C" {
#endif
/* inits */
static PyObject *pa_initialize(PyObject *self, PyObject *args);
static PyObject *pa_terminate(PyObject *self, PyObject *args);
/* version */
static PyObject *pa_getVersion(PyObject *self, PyObject *args);
/*engine api */
static PyObject *pa_setLogPath(PyObject *self, PyObject *args);
static PyObject *pa_logOff(PyObject *self, PyObject *args);
static PyObject *pa_setChannelProfile(PyObject *self, PyObject *args);
static PyObject *pa_setClientRole(PyObject *self, PyObject *args);
static PyObject *pa_enableWebSdkInteroperability(PyObject *self, PyObject *args);

static PyObject *pa_setVideoProfile(PyObject *self, PyObject *args);
static PyObject *pa_setAudioProfile(PyObject *self, PyObject *args);

static PyObject *pa_joinChannel(PyObject *self, PyObject *args);
static PyObject *pa_leaveChannel(PyObject *self, PyObject *args);

static PyObject *pa_enableVideo(PyObject *self, PyObject *args);
static PyObject *pa_enableAudio(PyObject *self, PyObject *args);
static PyObject *pa_muteLocalVideo(PyObject *self, PyObject *args);
static PyObject *pa_muteLocalAudio(PyObject *self, PyObject *args);
static PyObject *pa_muteAllRemoteVideoStreams(PyObject *self, PyObject *args);
static PyObject *pa_muteAllRemoteAudioStreams(PyObject *self, PyObject *args);
static PyObject *pa_enableDualStreamMode(PyObject *self, PyObject *args);

static PyObject *pa_setParameters(PyObject *self, PyObject *args);
static PyObject *pa_addView(PyObject *self, PyObject *args);

int _stream_callback_cfunction(int streamType, unsigned int uid, void *data, void *userData);
static PyObject *pa_registerAudioObserver(PyObject *self, PyObject *args);
static PyObject *pa_registerVideoObserver(PyObject *self, PyObject *args);

static PyObject *pa_setExternalVideoSource(PyObject *self, PyObject *args);
static PyObject *pa_pushVideoFrame(PyObject *self, PyObject *args);
#ifdef __cplusplus
}
#endif

#endif