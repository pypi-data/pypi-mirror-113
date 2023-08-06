#include <cassert>
#include <string>
#include <iostream>
#include <stdbool.h>
#include "_agoraobject.h"
#include "_viewsmanager.h"

CAgoraObject* CAgoraObject::getInstance()
{
    std::lock_guard<std::mutex> autoLock(m_mutex);
    if(nullptr == m_pInstance)
        m_pInstance = new CAgoraObject();

    return m_pInstance;
}

CAgoraObject* CAgoraObject::m_pInstance = nullptr;
std::mutex  CAgoraObject::m_mutex;

CAgoraObject::CAgoraObject():
    m_rtcEngine(nullptr)
{
}

CAgoraObject::~CAgoraObject()
{
}

void CAgoraObject::init(string appId)
{
    if(m_rtcEngine)
    {
        m_rtcEngine->release();
    }  
    m_rtcEngine = createAgoraRtcEngine();
    agora::rtc::RtcEngineContext context;
    context.eventHandler = this;

    context.appId = appId.c_str();

    m_rtcEngine->initialize(context);

    m_videoDeviceManager  = new AVideoDeviceManager(m_rtcEngine);
    m_audioDeviceManager  = new AAudioDeviceManager(m_rtcEngine);
}

void CAgoraObject::destroy()
{
    if(m_rtcEngine)
    {
        m_rtcEngine->release();
        m_rtcEngine = nullptr;
    }       
}

string CAgoraObject::getSDKVersion()
{
	int nBuildNumber = 0;
	const char *lpszEngineVer = getAgoraRtcEngineVersion(&nBuildNumber);

	string strEngineVer(lpszEngineVer);

	return strEngineVer;
}

int CAgoraObject::joinChannel(const string& key, const string& channel, unsigned int uid)
{
    if (channel.empty()) {
        return -1;
    }

    VideoCanvas canvas;
	canvas.renderMode = RENDER_MODE_FIT;
	canvas.uid = uid;
	canvas.view = CViewsManager::getInstance()->GetFirstView();

	int nRet = m_rtcEngine->setupLocalVideo(canvas);

    m_rtcEngine->startPreview();
    int r = m_rtcEngine->joinChannel(key.c_str(), channel.c_str(), "", uid);

    return r;
}

int CAgoraObject::leaveChannel()
{
    int r = m_rtcEngine->leaveChannel();
    return r;
}

int CAgoraObject::enableVideo(bool enabled)
{
    return enabled ? m_rtcEngine->enableVideo() : m_rtcEngine->disableVideo();
}

int CAgoraObject::enableAudio(bool enabled)
{
    return enabled ? m_rtcEngine->enableAudio() : m_rtcEngine->disableAudio();
}

bool CAgoraObject::setLogPath(const string &strDir)
{
    int ret = 0;

    RtcEngineParameters rep(*m_rtcEngine);
    ret = rep.setLogFile(strDir.c_str());

    return ret == 0 ? true : false;
}

bool CAgoraObject::logOff()
{
    int ret = 0;
    m_logOff = true;
    return ret == 0 ? true : false;
}

bool CAgoraObject::setChannelProfile(int channelType)
{
    int ret = 0;
    ret = m_rtcEngine->setChannelProfile((CHANNEL_PROFILE_TYPE)channelType);

    return ret == 0 ? true : false;
}

bool CAgoraObject::setClientRole(int roleType)
{
    int ret = 0;

    ret = m_rtcEngine->setClientRole((CLIENT_ROLE_TYPE)roleType);

    return ret == 0 ? true : false;
}

bool CAgoraObject::enableWebSdkInteroperability(bool bEnable)
{
    RtcEngineParameters rep(*m_rtcEngine);

    int	nRet = rep.enableWebSdkInteroperability(static_cast<bool>(bEnable));

    return nRet == 0 ? true : false;
}

