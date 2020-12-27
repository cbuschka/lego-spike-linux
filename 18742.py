from util.print_override import spikeprint;print = spikeprint
import hub
from runtime import VirtualMachine
from util.rotation import rotate_hub_display_to_value
from util.scratch import clamp, compare, convert_animation_frame, number_color_to_rgb, pitch_to_freq
from util.sensors import get_sensor_value

g_animation = ["0000000000567890000000000", "0000000000456980000000000", "0000000000349870000000000", "0000000000298760000000000", "0000000000987650000000000", "0000000000896540000000000", "0000000000789430000000000", "0000000000678920000000000"]
g_animation_1 = ["0000000000999990000000000", "0000000000899980000000000", "0000000000789870000000000", "0000000000679760000000000", "0000000000569650000000000", "0000000000458540000000000", "0000000000148410000000000", "0000000700179710070000000", "0000000800189810080000000", "0000000700179710070000000", "0000000000109010000000000", "0000000000109010000000000", "0000000000108010000000000", "0000000000108010000000000", "0000000000107010000000000", "0000000000106010000000000", "0000000000105010000000000", "0000000000101010000000000", "0000000000000000000000000"]

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
    vm.store.move_pair(("C", "A"))
    vm.store.move_speed(80)
    pair = vm.system.move.on_pair(*vm.store.move_pair())
    speeds = pair.from_steering(50, vm.store.move_speed())
    (acceleration, deceleration) = vm.store.move_acceleration()
    vm.store.move_last_status(await pair.move_differential_speed_async(round(clamp((110 / vm.store.move_calibration()) * 360, -3600000, 3600000)), speeds[0], speeds[1], stop=vm.store.move_stop(), acceleration=acceleration, deceleration=deceleration))
    pair = vm.system.move.on_pair(*vm.store.move_pair())
    speeds = pair.from_steering(-50, vm.store.move_speed())
    (acceleration_1, deceleration_1) = vm.store.move_acceleration()
    vm.store.move_last_status(await pair.move_differential_speed_async(round(clamp((110 / vm.store.move_calibration()) * 360, -3600000, 3600000)), speeds[0], speeds[1], stop=vm.store.move_stop(), acceleration=acceleration_1, deceleration=deceleration_1))
    yield 1000
    global g_animation_1
    brightness_1 = vm.store.display_brightness()
    frames_1 = [hub.Image(convert_animation_frame(frame, brightness_1)) for frame in g_animation_1]
    vm.system.display.show(frames_1, clear=False, delay=167, loop=False, fade=2)
    await vm.system.sound.play_async("/extra_files/Shut Down", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    yield 2000
    vm.stop()

def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "S9JjABY0zrMIKqc-Dp9G")

    vm.register_on_start("h8EqnFZU5g4RaOBhKDaI", stack_1)

    return vm
