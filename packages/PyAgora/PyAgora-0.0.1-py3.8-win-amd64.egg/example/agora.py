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



def run(channel="fortest", vW=1280, vH=720, fps=10, kbps=1000, viewW=2, viewH=2, 
        robot=False, disableVideo=False, disableAudio=False, baselineVideo=False,disableFec=False,
        disable3A=False,logoff=True, enableDual=False,
        audioSpecifyCodec=None,robotAudioSamplrate=48000,robotAudioChans=1, uid=None,appId=None,h265Mode=-1,params=[]):
    aOb = None
    vOb = None
    vCapTask = None
    vQueue = None
    aCapTask = None
    aQueue = None
    try:
        if appId is None:
            appId='aab8b8f5a8cd4469a63042fcfafe7063'
            #print("error: appId is none, please input appId")
            #return
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
        if viewW != 0 and viewH != 0:
            relative_height = 1 / float(viewH)
            relative_width = 1 / float(viewW)

            for h in range(viewH):
                for w in range(viewW):
                    display_frame = tkinter.Frame(window, bg='')
                    relative_y = h * relative_height
                    relative_x = w * relative_width
                    display_frame.place(relx = relative_x, rely = relative_y,
                            anchor = tkinter.NW, relwidth = relative_width, relheight = relative_height)
                    frame_id = display_frame.winfo_id()
                    agora.addView(frame_id)
        
        agora.initialize(appId)

        if logoff == True:
            agora.logOff()

        if disableAudio == True:
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
        if enableCustomCapture == True:
            
            aOb = audioObserver()
            agora.registerAudioObserver(aOb[0])
            
            #parameter = json.dumps({"che.video.local.camera_index": 1024})
            #agora.setParameters(parameter)
            #vOb = videoObserver()
            #agora.registerVideoObserver(vOb[0])
            
            try:
                agora.setExternalVideoSource(True, False)
                vQueue = queue.Queue()
                vCapTask = threading.Thread(target=customVCapture, args=(vQueue, agora, vW, vH))
                vCapTask.start()  
            except Exception as e:
                print(e)
        for param in params:
            print(param)
            agora.setParameters(param)    
        #agora.enumerateRecordingDevices()
        #agora.enumerateVideoDevices()

        #agora.setRecordingDevice(ctypes.c_char_p(bytes("{0.0.1.00000000}.{5c5eacc2-a2df-47db-9e25-5e6da81b5ae8}", 'utf-8')))
        #agora.setVideoDevice(ctypes.c_char_p(bytes("YY开播", 'utf-8')))

        agora.setChannelProfile(1)

        agora.setClientRole(1)

        agora.setVideoProfile(vW, vH, fps, kbps)
        
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

        if h265Mode != -1:    
            parameter = json.dumps({"che.video.h265_mode": h265Mode})
            agora.setParameters(parameter)

        agora.joinChannel("", channel, uid)
        def on_close():
            window.destroy()
        window.protocol("WM_DELETE_WINDOW", on_close)
        window.mainloop()

    except Exception as e:
        print(e)
    finally:
        if vCapTask is not None:
            vQueue.put("done")
            vCapTask.join()
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
                if len(data) <= 0:
                    wf.rewind()
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

def customVCapture(queue, agora, w, h):
    cap = cv2.VideoCapture(customVideoSrc)
    rate = cap.get(cv2.CAP_PROP_FPS)
    delay = (int)(1000/rate)-10
    frame_counter = 0
    while True:
        if queue.empty() == False:
            cmd = queue.get()
            if cmd == 'done':
                break
        start = time.time()
        ret, frame = cap.read()
        if ret != True:
            break

        frame_counter += 1
        if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            frame_counter = 0 #Or whatever as long as it is the same as next line
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            #print("rewind max {}".format(frame_counter))
#        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))       
#        print("frame_counter: {}".format(frame_counter))
        frame = cv2.resize(frame, (w, h))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)  
        #cv2.imshow("test", frame)
        agora.pushVideoFrame(frame.tobytes(), w, h, 0, np.int64(round(time.time()*1000)))
        used_ms = int((time.time() - start)*1000)
        if cv2.waitKey(max(delay-used_ms, 1)):
    	    pass

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
            diff = (now - last_time)*1.12
            #print("diff {} delay {}".format(diff, delay))
            if diff < delay and frame is not None:#higher fps than source file
                last_time = now
                return (frame[:height].tobytes(), frame[height:int(height+height/4)].tobytes(), frame[int(height+height/4):].tobytes())
            f_num =  round(diff / delay)
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
    run(robot=False, fps=30, kbps=1720, viewH=3, viewW=3)
