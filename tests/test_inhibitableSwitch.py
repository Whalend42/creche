import sys
sys.path.append("../src/")

from creche.hardware.inhibitableSwitch import InhibitableSwitch
from creche.hardware.status import Status

switch = InhibitableSwitch(status=Status.OFF, inhibited=False)
assert switch.status() == Status.OFF, "Status initialization failed"
print("Successful status initialization")
assert switch.isInhibited() == False, "Inhibition initialization failed"
print("Successful inhibition initialization")

switch = switch.on()
assert switch.status() == Status.ON, "Status change to ON failed"
print("Successful status change to ON")
assert switch.isInhibited() == False, "Inhibition impacted by status change"
print("Successfully kept inhibition")

switch = switch.off()
assert switch.status() == Status.OFF, "Status change to OFF failed"
print("Successful status change to OFF")
assert switch.isInhibited() == False, "Inhibition impacted by status change"
print("Successfully kept inhibition")

switch = switch.inhibit()
assert switch.status() == Status.OFF, "Status has changed over inhibition"
print("Successful kept status over inhibition")
assert switch.isInhibited() == True, "Inhibition failed"
print("Successfully changed inhibition")

switch = switch.on()
assert switch.status() == Status.OFF, "Status change while inhibited"
print("Successful status kept")
assert switch.isInhibited() == True, "Status change impacted inhibition state"
print("Successfully kept inhibition")

switch = switch.release()
assert switch.status() == Status.OFF, "Status has changed over release"
print("Successful kept status over release")
assert switch.isInhibited() == False, "release failed"
print("Successfully changed inhibition")

switch = switch.on()
assert switch.status() == Status.ON, "Status did not change while not inhibited"
print("Successful status change")
assert switch.isInhibited() == False, "Status change impacted inhibition state"
print("Successfully kept inhibition")

switch = switch.forceOn()
assert switch.status() == Status.ON, "Forced status change to ON failed"
print("Successful force status change to ON")
assert switch.isInhibited() == True, "Force change of status did not impact inhibition"
print("Successfully changed inhibition")

switch = switch.release()
assert switch.status() == Status.ON, "Status has changed over release"
print("Successful kept status over release")
assert switch.isInhibited() == False, "release failed"
print("Successfully changed inhibition")

switch = switch.forceOff()
assert switch.status() == Status.OFF, "Forced status change to OFF failed"
print("Successful force status change to OFF")
assert switch.isInhibited() == True, "Force change of status did not impact inhibition"
print("Successfully changed inhibition")
