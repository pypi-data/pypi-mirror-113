__author__ = "Fan"
__version__ = "0.0.1"
__docformat__ = "restructuredtext en"

import sys
import numpy as np

# attempt to import PortAudio
try:
    import _pyagorasdk as pa
except ImportError:
    print("Could not import the PyAgoraSdk C module '_pyagorasdk'.")
    raise

############################################################
# GLOBALS
############################################################

##### Audio and Video observer stream type #####

paStreamAudioRecord = pa.StreamAudioRecord
paStreamAudioPlay = pa.StreamAudioPlay
paStreamAudioMix = pa.StreamAudioMix
paStreamAudioPlayBeforeMix = pa.StreamAudioPlayBeforeMix
paStreamVideoCap = pa.StreamVideoCap
paStreamVideoRender = pa.StreamVideoRender

############################################################
# Convenience Functions
############################################################
def initialize(appid):
    """
    init agora sdk.

    :param appid: appid string.
    :raises NULL.
    :rtype: NULL
    """

    return pa.initialize(appid)


def terminate():
    """
    terminate agora sdk.

    :param NULL.
    :raises NULL.
    :rtype: NULL
    """

    return pa.terminate()


def getVersion():
    """
    Returns py agora sdk version.

    :rtype: string
    """

    return pa.getVersion()


def setLogPath(path: str):
    """
    set agora sdk log path.

    :param path: path string.
    :raises NULL.
    :rtype: bool
    """

    return pa.setLogPath()

def logOff():
    """
    cancel agora python sdk log .

    :param .
    :raises NULL.
    :rtype: NULL
    """

    return pa.logOff()

def setChannelProfile(profile: int):
    """
    set Channel Profile.

    :param profile: 
            - 0: Communication
            - 1: Live streaming
            - 2: Gaming
    :raises NULL.
    :rtype: bool
    """

    return pa.setChannelProfile(profile)


def setClientRole(role: int):
    """
    set Client Role.

    :param role:
            - 1: Host
            - 2: Audience
    :raises NULL.
    :rtype: bool
    """

    return pa.setClientRole(role)


def enableWebSdkInteroperability(enable: bool):
    """
    enable Web Sdk Interoperability.

    :param enable: enable.
    :raises NULL.
    :rtype: bool
    """

    return pa.enableWebSdkInteroperability(enable)


def setVideoProfile(width: int, height: int, fps: int, bitrate: int):
    """
    set agora video profile.

    :param width: width.
    :param height: height.
    :param fps: fps.
    :param bitrate: bitrate.
    :raises NULL.
    :rtype: bool
    """

    return pa.setVideoProfile(width, height, fps, bitrate)


def setAudioProfile(profile: int, scenario: int):
    """
    set agora audio profile.

    :param profile: profile.
    :param scenario: scenario.
    :raises NULL.
    :rtype: bool
    """

    return pa.setAudioProfile(profile, scenario)


def joinChannel(token: str, channel: str, uid: int):
    """
    join Channel.

    :param token: token.
    :param channel: channel name.
    :param uid: uid.
    :raises NULL.
    :rtype: bool
    """

    return pa.joinChannel(token, channel, uid)


def leaveChannel():
    """
    leave Channel.

    :param NULL.
    :raises NULL.
    :rtype: bool
    """

    return pa.leaveChannel()


def enableVideo(enable: bool):
    """
    enable video.

    :param enable: enable.
    :raises NULL.
    :rtype: bool
    """

    return pa.enableVideo(enable)


def enableAudio(enable: bool):
    """
    enableAudio.

    :param enable: enable.
    :raises NULL.
    :rtype: bool
    """

    return pa.enableAudio(enable)


def muteLocalVideo(mute: bool):
    """
    mute local video.

    :param mute: mute.
    :raises NULL.
    :rtype: bool
    """

    return pa.muteLocalVideo(mute)


def muteLocalAudio(mute: bool):
    """
    mute local audio.

    :param mute: mute.
    :raises NULL.
    :rtype: bool
    """

    return pa.muteLocalAudio(mute)


def muteAllRemoteVideoStreams(mute: bool):
    """
    mute all remote video streams.

    :param mute: mute.
    :raises NULL.
    :rtype: bool
    """

    return pa.muteAllRemoteVideoStreams(mute)


def muteAllRemoteAudioStreams(mute: bool):
    """
    mute all remote audio streams.

    :param mute: mute.
    :raises NULL.
    :rtype: bool
    """

    return pa.muteAllRemoteAudioStreams(mute)

def enableDualStreamMode(enable: bool):
    """
    enable Dual Stream Mode.

    :param enable: enable.
    :raises NULL.
    :rtype: bool
    """

    return pa.enableDualStreamMode(enable)

def setParameters(param: str):
    """
    set private parameter.

    :param param: param json string.
    :raises NULL.
    :rtype: bool
    """

    return pa.setParameters(param)


def addView(view: int):
    """
    add view for rendering.

    :param view: view handler.
    :raises NULL.
    :rtype: bool
    """

    return pa.addView(view)

def registerAudioObserver(observer: object):
    """
    register Audio Observer.

    :param observer: Specifies a observer callback function  .
        To use the operation, specify a callback that conforms
        to the following signature:
        .. code-block:: python

        observer(streamType,  # Stream Type:0 for recorder, 1 for playback, 2 for mix, 3 for playback before mix
                uid,  # user id
                audioFrame) # AudioFrame
    :raises NULL.
    :rtype: bool
    """

    return pa.registerAudioObserver(observer)

def registerVideoObserver(observer: object):
    """
    register Video Observer.

    :param observer: Specifies a observer callback function  .
        To use the operation, specify a callback that conforms
        to the following signature:
        .. code-block:: python

        observer(streamType,  # Stream Type:10 for cappture, 11 for render
                uid,  # user id
                videoFrame) # VideoFrame
    :raises NULL.
    :rtype: bool
    """

    return pa.registerVideoObserver(observer)

def setExternalVideoSource(enable: bool, texture: bool):
    """
    setExternalVideoSource.

    :param enable: enable external Video Source .
           texture: use texture
    :raises NULL.
    :rtype: bool
    """

    return pa.setExternalVideoSource(enable, texture)

def pushVideoFrame(frame: bytes, stride: int, height: int, rotation: int, timestamp: np.int64):
    """
    register Video Observer.

    :param frame: frame buffer .
           stride: frame stride
           height: frame height
           rotation: frame rotation
           timestamp: frame capture timestamp
    :raises NULL.
    :rtype: bool
    """

    return pa.pushVideoFrame(frame, stride, height, rotation, timestamp)

if __name__ == '__main__':
    print(getVersion())