VDevices CAgoraObject::getRecordingDeviceList()
{
    VDevices devices;

    if (!m_audioDeviceManager || !m_audioDeviceManager->get())
        return devices;

    agora::util::AutoPtr<IAudioDeviceCollection> spCollection((*m_audioDeviceManager)->enumerateRecordingDevices());
    if (!spCollection)
        return devices;
    char name[MAX_DEVICE_ID_LENGTH], guid[MAX_DEVICE_ID_LENGTH];
    int count = spCollection->getCount();
    if (count > 0)
    {
        for (int i = 0; i < count; i++)
        {
            if (!spCollection->getDevice(i, name, guid))
            {
                DeviceInfo info;
                info.id   = guid;
                info.name = name;
                devices.push_back(info);
            }
        }
    }
    return devices;
}

VDevices CAgoraObject::getPlayoutDeviceList()
{
    VDevices devices;

    if (!m_audioDeviceManager || !m_audioDeviceManager->get())
        return devices;

    agora::util::AutoPtr<IAudioDeviceCollection> spCollection((*m_audioDeviceManager)->enumeratePlaybackDevices());
    if (!spCollection)
        return devices;
    char name[MAX_DEVICE_ID_LENGTH], guid[MAX_DEVICE_ID_LENGTH];
    int count = spCollection->getCount();
    if (count > 0)
    {
        for (int i = 0; i < count; i++)
        {
            if (!spCollection->getDevice(i, name, guid))
            {
                DeviceInfo info;
                info.id   = guid;
                info.name = name;
                devices.push_back(info);
            }
        }
    }
    return devices;
}

VDevices CAgoraObject::getVideoDeviceList()
{
	m_rtcEngine->enableVideo();
    VDevices devices;

    if (!m_videoDeviceManager || !m_videoDeviceManager->get())
        return devices;

    agora::util::AutoPtr<IVideoDeviceCollection> spCollection((*m_videoDeviceManager)->enumerateVideoDevices());
    if (!spCollection)
        return devices;
    char name[MAX_DEVICE_ID_LENGTH], guid[MAX_DEVICE_ID_LENGTH];
    int count = spCollection->getCount();
    if (count > 0)
    {
        for (int i = 0; i < count; i++)
        {
            if (!spCollection->getDevice(i, name, guid))
            {
                DeviceInfo info;
                info.id   = guid;
                info.name = name;
                devices.push_back(info);
            }
        }
    }
    return devices;
}

string CAgoraObject::getCurrentVideoDevice()
{
     if (!m_videoDeviceManager || !m_videoDeviceManager->get())
         return string("");
     char deviceId[MAX_DEVICE_ID_LENGTH] = {0};
     string strId("");
     if(0 == (*m_videoDeviceManager)->getDevice(deviceId)){
         strId = string(deviceId);
     }
     return strId;
}

string CAgoraObject::getCurrentPlaybackDevice()
{
    if (!m_audioDeviceManager || !m_audioDeviceManager->get())
        return string("");
    char deviceId[MAX_DEVICE_ID_LENGTH] = {0};
    string strId("");
    if(0 == (*m_videoDeviceManager)->getDevice(deviceId)){
        strId = string(deviceId);
    }
    return strId;
}

string CAgoraObject::getCurrentRecordingDevice()
{
    if (!m_audioDeviceManager || !m_audioDeviceManager->get())
        return string("");
    char deviceId[MAX_DEVICE_ID_LENGTH] = {0};
    string strId("");
    if(0 == (*m_audioDeviceManager)->getPlaybackDevice(deviceId)){
        strId = string(deviceId);
    }
    return strId;
}

int CAgoraObject::setRecordingDevice(const string& guid)
{
    if (guid.empty())
        return -1;

    if (!m_audioDeviceManager || !m_audioDeviceManager->get())
        return -1;
    return (*m_audioDeviceManager)->setRecordingDevice(guid.c_str());
}

