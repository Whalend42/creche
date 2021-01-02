import sys
sys.path.append("../src/")

from creche.hardware.inhibitableSwitch import InhibitableSwitch
from creche.hardware.inhibitableSwitches import InhibitableSwitches
from creche.hardware.status import Status

size = 5
switches = InhibitableSwitches([InhibitableSwitch(status=Status.OFF, inhibited=False)]*size)

for i in range(size):
    assert switches.status(i) == Status.OFF, "1. Status initialization failed"
    assert switches.isInhibited(i) == False, "1. Inhibition initialization failed"
print("1. Successful status and inhibition initialization")

switches = switches.on(0)
switches = switches.on(2)
switches = switches.on(4)
for i in range(size):
    if i == 0 or i == 2 or i == 4:
        assert switches.status(i) == Status.ON, "2. Status not changed to ON"
    else:
        assert switches.status(i) == Status.OFF, "2. Status not kept to OFF"

    assert switches.isInhibited(i) == False, "2. Inhibition modified unexpectedly"
print("2. Successful status change and inhibition kept")

switches = switches.off(0)
switches = switches.off(3)
switches = switches.off(4)
for i in range(size):
    if i == 2:
        assert switches.status(i) == Status.ON, "3. Status unexpectedly changed to OFF"
    else:
        assert switches.status(i) == Status.OFF, "3. Status not kept or not changed to OFF"

    assert switches.isInhibited(i) == False, "3. Inhibition modified unexpectedly"
print("3. Successful status change and inhibition kept")

switches = switches.inhibit(0)
switches = switches.inhibit(2)
switches = switches.inhibit(4)
for i in range(size):
    if i == 2:
        assert switches.status(i) == Status.ON, "4. Status unexpectedly changed to OFF with Inhibition"
    else:
        assert switches.status(i) == Status.OFF, "4. Status unexpectedly changed to ON with Inhibition"

    if i == 0 or i == 2 or i == 4:
        assert switches.isInhibited(i) == True, "4. Inhibition not changed"
    else:
        assert switches.isInhibited(i) == False, "4. Inhibition not kept"
print("4. Successful inhibition changed and status kept")

switches = switches.on(0)
switches = switches.off(2)
switches = switches.on(3)
switches = switches.on(4)
for i in range(size):
    if i == 2 or i == 3:
        assert switches.status(i) == Status.ON, "5. Status unexpectedly changed to OFF while Inhibited"
    else:
        assert switches.status(i) == Status.OFF, "5. Status unexpectedly changed to ON with Inhibited"

    if i == 0 or i == 2 or i == 4:
        assert switches.isInhibited(i) == True, "5. Inhibition unexpectedly changed"
    else:
        assert switches.isInhibited(i) == False, "5. Inhibition unexpectedly changed"
print("5. Successfuly kept the status on inhibited switches and changed on not inhibited")

switches = switches.release(0)
switches = switches.release(3)
switches = switches.release(4)
for i in range(size):
    if i == 2 or i == 3:
        assert switches.status(i) == Status.ON, "6. Status unexpectedly changed to OFF with release"
    else:
        assert switches.status(i) == Status.OFF, "6. Status unexpectedly changed to ON with release"

    if i == 2:
        assert switches.isInhibited(i) == True, "6. release unexpectedly changed"
    else:
        assert switches.isInhibited(i) == False, "6. release not kept or changed"
print("6. Successful release and status kept")

switches = switches.forceOn(0)
switches = switches.forceOn(3)
for i in range(size):
    if i == 2 or i == 3 or i == 0:
        assert switches.status(i) == Status.ON, "7. Status not changed to ON"
    else:
        assert switches.status(i) == Status.OFF, "7. Status unexpectedly changed to ON"

    if i == 2 or i == 3 or i == 0:
        assert switches.isInhibited(i) == True, "7. Force ON didn't change the inhibition"
    else:
        assert switches.isInhibited(i) == False, "7. inhibition not kept"
print("7. Successful 'forceOn'")

switches = switches.off(1)
switches = switches.off(3)
switches = switches.on(4)
for i in range(size):
    if i == 2 or i == 3 or i == 0 or i == 4:
        assert switches.status(i) == Status.ON, "8. Status not changed to ON"
    else:
        assert switches.status(i) == Status.OFF, "8. Status unexpectedly changed to ON"

    if i == 2 or i == 3 or i == 0:
        assert switches.isInhibited(i) == True, "8. Force ON didn't change the inhibition"
    else:
        assert switches.isInhibited(i) == False, "8. inhibition not kept"
print("8. Successful, no effect of 'on'/'off' after 'forceOn'")

switches = switches.forceOff(0)
switches = switches.forceOff(3)
for i in range(size):
    if i == 2 or i == 4:
        assert switches.status(i) == Status.ON, "9. Status not changed to ON"
    else:
        assert switches.status(i) == Status.OFF, "9. Status unexpectedly changed to ON"

    if i == 2 or i == 3 or i == 0:
        assert switches.isInhibited(i) == True, "9. Force ON didn't change the inhibition"
    else:
        assert switches.isInhibited(i) == False, "9. inhibition not kept"
print("9. Successful 'forceOff'")

switches = switches.inhibitAll()
for i in range(size):
    if i == 2 or i == 4:
        assert switches.status(i) == Status.ON, "10. Status not changed to ON"
    else:
        assert switches.status(i) == Status.OFF, "10. Status unexpectedly changed to ON"

    assert switches.isInhibited(i) == True, "10. Force ON didn't change the inhibition"
print("10. Successful 'inhibitAll'")

switches = switches.releaseAll()
for i in range(size):
    if i == 2 or i == 4:
        assert switches.status(i) == Status.ON, "11. Status not changed to ON"
    else:
        assert switches.status(i) == Status.OFF, "11. Status unexpectedly changed to ON"

    assert switches.isInhibited(i) == False, "11. Force ON didn't change the inhibition"
print("11. Successful 'releaseAll'")

switches = switches.allOn()
for i in range(size):
    assert switches.status(i) == Status.ON, "11. Status not changed to ON"
    assert switches.isInhibited(i) == False, "11. Force ON didn't change the inhibition"
print("11. Successful 'allOn'")

switches = switches.allOff()
for i in range(size):
    assert switches.status(i) == Status.OFF, "12. Status not changed to ON"
    assert switches.isInhibited(i) == False, "12. Force ON didn't change the inhibition"
print("12. Successful 'allOff'")

switches = switches.forceAllOn()
for i in range(size):
    assert switches.status(i) == Status.ON, "13. Status not changed to ON"
    assert switches.isInhibited(i) == True, "13. Force ON didn't change the inhibition"
print("13. Successful 'forceAllOn'")

switches = switches.releaseAll()
switches = switches.forceAllOff()
for i in range(size):
    assert switches.status(i) == Status.OFF, "14. Status not changed to ON"
    assert switches.isInhibited(i) == True, "14. Force ON didn't change the inhibition"
print("14. Successful 'forceAllOff'")
