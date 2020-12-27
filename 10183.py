from util.print_override import spikeprint;print = spikeprint
import hub
import math
from runtime import Stack, VirtualMachine
from util.rotation import rotate_hub_display_to_value
from util.scratch import clamp, compare, convert_animation_frame, number_color_to_rgb, pitch_to_freq, to_number
from util.sensors import get_sensor_value

g_animation = ["1111118111177176661655555", "1910018108771776616655555", "1110918108771776616655555", "1911118181771716666155555", "1119118181177716666655555", "1191118818177771666655555", "1191111818177776666655555", "9111181181717716666655555", "1119181181711716166155555", "1111111181711716166655555", "1111111181717776166655555", "1191111818177176666655555", "1191911818117171166615555", "1911118181171776666655555"]

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
    hub.led(*number_color_to_rgb(0))
    rotate_hub_display_to_value("2")
    global g_animation
    brightness = vm.store.display_brightness()
    frames = [hub.Image(convert_animation_frame(frame, brightness)) for frame in g_animation]
    vm.system.display.show(frames, clear=False, delay=200, loop=True, fade=1)
    await bigBotCalibrate(vm)
    vm.store.move_pair(("C", "A"))
    vm.store.move_speed(80)
    while True:
        def cond():
            sensor_value = get_sensor_value("E", 0, -1, (61,))
            if sensor_value is None:
                sensor_value = -1
            return compare(sensor_value, "1") > 0
        while not cond():
            pair = vm.system.move.on_pair(*vm.store.move_pair())
            powers = pair.from_steering(0, round(clamp(to_number(math.sin(((vm.get_time() / 1000) * 360) * 0.017453292519943295)) * 35, -100, 100)))
            pair.start_at_powers(powers[0], -powers[1])
            yield
        sensor_value_1 = get_sensor_value("E", 0, -1, (61,))
        if sensor_value_1 is None:
            sensor_value_1 = -1
        stacks = vm.broadcast(str(sensor_value_1))
        while any([s.is_active() for s in stacks]):
            yield
        hub.led(*number_color_to_rgb(0))
        yield

async def stack_2(vm, stack):
    hub.led(*number_color_to_rgb(3))
    vm.system.sound.play("/extra_files/Whirl", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    pair = vm.system.move.on_pair(*vm.store.move_pair())
    speeds = pair.from_direction("counterclockwise", vm.store.move_speed())
    (acceleration, deceleration) = vm.store.move_acceleration()
    vm.store.move_last_status(await pair.move_differential_speed_async(round(clamp((35 / vm.store.move_calibration()) * 360, -3600000, 3600000)), speeds[0], speeds[1], stop=vm.store.move_stop(), acceleration=acceleration, deceleration=deceleration))

async def stack_3(vm, stack):
    hub.led(*number_color_to_rgb(5))
    vm.system.sound.play("/extra_files/Scanning", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    pair = vm.system.move.on_pair(*vm.store.move_pair())
    pair.stop(vm.store.move_stop())
    for _ in range(6):
        (acceleration_1, deceleration_1) = vm.store.motor_acceleration("A")
        vm.store.motor_last_status("A", await vm.system.motors.on_port("A").run_for_degrees_async(90, -vm.store.motor_speed("A"), stall=vm.store.motor_stall("A"), stop=vm.store.motor_stop("A"), acceleration=acceleration_1, deceleration=deceleration_1))
        (acceleration_2, deceleration_2) = vm.store.motor_acceleration("C")
        vm.store.motor_last_status("C", await vm.system.motors.on_port("C").run_for_degrees_async(90, vm.store.motor_speed("C"), stall=vm.store.motor_stall("C"), stop=vm.store.motor_stop("C"), acceleration=acceleration_2, deceleration=deceleration_2))
        yield

async def stack_4(vm, stack):
    hub.led(*number_color_to_rgb(7))
    vm.system.sound.play("/extra_files/Laugh", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    for _ in range(3):
        pair = vm.system.move.on_pair(*vm.store.move_pair())
        speeds = pair.from_direction("counterclockwise", vm.store.move_speed())
        (acceleration_3, deceleration_3) = vm.store.move_acceleration()
        vm.store.move_last_status(await pair.move_differential_speed_async(round(clamp((6 / vm.store.move_calibration()) * 360, -3600000, 3600000)), speeds[0], speeds[1], stop=vm.store.move_stop(), acceleration=acceleration_3, deceleration=deceleration_3))
        pair = vm.system.move.on_pair(*vm.store.move_pair())
        speeds = pair.from_direction("clockwise", vm.store.move_speed())
        (acceleration_4, deceleration_4) = vm.store.move_acceleration()
        vm.store.move_last_status(await pair.move_differential_speed_async(round(clamp((6 / vm.store.move_calibration()) * 360, -3600000, 3600000)), speeds[0], speeds[1], stop=vm.store.move_stop(), acceleration=acceleration_4, deceleration=deceleration_4))
        yield

async def stack_5(vm, stack):
    hub.led(*number_color_to_rgb(9))
    vm.system.sound.play("/extra_files/Affirmative", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))
    pair = vm.system.move.on_pair(*vm.store.move_pair())
    pair.stop(vm.store.move_stop())
    (acceleration_5, deceleration_5) = vm.store.motor_acceleration("D")
    vm.store.motor_last_status("D", await vm.system.motors.on_port("D").run_to_relative_position_async(600, 100, stall=vm.store.motor_stall("D"), stop=vm.store.motor_stop("D"), acceleration=acceleration_5, deceleration=deceleration_5))
    (acceleration_6, deceleration_6) = vm.store.motor_acceleration("D")
    vm.store.motor_last_status("D", await vm.system.motors.on_port("D").run_to_relative_position_async(-600, 100, stall=vm.store.motor_stall("D"), stop=vm.store.motor_stop("D"), acceleration=acceleration_6, deceleration=deceleration_6))
    (acceleration_7, deceleration_7) = vm.store.motor_acceleration("D")
    vm.store.motor_last_status("D", await vm.system.motors.on_port("D").run_to_relative_position_async(0, 100, stall=vm.store.motor_stall("D"), stop=vm.store.motor_stop("D"), acceleration=acceleration_7, deceleration=deceleration_7))

def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "UgnW11Q73RQU7xAyD_hz")

    vm.register_on_start("IG17-rCl5Mgs4J8Me7fA", stack_1)
    vm.register_on_broadcast("FlT}67PKWTT6NQ`;k?2v", stack_2, "3")
    vm.register_on_broadcast("Hk35_SLoXnj%/FB9@86l", stack_3, "5")
    vm.register_on_broadcast("qiPC^wg?d*$bEwT2{$jb", stack_4, "7")
    vm.register_on_broadcast("!xnO:KWc^%~(TcE6lMrs", stack_5, "9")

    return vm