int CAgoraObject::setPlayoutDevice(const string& guid)
{
    if (guid.empty())
        return -1;

    if (!m_audioDeviceManager || !m_audioDeviceManager->get())
        return -1;
    return (*m_audioDeviceManager)->setPlaybackDevice(guid.c_str());
}

int CAgoraObject::setVideoDevice(const string& guid)
{
    if (guid.empty())
        return -1;

    if (!m_videoDeviceManager || !m_videoDeviceManager->get())
        return -1;
    return (*m_videoDeviceManager)->setDevice(guid.c_str());
}

bool CAgoraObject::setVideoProfile(int nWidth,int nHeight, int fps, int bitrate)
{
    int res = 0;
    VideoEncoderConfiguration vec;

    vec = VideoEncoderConfiguration(nWidth,nHeight,(FRAME_RATE)fps,bitrate,ORIENTATION_MODE_FIXED_LANDSCAPE);
    res = m_rtcEngine->setVideoEncoderConfiguration(vec);

    return res ==0 ? true : false;
}

bool CAgoraObject::setAudioProfile(int profile, int scenario)
{
    int res = 0;
    res = m_rtcEngine->setAudioProfile((AUDIO_PROFILE_TYPE)profile, (AUDIO_SCENARIO_TYPE)scenario);

    return res ==0 ? true : false;
}

bool CAgoraObject::setRecordingIndex(int nIndex)
{
    int res = 0;
   if (!m_audioDeviceManager || !m_audioDeviceManager->get())
        return false;

    agora::util::AutoPtr<IAudioDeviceCollection> spCollection((*m_audioDeviceManager)->enumerateRecordingDevices());
    if (!spCollection)
        return false;
    char name[MAX_DEVICE_ID_LENGTH], guid[MAX_DEVICE_ID_LENGTH];
    int count = spCollection->getCount();
    assert(res < count);
    spCollection->getDevice(nIndex,name,guid);
    res = spCollection->setDevice(guid);

    return res ==0 ? true:false;
}

bool CAgoraObject::setPlayoutIndex(int nIndex)
{
    int res = 0;
    if (!m_audioDeviceManager || !m_audioDeviceManager->get())
        return false;

    agora::util::AutoPtr<IAudioDeviceCollection> spCollection((*m_audioDeviceManager)->enumeratePlaybackDevices());
    if (!spCollection)
        return false;
    char name[MAX_DEVICE_ID_LENGTH], guid[MAX_DEVICE_ID_LENGTH];
    int count = spCollection->getCount();
    assert(res < count);
    spCollection->getDevice(nIndex,name,guid);
    res = spCollection->setDevice(guid);

    return res ==0 ? true:false;
}

bool CAgoraObject::setVideoIndex(int nIndex)
{
    int res = 0;

    if (!m_videoDeviceManager || !m_videoDeviceManager->get())
        return false;

    agora::util::AutoPtr<IVideoDeviceCollection> spCollection((*m_videoDeviceManager)->enumerateVideoDevices());
    if (!spCollection)
        return false;
    char name[MAX_DEVICE_ID_LENGTH], guid[MAX_DEVICE_ID_LENGTH];
    int count = spCollection->getCount();
    assert(nIndex < count);
    spCollection->getDevice(nIndex,name,guid);
    res = spCollection->setDevice(guid);

    return res == 0 ? true : false;
}

void CAgoraObject::setExternalVideoSource(bool enable, bool useTexture) 
{
    agora::util::AutoPtr<agora::media::IMediaEngine> mediaEngine;
	mediaEngine.queryInterface(m_rtcEngine, agora::AGORA_IID_MEDIA_ENGINE);
	mediaEngine->setExternalVideoSource(enable, useTexture);
}

