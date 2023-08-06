#ifndef CAGORAOBJECT_H
#define CAGORAOBJECT_H

#include <Memory>
#include <mutex>
#include <unordered_map>
#include <vector>
#include <functional>

#include <IAgoraRtcEngine.h>
#include <IAgoraMediaEngine.h>

using namespace agora::rtc;
using namespace std;

typedef struct{
    string id;
    string name;
}DeviceInfo;
enum STREAM_TYPE {
//AUDIO
    STREAM_AUDIO_RECORD = 0,
    STREAM_AUDIO_PLAYBACK, 
    STREAM_AUDIO_MIX, 
    STREAM_AUDIO_PLAYBACK_BEFORE_MIX, 

//VIDEO
    STREAM_VIDEO_CAPTURE = 10, 
    STREAM_VIDEO_RENDER
};
typedef std::vector<DeviceInfo> VDevices;
typedef std::function<void(int, unsigned int, void*, void*)> StreamObserver;

class CAgoraObject: public agora::rtc::IRtcEngineEventHandler,
                    public agora::media::IAudioFrameObserver,
                    public agora::media::IVideoFrameObserver

{
public:
    void init(string appId);
    void destroy();
    string getSDKVersion();

    bool setLogPath(const string &strDir);
    bool logOff();
    bool setChannelProfile(int channelType);
    bool setClientRole(int roleType);
    bool enableWebSdkInteroperability(bool bEnable);

    bool setVideoProfile(int nWidth,int nHeight, int fps, int bitrate);
    bool setAudioProfile(int profile, int scenario);

    int joinChannel(const string& key, const string& channel, unsigned int uid);
    int leaveChannel();
  
    int enableVideo(bool enabled);
    int enableAudio(bool enabled);
    bool muteLocalVideo(bool bMute);
    bool muteLocalAudio(bool bMute);
    bool muteAllRemoteVideoStreams(bool bMute);
    bool muteAllRemoteAudioStreams(bool bMute);

    void setParameters(const string& key);
    //string getParameters();
    void addView(void* handler);

    VDevices getRecordingDeviceList();
    VDevices getPlayoutDeviceList();
    VDevices getVideoDeviceList();

    int setRecordingDevice(const string& guid);
    int setPlayoutDevice(const string& guid);
    int setVideoDevice(const string& guid);
    string getCurrentVideoDevice();
    string getCurrentPlaybackDevice();
    string getCurrentRecordingDevice();
    bool setRecordingIndex(int nIndex);
    bool setPlayoutIndex(int nIndex);
    bool setVideoIndex(int nIndex);

    void setExternalVideoSource(bool enable, bool useTexture);
    void pushVideoFrame(agora::media::ExternalVideoFrame *frame);

    bool setBeautyEffectOptions(bool enabled, BeautyOptions& options);
public:
    //IRtcEngineEventHandler
    virtual void onVideoStopped() override;
    virtual void onJoinChannelSuccess(const char* channel, uid_t uid, int elapsed) override;
    virtual void onLeaveChannel(const RtcStats& stat) override;
    virtual void onUserJoined(uid_t uid, int elapsed) override;
    virtual void onUserOffline(uid_t uid, USER_OFFLINE_REASON_TYPE reason) override;
    virtual void onFirstLocalVideoFrame(int width, int height, int elapsed) override;
    virtual void onFirstRemoteVideoDecoded(uid_t uid, int width, int height, int elapsed) override;
    virtual void onFirstRemoteVideoFrame(uid_t uid, int width, int height, int elapsed) override;
    virtual void onLocalVideoStats(const LocalVideoStats &stats) override;
    virtual void onRemoteVideoStats(const RemoteVideoStats &stats) override;
    virtual void onLocalAudioStats(const LocalAudioStats& stats) override;
    virtual void onRemoteAudioStats(const RemoteAudioStats& stats) override;
    virtual void onRtcStats(const RtcStats &stats) override;
    virtual void onVideoDeviceStateChanged(const char* deviceId, int deviceType, int deviceState) override;
    virtual void onAudioDeviceStateChanged(const char* deviceId, int deviceType, int deviceState) override;

public:
    void registerAudioFrameObserver(StreamObserver cb, void* userdata);
    void registerVideoFrameObserver(StreamObserver cb, void* userdata);
public:
    //IAudioFrameObserver
    virtual bool onRecordAudioFrame(AudioFrame& audioFrame);
	virtual bool onPlaybackAudioFrame(AudioFrame& audioFrame);
	virtual bool onMixedAudioFrame(AudioFrame& audioFrame);
	virtual bool onPlaybackAudioFrameBeforeMixing(unsigned int uid, AudioFrame& audioFrame);

    //IVideoFrameObserver 
	virtual bool onCaptureVideoFrame(VideoFrame& videoFrame);
    virtual VIDEO_FRAME_TYPE getVideoFormatPreference() { return FRAME_TYPE_YUV420; };
	virtual bool onRenderVideoFrame(unsigned int uid, VideoFrame& videoFrame);
public:
    agora::rtc::IRtcEngine* getRtcEngine(){return m_rtcEngine;};
public:
    static CAgoraObject* getInstance();
    static CAgoraObject* m_pInstance;
    static std::mutex    m_mutex;

private:
    explicit CAgoraObject();
    ~CAgoraObject();

    agora::rtc::IRtcEngine* m_rtcEngine = nullptr;
    
    std::unordered_map<int, void*> m_mapViews;

    AVideoDeviceManager* m_videoDeviceManager;
    AAudioDeviceManager* m_audioDeviceManager;

    StreamObserver m_audioObserver = nullptr;
    void* m_audioContext = nullptr;
    StreamObserver m_videoObserver = nullptr;
    void* m_videoContext = nullptr;
    bool m_logOff = false;
};

#endif // CAGORAOBJECT_H
