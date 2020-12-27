from util.print_override import spikeprint;print = spikeprint
import hub
from runtime import VirtualMachine
from runtime.extensions import SoundExtension
from util.scratch import pitch_to_freq
from util.sensors import get_sensor_value

async def stack_1(vm, stack):
    hub.sound.beep(0, 0)
    await vm.extensions["sound"].stop_all()
    vm.store.move_pair(("A", "B"))
    pair = vm.system.move.on_pair(*vm.store.move_pair())
    pair.stop(vm.store.move_stop())

async def stack_2(vm, stack):
    vm.system.sound.play("/extra_files/Target Acquired", freq=pitch_to_freq(vm.store.sound_pitch(), 12000, 16000, 20000))

def stack_condition(vm, stack):
    sensor_value = get_sensor_value("E", 0, -1, (61,))
    if sensor_value is None:
        sensor_value = -1
    return 9 == sensor_value

def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "OKZ2sufrqNP6O2oVnlY7")

    vm.extensions["sound"] = SoundExtension(rpc)

    vm.register_on_start("RLze!!4X?NkDxzH.e%7z", stack_1)
    vm.register_on_condition("o~I:dV{EhWkB2y2=g?dY", stack_2, stack_condition)

    return vm