void CAgoraObject::pushVideoFrame(agora::media::ExternalVideoFrame *frame) 
{
    agora::util::AutoPtr<agora::media::IMediaEngine> mediaEngine;
	mediaEngine.queryInterface(m_rtcEngine, agora::AGORA_IID_MEDIA_ENGINE);
	mediaEngine->pushVideoFrame(frame);
}

bool CAgoraObject::muteLocalVideo(bool bMute)
{
     int nRet = 0;

    RtcEngineParameters rep(*m_rtcEngine);
    nRet = rep.enableLocalVideo(!bMute);

    return nRet == 0 ? true : false;
}

bool CAgoraObject::muteLocalAudio(bool bMute)
{
    int nRet = 0;

    RtcEngineParameters rep(*m_rtcEngine);
    nRet = m_rtcEngine->enableLocalAudio(!bMute);

    return nRet == 0 ? true : false;
}

bool CAgoraObject::muteAllRemoteVideoStreams(bool bMute)
{
     int nRet = 0;

    RtcEngineParameters rep(*m_rtcEngine);
    nRet = rep.muteAllRemoteVideoStreams(bMute);

    return nRet == 0 ? true : false;
}

bool CAgoraObject::muteAllRemoteAudioStreams(bool bMute)
{
    int nRet = 0;

    RtcEngineParameters rep(*m_rtcEngine);
    nRet = m_rtcEngine->muteAllRemoteAudioStreams(bMute);

    return nRet == 0 ? true : false;
}

bool CAgoraObject::setBeautyEffectOptions(bool enabled, BeautyOptions& options)
{
	int nRet = 0;

	nRet = m_rtcEngine->setBeautyEffectOptions(enabled, options);
	return nRet == 0 ? true : false;
}

void CAgoraObject::setParameters(const string& key) 
{
    AParameter rep(*m_rtcEngine);
    std::cout<<"setParameters:"<<key.c_str()<<endl;
	rep->setParameters(key.c_str());
}

void CAgoraObject::addView(void* handler) {
    CViewsManager::getInstance()->AddView(handler);
}

void CAgoraObject::onVideoStopped()
{

}

void CAgoraObject::onJoinChannelSuccess(const char* channel, uid_t uid, int elapsed)
{

}

void CAgoraObject::onLeaveChannel(const RtcStats& stat)
{
    m_mapViews.clear();
	CViewsManager::getInstance()->FreeAllView();
}

void CAgoraObject::onUserJoined(uid_t uid, int elapsed)
{
    VideoCanvas canvas;
	canvas.renderMode = RENDER_MODE_FIT;
	canvas.uid = uid;
	canvas.view = CViewsManager::getInstance()->GetOneFreeView();

	m_mapViews.insert(std::make_pair(canvas.uid, canvas.view));
	m_rtcEngine->setupRemoteVideo(canvas);
 }

void CAgoraObject::onUserOffline(uid_t uid, USER_OFFLINE_REASON_TYPE reason)
{
    auto it = m_mapViews.find(uid);
	if (it != m_mapViews.end())
	{
		CViewsManager::getInstance()->FreeView(it->second);
		m_mapViews.erase(it);
	}
}

void CAgoraObject::onFirstLocalVideoFrame(int width, int height, int elapsed)
{

}

void CAgoraObject::onFirstRemoteVideoDecoded(uid_t uid, int width, int height, int elapsed)
{

}

void CAgoraObject::onFirstRemoteVideoFrame(uid_t uid, int width, int height, int elapsed)
{

}

