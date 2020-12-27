from util.print_override import spikeprint;print = spikeprint
import hub
from runtime import VirtualMachine
from util.rotation import rotate_hub_display_to_value
from util.scratch import clamp, compare, convert_animation_frame, number_color_to_rgb, percent_to_int, pitch_to_freq, to_number
from util.sensors import get_sensor_value, is_type

g_animation = ["0000000000567890000000000", "0000000000456980000000000", "0000000000349870000000000", "0000000000298760000000000", "0000000000987650000000000", "0000000000896540000000000", "0000000000789430000000000", "0000000000678920000000000"]
g_animation_1 = ["0090006960990990696000900", "0090006960990990696000900", "0090006960990990696000900", "0090006960990990696000900"]
g_animation_2 = ["0000000000999990000000000", "0000000000899980000000000", "0000000000789870000000000", "0000000000679760000000000", "0000000000569650000000000", "0000000000458540000000000", "0000000000148410000000000", "0000000700179710070000000", "0000000800189810080000000", "0000000700179710070000000", "0000000000109010000000000", "0000000000109010000000000", "0000000000108010000000000", "0000000000108010000000000", "0000000000107010000000000", "0000000000106010000000000", "0000000000105010000000000", "0000000000101010000000000", "0000000000000000000000000"]

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
    vm.store.move_speed(10)
    vm.store.motor_speed("D", 100)
    (acceleration, deceleration) = vm.store.motor_acceleration("D")
    vm.store.motor_last_status("D", await vm.system.motors.on_port("D").run_for_degrees_async(648, vm.store.motor_speed("D"), stall=vm.store.motor_stall("D"), stop=vm.store.motor_stop("D"), acceleration=acceleration, deceleration=deceleration))
    while True:
        vm.system.sound.play("/extra_files/Scanning", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
        port = getattr(hub.port, "F", None)
        if getattr(port, "device", None) and is_type("F", 62):
            port.device.mode(5, bytes("".join([chr(percent_to_int(round(clamp(to_number(p), 0, 100)), 87)) for p in "0 0 100 100".split()]), "utf-8"))
        pair = vm.system.move.on_pair(*vm.store.move_pair())
        speeds = pair.from_direction("counterclockwise", vm.store.move_speed())
        (acceleration_1, deceleration_1) = vm.store.move_acceleration()
        vm.store.move_last_status(await pair.move_differential_speed_async(round(clamp((6 / vm.store.move_calibration()) * 360, -3600000, 3600000)), speeds[0], speeds[1], stop=vm.store.move_stop(), acceleration=acceleration_1, deceleration=deceleration_1))
        vm.system.sound.play("/extra_files/Scanning", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
        port_1 = getattr(hub.port, "F", None)
        if getattr(port_1, "device", None) and is_type("F", 62):
            port_1.device.mode(5, bytes("".join([chr(percent_to_int(round(clamp(to_number(p), 0, 100)), 87)) for p in "100 100 0 0".split()]), "utf-8"))
        pair = vm.system.move.on_pair(*vm.store.move_pair())
        speeds = pair.from_direction("clockwise", vm.store.move_speed())
        (acceleration_2, deceleration_2) = vm.store.move_acceleration()
        vm.store.move_last_status(await pair.move_differential_speed_async(round(clamp((6 / vm.store.move_calibration()) * 360, -3600000, 3600000)), speeds[0], speeds[1], stop=vm.store.move_stop(), acceleration=acceleration_2, deceleration=deceleration_2))
        yield

async def stack_2(vm, stack):
    yield 5000
    while True:
        sensor_value = get_sensor_value("F", 0, 200, (62,))
        if sensor_value is None:
            sensor_value = 200
        if sensor_value < 40:
            break
        yield 0
    vm.stop_stacks(except_stack=stack)
    pair = vm.system.move.on_pair(*vm.store.move_pair())
    pair.stop(vm.store.move_stop())
    port_2 = getattr(hub.port, "F", None)
    if getattr(port_2, "device", None) and is_type("F", 62):
        port_2.device.mode(5, bytes("".join([chr(percent_to_int(round(clamp(to_number(p), 0, 100)), 87)) for p in "100 100 100 100".split()]), "utf-8"))
    global g_animation_1
    brightness_1 = vm.store.display_brightness()
    frames_1 = [hub.Image(convert_animation_frame(frame, brightness_1)) for frame in g_animation_1]
    vm.system.display.show(frames_1, clear=False, delay=500, loop=False, fade=5)
    await vm.system.sound.play_async("/extra_files/Target Acquired", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    (acceleration_3, deceleration_3) = vm.store.motor_acceleration("D")
    vm.store.motor_last_status("D", await vm.system.motors.on_port("D").run_for_degrees_async(1080, -vm.store.motor_speed("D"), stall=vm.store.motor_stall("D"), stop=vm.store.motor_stop("D"), acceleration=acceleration_3, deceleration=deceleration_3))
    vm.system.sound.play("/extra_files/Laser", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    (acceleration_4, deceleration_4) = vm.store.motor_acceleration("B")
    vm.store.motor_last_status("B", await vm.system.motors.on_port("B").run_for_time_async(400, vm.store.motor_speed("B"), stall=vm.store.motor_stall("B"), stop=vm.store.motor_stop("B"), acceleration=acceleration_4, deceleration=deceleration_4))
    vm.system.sound.play("/extra_files/Laser", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    (acceleration_5, deceleration_5) = vm.store.motor_acceleration("B")
    vm.store.motor_last_status("B", await vm.system.motors.on_port("B").run_for_degrees_async(130, -vm.store.motor_speed("B"), stall=vm.store.motor_stall("B"), stop=vm.store.motor_stop("B"), acceleration=acceleration_5, deceleration=deceleration_5))
    (acceleration_6, deceleration_6) = vm.store.motor_acceleration("B")
    vm.store.motor_last_status("B", await vm.system.motors.on_port("B").run_for_degrees_async(60, vm.store.motor_speed("B"), stall=vm.store.motor_stall("B"), stop=vm.store.motor_stop("B"), acceleration=acceleration_6, deceleration=deceleration_6))
    yield 1000
    (acceleration_7, deceleration_7) = vm.store.motor_acceleration("D")
    vm.store.motor_last_status("D", await vm.system.motors.on_port("D").run_for_degrees_async(540, vm.store.motor_speed("D"), stall=vm.store.motor_stall("D"), stop=vm.store.motor_stop("D"), acceleration=acceleration_7, deceleration=deceleration_7))
    global g_animation_2
    brightness_2 = vm.store.display_brightness()
    frames_2 = [hub.Image(convert_animation_frame(frame, brightness_2)) for frame in g_animation_2]
    vm.system.display.show(frames_2, clear=False, delay=167, loop=False, fade=2)
    await vm.system.sound.play_async("/extra_files/Shut Down", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    yield 2000
    vm.stop()

def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "2-CwN8F6-V98gSnfdc-F")

    vm.register_on_start("NYaD6kdKN_nRerwXrvme", stack_1)
    vm.register_on_start("F_sJt4gHXifv7K.f[D1w", stack_2)

    return vm
