import sensor
import image
import lcd
import KPU as kpu
import utime as time

import socket
import ujson


from Corgi85 import corgi85


while(corgi85.wifi_check() == 0):
    print("WIFI Connecting")
    time.sleep(1)

token = "DtFrZ0QvOtrVn8rllWpT4EcstLC7xMAZyDbviBBMwBO"
corgi85.LINE_setToken(token)  #set line Token

#setup LCD screen
lcd.init()
#lcd.rotation(0)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)



clock = time.clock()

classes = ["นางสาวมิ้น", "นางสาวแหม่ม"]
#set model cnn
task = kpu.load(0x200000)

a = kpu.set_outputs(task, 0, 7, 7, 35)
anchor = (2.4654, 3.08, 3.3219, 3.86, 3.7231, 4.66, 4.2004, 5.40, 4.9471, 6.0257)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
timep = 0
while(True):

    clock.tick()

    img = sensor.snapshot()
    fps = 1000/(time.ticks_ms() - timep)
    timep = time.ticks_ms()

    objects = kpu.run_yolo2(task, img)

    if objects:
        for obj in objects:
            img.draw_rectangle(obj.rect(), color=(255, 0, 0), thickness=4)
            class_name = classes[obj.classid()]
            #img.draw_string(obj.x(), obj.y(), class_name, color=(0, 255, 0), scale=3)
            #img.draw_string(0, 200, "%.1fFPS" % fps, scale=2, color=(255, 0, 0))

            try:
                time_string = get_current_time()
            except Exception as e:
                time_string = "N/A"  # ถ้าเกิดข้อผิดพลาดในการดึงเวลา
            # ส่งภาพพร้อมกรอบและข้อความ
            corgi85.LINE_notifyPicture(img, '')
            #corgi85.LINE_notify('\n'+class_name +' เข้าเรียนที่'+time_string)


    #lcd.display(img)
kpu.deinit(task)

#if objects:
    #for obj in objects:
        #img.draw_rectangle(obj.rect(), color=(255, 0, 0), thickness=4)
        #class_name = classes[obj.classid()]
        ##img.draw_string(obj.x(), obj.y(), class_name, color=(0, 255, 0), scale=3)
        ## img.draw_string(0, 200, "%.1fFPS" % fps, scale=2, color=(255, 0, 0))
        ##corgi85.LINE_notifyPicture(img, class_name)

        ## เช็คว่าพบคลาสใหม่หรือไม่
        #if not detected_classes[class_name]:
            ## ส่งภาพพร้อมกรอบและข้อความ
            #corgi85.LINE_notifyPicture(img, class_name)
            ##time.sleep(3)
            ## อัพเดตสถานะของคลาสที่ตรวจจับได้
            #detected_classes[class_name] = True

        ## เช็คว่าพบทุกคลาสหรือไม่
        #if all(detected_classes.values()):
            #corgi85.LINE_notify("มาครบแล้ว")
            #break

##lcd.display(img)

## เช็คว่าพบทุกคลาสหรือไม่
#if all(detected_classes.values()):
    #break