void CAgoraObject::onLocalVideoStats(const LocalVideoStats &stats)
{
    if(m_logOff==true) return;
    std::cout<<"onLocalVideoStats sentBitrate:"<<stats.sentBitrate<<" sentFrameRate:"<<stats.sentFrameRate<<" encoderOutputFrameRate:"<<stats.encoderOutputFrameRate
    <<" rendererOutputFrameRate:"<<stats.rendererOutputFrameRate<<" targetBitrate:"<<stats.targetBitrate<<" targetFrameRate:"<<stats.targetFrameRate<<" encodedBitrate:"<<stats.encodedBitrate
    <<" encodedBitrate:"<<stats.encodedBitrate<<" encodedFrameWidth:"<<stats.encodedFrameWidth<<" encodedFrameHeight:"<<stats.encodedFrameHeight<<" encodedFrameCount:"<<stats.encodedFrameCount
    <<" codecType:"<<stats.codecType<<" txPacketLossRate:"<<stats.txPacketLossRate<<" captureFrameRate:"<<stats.captureFrameRate//<<"captureBrightnessLevel:"<<stats.captureBrightnessLevel
    <<std::endl;
}

void CAgoraObject::onRemoteVideoStats(const RemoteVideoStats &stats)
{
    if(m_logOff==true) return;
    std::cout<<"onRemoteVideoStats uid:"<<stats.uid<<" delay:"<<stats.delay<<" width:"<<stats.width
    <<" height:"<<stats.height<<" receivedBitrate:"<<stats.receivedBitrate<<" decoderOutputFrameRate:"<<stats.decoderOutputFrameRate<<" rendererOutputFrameRate:"<<stats.rendererOutputFrameRate
    <<" packetLossRate:"<<stats.packetLossRate<<" rxStreamType:"<<stats.rxStreamType<<" totalFrozenTime:"<<stats.totalFrozenTime<<" frozenRate:"<<stats.frozenRate
    //<<"totalActiveTime:"<<stats.totalActiveTime<<"publishDuration:"<<stats.publishDuration
    <<std::endl;
}

void CAgoraObject::onLocalAudioStats(const LocalAudioStats& stats)
{
    if(m_logOff==true) return;
    std::cout<<"onLocalAudioStats numChannels:"<<stats.numChannels<<" sentSampleRate:"<<stats.sentSampleRate<<" sentBitrate:"<<stats.sentBitrate
    <<" txPacketLossRate:"<<stats.txPacketLossRate
    <<std::endl;
}

void CAgoraObject::onRemoteAudioStats(const RemoteAudioStats& stats)
{
    if(m_logOff==true) return;
    std::cout<<"onRemoteAudioStats uid:"<<stats.uid<<" quality:"<<stats.quality<<" networkTransportDelay:"<<stats.networkTransportDelay
    <<" jitterBufferDelay:"<<stats.jitterBufferDelay<<" audioLossRate:"<<stats.audioLossRate<<" numChannels:"<<stats.numChannels<<" receivedSampleRate:"<<stats.receivedSampleRate
    <<" receivedBitrate:"<<stats.receivedBitrate<<" totalFrozenTime:"<<stats.totalFrozenTime<<" totalActiveTime:"<<stats.totalActiveTime<<" publishDuration:"<<stats.publishDuration
    //<<"qoeQuality:"<<stats.qoeQuality<<"qualityChangedReason:"<<stats.qualityChangedReason<<"mosValue:"<<stats.mosValue
    <<std::endl;
}

void CAgoraObject::onRtcStats(const RtcStats &stats)
{

}

void CAgoraObject::onVideoDeviceStateChanged(const char* deviceId, int deviceType, int deviceState)
{
    // if(deviceType == VIDEO_CAPTURE_DEVICE && m_videoDeviceManager){
    //     m_videoDeviceManager->release();
    //     m_videoDeviceManager = new AVideoDeviceManager(m_rtcEngine);
    //     string cameraid = getCurrentVideoDevice();
    //     if(cameraid == deviceId && (deviceState == MEDIA_DEVICE_STATE_UNPLUGGED || deviceState == MEDIA_DEVICE_STATE_DISABLED)){
    //         qSSMap videoDeviceList = getVideoDeviceList();
    //         if(videoDeviceList.size() > 0){
    //             (*m_videoDeviceManager)->setDevice(deviceId.toUtf8());
    //         }
    //     }
    // }
}

