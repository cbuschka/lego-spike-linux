from util.print_override import spikeprint;print = spikeprint
import hub
from runtime import VirtualMachine
from util.rotation import rotate_hub_display_to_value
from util.scratch import clamp, compare, convert_animation_frame, number_color_to_rgb, percent_to_int, pitch_to_freq, to_number
from util.sensors import get_sensor_value, is_type

g_animation = ["0000000000567890000000000", "0000000000456980000000000", "0000000000349870000000000", "0000000000298760000000000", "0000000000987650000000000", "0000000000896540000000000", "0000000000789430000000000", "0000000000678920000000000"]

async def bigBotCalibrate(vm):
    vm.reset_time()
    vm.system.motors.on_port("D").pwm(100, stall=vm.store.motor_stall("D"))
    while True:
        if ((1 <= get_sensor_value("D", 1, 0, (49, 48, 76, 75)) <= 50) and (compare(vm.get_time() / 1000, 0.3) > 0)) or (compare(vm.get_time() / 1000, "3") > 0):
            break
        yield 0
    vm.system.motors.on_port("D").stop(vm.store.motor_stop("D"))
    yield 200
    hub.motion.reset_yaw()
    vm.system.motors.on_port("D").run_at_speed(-50, stall=vm.store.motor_stall("D"))
    vm.reset_time()
    while True:
        values = get_sensor_value("position", 0, 0, ())
        if (compare(values[0], -42) < 0) or (compare(vm.get_time() / 1000, 2) > 0):
            break
        yield 0
    vm.system.motors.on_port("D").stop(vm.store.motor_stop("D"))
    yield 200
    vm.system.motors.on_port("D").preset(0)

async def stack_1(vm, stack):
    hub.led(*number_color_to_rgb(9))
    rotate_hub_display_to_value("2")
    global g_animation
    brightness = vm.store.display_brightness()
    frames = [hub.Image(convert_animation_frame(frame, brightness)) for frame in g_animation]
    vm.system.display.show(frames, clear=False, delay=200, loop=True, fade=2)
    await bigBotCalibrate(vm)
    (acceleration, deceleration) = vm.store.motor_acceleration("D")
    vm.store.motor_last_status("D", await vm.system.motors.on_port("D").run_for_degrees_async(648, vm.store.motor_speed("D"), stall=vm.store.motor_stall("D"), stop=vm.store.motor_stop("D"), acceleration=acceleration, deceleration=deceleration))
    port = getattr(hub.port, "F", None)
    if getattr(port, "device", None) and is_type("F", 62):
        port.device.mode(5, bytes("".join([chr(percent_to_int(round(clamp(to_number(p), 0, 100)), 87)) for p in "100 100 100 100".split()]), "utf-8"))
    while True:
        sensor_value = get_sensor_value("F", 0, 200, (62,))
        if sensor_value is None:
            sensor_value = 200
        if sensor_value < 10:
            break
        yield 0
    await vm.system.sound.play_async("/extra_files/Target Acquired", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    (acceleration_1, deceleration_1) = vm.store.motor_acceleration("D")
    vm.store.motor_last_status("D", await vm.system.motors.on_port("D").run_for_degrees_async(648, -vm.store.motor_speed("D"), stall=vm.store.motor_stall("D"), stop=vm.store.motor_stop("D"), acceleration=acceleration_1, deceleration=deceleration_1))

def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "08hMNG-dP4WbJT8ulqfx")

    vm.register_on_start("O4a7qSvKDbzgtn35t9pb", stack_1)

    return vm
