#base_camera.py
import picamera, threading, io,time
from _thread import get_ident
# 相机事件类
class CameraEvent(object):
        """一个类似事件的类，当一个新框架可用时，它向所有活跃的客户机发出信号."""
        def __init__(self):
                self.events = {}
        def wait(self):
                """从每个客户机的线程调用，等待下一个帧."""
                ident = get_ident()
                if ident not in self.events:
                        # 这是一个新的客户端在self中添加一个条目。事件指令有两个元素，一个线程事件()和时间戳
                        self.events[ident] = [threading.Event(), time.time()]
                # print(2)
                return self.events[ident][0].wait()
        def set(self):
                """当一个新的帧可用时由相机线程调用."""
                now = time.time()
                remove = None
                for ident, event in self.events.items():
                        if not event[0].isSet():
                                # 如果事件没设置,设置并更新最后一帧的时间戳为现在
                                event[0].set()
                                event[1] = now
                        else:
                                # 如果客户的活动已经设置好了，就意味着客户没有处理前一帧如果事件持续了超过5秒，那么假设客户已经离开并移除它了
                                if now - event[1] > 5:
                                        remove = ident
                if remove:
                        del self.events[remove]
        def clear(self):
                """在处理一个框架后从每个客户机线程调用."""
                # print(3)
                self.events[get_ident()][0].clear()
# 相机基础类
class BaseCamera(object):
        thread = None  # 从相机读取帧的后台线程
        frame = None  # 当前帧通过后台线程存储在这里
        last_access = 0  # 最后客户端访问摄像机的时间
        event = CameraEvent()
        def __init__(self):
                """启动后台摄像头线程，如果它还没有运行."""
                if BaseCamera.thread is None:
                        # 启动后台帧线程
                        BaseCamera.thread = threading.Thread(target=self._thread)
                        BaseCamera.thread.start()
                        while self.get_frame() is None: # 等到帧可用
                                time.sleep(0)
        def get_frame(self):
                """返回当前相机帧."""
                BaseCamera.last_access = time.time()
                BaseCamera.event.wait() # 等待来自摄像机线程的信号
                BaseCamera.event.clear()
                return BaseCamera.frame
        @staticmethod
        def frames():
                """"从相机的生成器返回帧."""
                raise RuntimeError('Must be implemented by subclasses.')
        @classmethod
        def _thread(cls):
                """相机的后台线程."""
                print('Starting camera thread.')
                frames_iterator = cls.frames()
                for frame in frames_iterator:
                        BaseCamera.frame = frame
                        BaseCamera.event.set()  # 向客户发送信号
                        # print(1)
                        time.sleep(0)
                        if time.time() - BaseCamera.last_access > 10:   # 如果没有任何请求10秒后停止线程
                                frames_iterator.close()
                                print('Stopping camera thread due to inactivity.')
                                break
                BaseCamera.thread = None
# 相机类继承基础相机类
class Camera(BaseCamera):
        @staticmethod
        def frames():
                with picamera.PiCamera() as camera:
                        # 让相机热热身
                        camera.resolution = (640,480)
                        time.sleep(2)
                        stream = io.BytesIO()
                        for foo in camera.capture_continuous(stream, 'jpeg',use_video_port=True):
                                # 返回当前帧
                                stream.seek(0)
                                yield stream.read()
                                # 为下一帧重新设置流
                                stream.seek(0)
                                stream.truncate()