import os
import tkinter
import json
import sys
import random
import numpy as np
import threading, queue
import cv2
import wave
import audioop
import time
import math
import pyagora as agora


customVideoSrc = "..\\data\\wudao.mp4"
customAudioSrc = "..\\data\\wudao-2-48.wav"

loopback = False
current_dir = os.path.abspath(os.path.dirname(__file__))
customVideoSrc = os.path.join(current_dir, customVideoSrc)
customAudioSrc = os.path.join(current_dir, customAudioSrc)

vCapTask = None
vQueue = None

aCapTask = None
aQueue = None

def run(channel_name="fortest", v_w=1280, v_h=720, view_w=2, view_h=2, kbps=1000, fps=15, 
        robot=False, disableVideo=False, disableAudio=False, baselineVideo=False,disableFec=False,
        disable3A=False,logoff=False, enableDual=False,
        audioSpecifyCodec=None,robot_audio_samplrate=48000,robot_audio_chans=1, uid=None,app_id=None,h265_mode=-1,params=[]):
    try:
        if app_id is None:
            app_id = "aab8b8f5a8cd4469a63042fcfafe7063"
        if uid is None:
            uid = random.randint(0,1000)
        enableCustomCapture = False
        if robot == True:
            enableCustomCapture = True

        if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
            os.add_dll_directory(current_dir)

        window = tkinter.Tk()
        window.title("agora")
        window.geometry('1280x720')
        if view_w != 0 and view_h != 0:
            relative_height = 1 / float(view_h)
            relative_width = 1 / float(view_w)

            for h in range(view_h):
                for w in range(view_w):
                    display_frame = tkinter.Frame(window, bg='')
                    relative_y = h * relative_height
                    relative_x = w * relative_width
                    display_frame.place(relx = relative_x, rely = relative_y,
                            anchor = tkinter.NW, relwidth = relative_width, relheight = relative_height)
                    frame_id = display_frame.winfo_id()
                    agora.addView(frame_id)
        if logoff == True:
            agora.logoff()
        agora.initialize(app_id)

        agora.enableAudio(not disableAudio)
        
        agora.enableVideo(not disableVideo)

        agora.enableDualStreamMode(enableDual)

        if baselineVideo == True:
            #100:high， 66:baseline
            parameter = '{"che.video.h264Profile" : 66}'
            agora.setParameters(parameter)

        #agora.setAudioProfile(profile, scenario)
        if robot == True:
            agora.muteAllRemoteVideoStreams(True)
            agora.muteAllRemoteAudioStreams(True)
            #agora.stopPreview()
        aOb = None
        vOb = None
        if enableCustomCapture == True:
            parameter = json.dumps({"che.video.local.camera_index": 1024})
            agora.setParameters(parameter)
            aOb = audioObserver()
            vOb = videoObserver()
            agora.registerAudioObserver(aOb[0])
            agora.registerVideoObserver(vOb[0])

        for param in params:
            agora.setParameters(param)    
        #agora.enumerateRecordingDevices()
        #agora.enumerateVideoDevices()

        #agora.setRecordingDevice(ctypes.c_char_p(bytes("{0.0.1.00000000}.{5c5eacc2-a2df-47db-9e25-5e6da81b5ae8}", 'utf-8')))
        #agora.setVideoDevice(ctypes.c_char_p(bytes("YY开播", 'utf-8')))

        agora.setChannelProfile(1)

        agora.setClientRole(1)

        agora.setVideoProfile(v_w, v_h, fps, kbps)
        
        if disable3A == True:
            parameter = '{"che.audio.bypass.apm" : true}'
            agora.setParameters(parameter)

        if disableFec == True:
            parameter = '{"che.video.fecMethod", 0}'
            agora.setParameters(parameter)

            parameter = '{"che.audio.uplink.fec",false}'
            agora.setParameters(parameter)

        if audioSpecifyCodec is not None:    
            parameter = json.dumps({"che.audio.specify.codec": audioSpecifyCodec})
            agora.setParameters(parameter)

        if h265_mode != -1:    
            parameter = json.dumps({"che.video.h265_mode": h265_mode})
            agora.setParameters(parameter)

        agora.joinChannel("", channel_name, uid)
        def on_close():
            window.destroy()
        window.protocol("WM_DELETE_WINDOW", on_close)
        window.mainloop()

    except Exception as e:
        print(e)
    finally:
        if aOb is not None:
            aOb[1]()
        if vOb is not None:
            vOb[1]()
        agora.leaveChannel()
        agora.terminate()


def audioObserver():
    wf = wave.open(customAudioSrc, 'rb')
    CHUNK = 9600
    buffer = bytes()
    cap_cur = 0
    state = None
    '''
    wf1 = wave.open('./1.wav', 'wb')
    wf1.setnchannels(1)
    wf1.setsampwidth(2)
    wf1.setframerate(48000)
    '''
    def audioFrameObserver(streamtype, uid, samples, channels, samplesPerSec, data):
        if streamtype == agora.paStreamAudioRecord:
            nonlocal cap_cur
            nonlocal buffer
            nonlocal state
            width = 2   
            inchannels = 2
            insamplerate = 48000
            data_len = samples*channels*width
            out = None
            #print('cap_cur {} channels {} samples {} buffer len {}'.format(cap_cur, channels, samples, len(buffer)))
            if cap_cur + data_len > len(buffer):
                data = wf.readframes(CHUNK)
                converted, state = audioop.ratecv(data, width, inchannels, insamplerate, samplesPerSec, state)
                if channels == 1:
                    converted = audioop.tomono(converted, 2, 1, 0)
                out = buffer[cap_cur:] + converted[:data_len-len(buffer)+cap_cur]
                cap_cur = cap_cur + data_len - len(buffer)
                buffer = converted
                #wf1.writeframes(converted)
            else:
                out = buffer[cap_cur:cap_cur+data_len]
            cap_cur = cap_cur + data_len
            #wf1.writeframes(out)
            return (out,)
        return (data, )
    def close():
        wf.close()
    return audioFrameObserver,close

def videoObserver():
    cap = cv2.VideoCapture(customVideoSrc)
    rate = cap.get(cv2.CAP_PROP_FPS)
    delay = 1/rate
    cap_frame_counter = 0
    frame = None
    last_time = time.time()
    def videoFrameObserver(streamtype, uid, width, height, yBuffer, uBuffer, vBuffer):
        if streamtype == agora.paStreamVideoCap:
            nonlocal cap_frame_counter
            nonlocal frame
            nonlocal last_time
            now = time.time()
            if now - last_time < delay and frame is not None:#higher fps than source file
                last_time = now
                return (frame[:height].tobytes(), frame[height:int(height+height/4)].tobytes(), frame[int(height+height/4):].tobytes())
            f_num =  round((now - last_time) / delay)
            #print(f_num)
            for i in range(f_num):#lower fps than source file
                ret, frame = cap.read()
                if ret != True:
                    return (np.zeros(width*height).tobytes(),np.zeros(width*height//4).tobytes(),np.zeros(width*height//4).tobytes())
                cap_frame_counter += 1
                if cap_frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    cap_frame_counter = 0 #Or whatever as long as it is the same as next line
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)   
            last_time = now      
            frame = cv2.resize(frame, (width, height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420) 
            return (frame[:height].tobytes(), frame[height:int(height+height/4)].tobytes(), frame[int(height+height/4):].tobytes())
        return (yBuffer, uBuffer, vBuffer)
    def close():
        cap.release()
        cv2.destroyAllWindows()
    return videoFrameObserver,close

if __name__ ==  '__main__':
    run(robot=False)