void CAgoraObject::onAudioDeviceStateChanged(const char* deviceId, int deviceType, int deviceState)
{
    // if(m_audioDeviceManager){
    //     m_audioDeviceManager->release();
    //     m_audioDeviceManager = new AAudioDeviceManager(m_rtcEngine);

    //     string audioId;


    //     if(deviceState == MEDIA_DEVICE_STATE_UNPLUGGED || deviceState == MEDIA_DEVICE_STATE_DISABLED){
    //         qSSMap audioDeviceList;
    //         if(deviceType == AUDIO_RECORDING_DEVICE){
    //             audioId = getCurrentRecordingDevice();
    //             audioDeviceList = getRecordingDeviceList();

    //             if(audioDeviceList.size() > 0 && audioId ==  deviceId){
    //                 (*m_audioDeviceManager)->setRecordingDevice(deviceId.toUtf8());
    //             }
    //         }
    //         else if(deviceType == AUDIO_PLAYOUT_DEVICE ){
    //             audioId = getCurrentPlaybackDevice();
    //             audioDeviceList = getPlayoutDeviceList();

    //             if(audioDeviceList.size() > 0 && audioId ==  deviceId){
    //                 (*m_audioDeviceManager)->setPlaybackDevice(deviceId.toUtf8());
    //             }
    //         }


    //     }
    // }
}

bool CAgoraObject::onCaptureVideoFrame(VideoFrame& videoFrame)
{
    if (m_videoObserver)
    {
        m_videoObserver(STREAM_VIDEO_CAPTURE, 0, &videoFrame, m_videoContext);
    }
	return true;
}

bool CAgoraObject::onRenderVideoFrame(unsigned int uid, VideoFrame& videoFrame)
{
    if (m_videoObserver)
    {
        //m_videoObserver(STREAM_VIDEO_RENDER, uid, &videoFrame, m_videoContext);
    }
	return true;
}

bool CAgoraObject::onRecordAudioFrame(AudioFrame& audioFrame)
{
    if(m_audioObserver)
    {
        m_audioObserver(STREAM_AUDIO_RECORD, 0, &audioFrame, m_audioContext);
    }
	return true;
}

bool CAgoraObject::onPlaybackAudioFrame(AudioFrame& audioFrame)
{
    if(m_audioObserver)
    {
        //m_audioObserver(STREAM_AUDIO_PLAYBACK, 0, &audioFrame, m_audioContext);
    }
	return true;
}

bool CAgoraObject::onMixedAudioFrame(AudioFrame& audioFrame)
{
    if(m_audioObserver)
    {
      //  m_audioObserver(STREAM_AUDIO_MIX, 0, &audioFrame, m_audioContext);
    }
	return true;
}

bool CAgoraObject::onPlaybackAudioFrameBeforeMixing(unsigned int uid, AudioFrame& audioFrame)
{
    if(m_audioObserver)
    {
        //m_audioObserver(STREAM_AUDIO_PLAYBACK_BEFORE_MIX, uid, &audioFrame, m_audioContext);
    }
	return true;
}

void CAgoraObject::registerAudioFrameObserver(StreamObserver cb,  void* userdata)
{
    agora::util::AutoPtr<agora::media::IMediaEngine> mediaEngine;
	mediaEngine.queryInterface(m_rtcEngine, agora::AGORA_IID_MEDIA_ENGINE);
	mediaEngine->registerAudioFrameObserver(this);
    m_audioObserver = cb;
    m_audioContext = userdata;
}

void CAgoraObject::registerVideoFrameObserver(StreamObserver cb,  void* userdata)
{
    agora::util::AutoPtr<agora::media::IMediaEngine> mediaEngine;
	mediaEngine.queryInterface(m_rtcEngine, agora::AGORA_IID_MEDIA_ENGINE);
	mediaEngine->registerVideoFrameObserver(this);
    m_videoObserver = cb;
    m_videoContext = userdata;
}