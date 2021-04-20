# ====== Legal notices
#
# Copyright (C) 2013 - 2020 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.qquick.org/license.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

import simpylc

class BassieStove(simpylc.Module):
    def __init__(self):
        simpylc.Module.__init__(self)

        self.page('BassieStove!')

        # ############# Constants #############
        self.group('Page constants', True)
        self.PAGE_LOCK = simpylc.Register()
        self.PAGE_ALARM = simpylc.Register()
        self.PAGE_MAIN = simpylc.Register()
        self.PAGE_SELECT_STOVE = simpylc.Register()
        self.PAGE_CHANGE_STOVE = simpylc.Register()
        self.PAGE_VIEW_TIMER = simpylc.Register()
        self.PAGE_CHANGE_TIMER = simpylc.Register()

        self.group('Lock constants')
        self.LOCK_COUNT = simpylc.Register()

        self.group('Stove constants')
        self.STOVE_COUNT = simpylc.Register()
        self.STOVE_TEMP_MAX = simpylc.Register()
        self.STOVE_TEMP_INC = simpylc.Register()

        self.group('Timer constants')
        self.TIMER_MAX = simpylc.Register()
        self.TIMER_INC = simpylc.Register()

        # ############# State #############
        self.group('Global state', True)
        self.randSeed = simpylc.Register()
        self.cycleCounter = simpylc.Register()

        self.group('Beeper state')
        self.beeperEnabled = simpylc.Marker()
        self.beeperFrequency = simpylc.Register()

        self.group('Page state')
        self.page = simpylc.Register()
        self.lockCounter = simpylc.Register()
        self.selectedLock = simpylc.Register()
        self.selectedStove = simpylc.Register(1)
        self.updateScreen = simpylc.Marker()
        self.updateScreenTimer = simpylc.Timer()

        self.group('Timer state')
        self.timerTime = simpylc.Register()
        self.timerTimer = simpylc.Timer()
        self.timerStarted = simpylc.Marker()
        self.timerFinished = simpylc.Marker()

        # ############# Locals #############
        self.group('Lock page locals', True)
        self.lock1ButtonTrigger = simpylc.Marker()
        self.lock2ButtonTrigger = simpylc.Marker()
        self.lock3ButtonTrigger = simpylc.Marker()

        self.group('Alarm page locals')
        self.alarmTimer = simpylc.Timer()
        self.newBeeperFrequency = simpylc.Register()

        self.group('Main page locals')
        self.changeButtonTrigger = simpylc.Marker()
        self.timerButtonTrigger = simpylc.Marker()
        self.lockButtonTrigger = simpylc.Marker()

        self.group('Select stove page locals')
        self.selectButtonTrigger = simpylc.Marker()
        self.newSelectedStove = simpylc.Register()
        self.leftButtonTrigger = simpylc.Marker()
        self.rightButtonTrigger = simpylc.Marker()

        self.group('Change stove page locals', True)
        self.backButtonTrigger = simpylc.Marker()
        self.newStove1Temperature = simpylc.Register()
        self.newStove2Temperature = simpylc.Register()
        self.newStove3Temperature = simpylc.Register()
        self.newStove4Temperature = simpylc.Register()
        self.downButtonTrigger = simpylc.Marker()
        self.upButtonTrigger = simpylc.Marker()

        self.group('View timer page locals')
        self.back2ButtonTrigger = simpylc.Marker()
        self.createStopButtonTrigger = simpylc.Marker()

        self.group('Change timer page locals')
        self.startButtonTrigger = simpylc.Marker()
        self.newTimerTime = simpylc.Register()
        self.down2ButtonTrigger = simpylc.Marker()
        self.up2ButtonTrigger = simpylc.Marker()

        # ############# Stoves #############
        self.group('Stoves', True)

        # Stove 1
        self.stove1Value = simpylc.Register()
        self.stove1Target = simpylc.Register()

        # Stove 2
        self.stove2Value = simpylc.Register()
        self.stove2Target = simpylc.Register()

        # Stove 3
        self.stove3Value = simpylc.Register()
        self.stove3Target = simpylc.Register()

        # Stove 4
        self.stove4Value = simpylc.Register()
        self.stove4Target = simpylc.Register()

        # ############# Buttons #############
        self.group('Buttons')

        # Left button
        self.leftButton = simpylc.Marker()
        self.leftButtonOneshot = simpylc.Oneshot()
        self.leftButtonHandled = simpylc.Marker()

        # Middle button
        self.middleButton = simpylc.Marker()
        self.middleButtonOneshot = simpylc.Oneshot()
        self.middleButtonHandled = simpylc.Marker()

        # Right button
        self.rightButton = simpylc.Marker()
        self.rightButtonOneshot = simpylc.Oneshot()
        self.rightButtonHandled = simpylc.Marker()

    def sweep(self):
        # ############# Stoves #############
        self.stove1Value.set((1 - simpylc.world.period) * self.stove1Value + simpylc.world.period * self.stove1Target)

        self.stove2Value.set((1 - simpylc.world.period) * self.stove2Value + simpylc.world.period * self.stove2Target)

        self.stove3Value.set((1 - simpylc.world.period) * self.stove3Value + simpylc.world.period * self.stove3Target)

        self.stove4Value.set((1 - simpylc.world.period) * self.stove4Value + simpylc.world.period * self.stove4Target)

        # ############# Buttons #############

        # Left button debounce
        self.leftButtonOneshot.trigger(self.leftButton)
        self.leftButtonHandled.mark(False)

        # Middle button debounce
        self.middleButtonOneshot.trigger(self.middleButton)
        self.middleButtonHandled.mark(False)

        # Right button debounce
        self.rightButtonOneshot.trigger(self.rightButton)
        self.rightButtonHandled.mark(False)

        # ############# Timer state #############

        self.timerTimer.reset(not self.timerStarted)
        self.timerFinished.mark(True, self.timerStarted and self.timerTimer >= self.timerTime)
        self.beeperEnabled.mark(True, self.timerFinished)
        self.beeperFrequency.set(440, self.timerFinished)

        # ############# Page state #############

        # Clear update screen
        self.updateScreen.mark(False)

        # Lock page
        self.selectedLock.set(((self.randSeed + self.cycleCounter) % 3) + 1, self.selectedLock == 0)

        # Lock page left button
        self.lock1ButtonTrigger.mark(self.page == self.PAGE_LOCK and self.leftButtonOneshot and not self.leftButtonHandled)

        self.page.set(self.PAGE_ALARM, self.lock1ButtonTrigger and self.selectedLock != 1)

        self.lockCounter.set(self.lockCounter + 1, self.lock1ButtonTrigger and self.selectedLock == 1)
        self.selectedLock.set(0, self.lock1ButtonTrigger and self.selectedLock == 1)

        self.leftButtonHandled.mark(True, self.lock1ButtonTrigger)

        # Lock page middle button
        self.lock2ButtonTrigger.mark(self.page == self.PAGE_LOCK and self.middleButtonOneshot and not self.middleButtonHandled)

        self.page.set(self.PAGE_ALARM, self.lock2ButtonTrigger and self.selectedLock != 2)

        self.lockCounter.set(self.lockCounter + 1, self.lock2ButtonTrigger and self.selectedLock == 2)
        self.selectedLock.set(0, self.lock2ButtonTrigger and self.selectedLock == 2)

        self.middleButtonHandled.mark(True, self.lock2ButtonTrigger)

        # Lock page right button
        self.lock3ButtonTrigger.mark(self.page == self.PAGE_LOCK and self.rightButtonOneshot and not self.rightButtonHandled)

        self.page.set(self.PAGE_ALARM, self.lock3ButtonTrigger and self.selectedLock != 3)

        self.lockCounter.set(self.lockCounter + 1, self.lock3ButtonTrigger and self.selectedLock == 3)
        self.selectedLock.set(0, self.lock3ButtonTrigger and self.selectedLock == 3)

        self.rightButtonHandled.mark(True, self.lock3ButtonTrigger)

        # Lock page counter
        self.selectedLock.set(((self.randSeed + self.cycleCounter) % 3) + 1, self.selectedLock == 0)
        self.page.set(self.PAGE_MAIN, self.lockCounter == self.LOCK_COUNT)
        self.lockCounter.set(0, self.lockCounter == self.LOCK_COUNT)

        # Alarm page
        self.alarmTimer.reset(self.alarmTimer >= 1)
        self.beeperEnabled.mark(True, self.page == self.PAGE_ALARM and self.cycleCounter > 0)
        self.newBeeperFrequency.set(880, self.beeperFrequency <= 440, 440)
        self.beeperFrequency.set(self.newBeeperFrequency, self.page == self.PAGE_ALARM and self.cycleCounter > 0 and self.alarmTimer < 0.02)

        # Main page
        self.changeButtonTrigger.mark(self.page == self.PAGE_MAIN and self.leftButtonOneshot and not self.leftButtonHandled)
        self.page.set(self.PAGE_SELECT_STOVE, self.changeButtonTrigger)
        self.leftButtonHandled.mark(True, self.changeButtonTrigger)

        self.timerButtonTrigger.mark(self.page == self.PAGE_MAIN and self.middleButtonOneshot and not self.middleButtonHandled)
        self.page.set(self.PAGE_VIEW_TIMER, self.timerButtonTrigger)
        self.middleButtonHandled.mark(True, self.timerButtonTrigger)

        self.lockButtonTrigger.mark(self.page == self.PAGE_MAIN and self.rightButtonOneshot and not self.rightButtonHandled)
        self.page.set(self.PAGE_LOCK, self.lockButtonTrigger)
        self.rightButtonHandled.mark(True, self.lockButtonTrigger)

        # Select stove page
        self.selectButtonTrigger.mark(self.page == self.PAGE_SELECT_STOVE and self.leftButtonOneshot and not self.leftButtonHandled)
        self.page.set(self.PAGE_CHANGE_STOVE, self.selectButtonTrigger)
        self.leftButtonHandled.mark(True, self.selectButtonTrigger)

        self.leftButtonTrigger.mark(self.page == self.PAGE_SELECT_STOVE and self.middleButtonOneshot and not self.middleButtonHandled)
        self.newSelectedStove.set(self.selectedStove - 1, self.selectedStove > 1, self.STOVE_COUNT)
        self.selectedStove.set(self.newSelectedStove, self.leftButtonTrigger)
        self.middleButtonHandled.mark(True, self.leftButtonTrigger)

        self.rightButtonTrigger.mark(self.page == self.PAGE_SELECT_STOVE and self.rightButtonOneshot and not self.rightButtonHandled)
        self.newSelectedStove.set(self.selectedStove + 1, self.selectedStove < self.STOVE_COUNT, 1)
        self.selectedStove.set(self.newSelectedStove, self.rightButtonTrigger)
        self.middleButtonHandled.mark(True, self.rightButtonTrigger)

        # Change stove page

        # Change stove page back button
        self.backButtonTrigger.mark(self.page == self.PAGE_CHANGE_STOVE and self.leftButtonOneshot and not self.leftButtonHandled)
        self.page.set(self.PAGE_MAIN, self.backButtonTrigger)
        self.leftButtonHandled.mark(True, self.backButtonTrigger)

        # Change stove page down button
        self.downButtonTrigger.mark(self.page == self.PAGE_CHANGE_STOVE and self.middleButtonOneshot and not self.middleButtonHandled)

        self.newStove1Temperature.set(self.stove1Target - self.STOVE_TEMP_INC, self.stove1Target > 0, 0)
        self.stove1Target.set(self.newStove1Temperature, self.downButtonTrigger and self.selectedStove == 1)

        self.newStove2Temperature.set(self.stove2Target - self.STOVE_TEMP_INC, self.stove2Target > 0, 0)
        self.stove2Target.set(self.newStove2Temperature, self.downButtonTrigger and self.selectedStove == 2)

        self.newStove3Temperature.set(self.stove3Target - self.STOVE_TEMP_INC, self.stove3Target > 0, 0)
        self.stove3Target.set(self.newStove3Temperature, self.downButtonTrigger and self.selectedStove == 3)

        self.newStove4Temperature.set(self.stove4Target - self.STOVE_TEMP_INC, self.stove4Target > 0, 0)
        self.stove4Target.set(self.newStove4Temperature, self.downButtonTrigger and self.selectedStove == 4)

        self.middleButtonHandled.mark(True, self.downButtonTrigger)

        # Change stove page up button
        self.upButtonTrigger.mark(self.page == self.PAGE_CHANGE_STOVE and self.rightButtonOneshot and not self.rightButtonHandled)

        self.newStove1Temperature.set(self.stove1Target + self.STOVE_TEMP_INC, self.stove1Target < self.STOVE_TEMP_MAX, self.STOVE_TEMP_MAX)
        self.stove1Target.set(self.newStove1Temperature, self.upButtonTrigger and self.selectedStove == 1)

        self.newStove2Temperature.set(self.stove2Target + self.STOVE_TEMP_INC, self.stove2Target < self.STOVE_TEMP_MAX, self.STOVE_TEMP_MAX)
        self.stove2Target.set(self.newStove2Temperature, self.upButtonTrigger and self.selectedStove == 2)

        self.newStove3Temperature.set(self.stove3Target + self.STOVE_TEMP_INC, self.stove3Target < self.STOVE_TEMP_MAX, self.STOVE_TEMP_MAX)
        self.stove3Target.set(self.newStove3Temperature, self.upButtonTrigger and self.selectedStove == 3)

        self.newStove4Temperature.set(self.stove4Target + self.STOVE_TEMP_INC, self.stove4Target < self.STOVE_TEMP_MAX, self.STOVE_TEMP_MAX)
        self.stove4Target.set(self.newStove4Temperature, self.upButtonTrigger and self.selectedStove == 4)

        self.rightButtonHandled.mark(True, self.upButtonTrigger)

        # View timer page
        self.back2ButtonTrigger.mark(self.page == self.PAGE_VIEW_TIMER and self.leftButtonOneshot and not self.leftButtonHandled)
        self.page.set(self.PAGE_MAIN, self.back2ButtonTrigger)
        self.leftButtonHandled.mark(True, self.back2ButtonTrigger)

        self.createStopButtonTrigger.mark(self.page == self.PAGE_VIEW_TIMER and self.rightButtonOneshot and not self.rightButtonHandled)
        self.page.set(self.PAGE_CHANGE_TIMER, self.createStopButtonTrigger and not self.timerStarted)
        self.timerFinished.mark(False, self.createStopButtonTrigger and self.timerStarted)
        self.beeperEnabled.mark(False, self.createStopButtonTrigger and self.timerStarted)
        self.timerStarted.mark(False, self.createStopButtonTrigger and self.timerStarted)
        self.rightButtonHandled.mark(True, self.createStopButtonTrigger)

        # Change timer page
        self.startButtonTrigger.mark(self.page == self.PAGE_CHANGE_TIMER and self.leftButtonOneshot and not self.leftButtonHandled)
        self.page.set(self.PAGE_VIEW_TIMER, self.startButtonTrigger)
        self.timerStarted.mark(True, self.startButtonTrigger)
        self.leftButtonHandled.mark(True, self.startButtonTrigger)

        self.down2ButtonTrigger.mark(self.page == self.PAGE_CHANGE_TIMER and self.middleButtonOneshot and not self.middleButtonHandled)
        self.newTimerTime.set(self.timerTime - self.TIMER_INC, self.timerTime > 0, 0)
        self.timerTime.set(self.newTimerTime, self.down2ButtonTrigger)
        self.middleButtonHandled.mark(True, self.down2ButtonTrigger)

        self.up2ButtonTrigger.mark(self.page == self.PAGE_CHANGE_TIMER and self.rightButtonOneshot and not self.rightButtonHandled)
        self.newTimerTime.set(self.timerTime + self.TIMER_INC, self.timerTime < self.TIMER_MAX, self.TIMER_MAX)
        self.timerTime.set(self.newTimerTime, self.up2ButtonTrigger)
        self.rightButtonHandled.mark(True, self.up2ButtonTrigger)

        # Trigger update screen when a button was handled
        self.updateScreenTimer.reset(self.page == self.PAGE_CHANGE_STOVE and self.updateScreenTimer >= 0.5)
        self.updateScreenTimer.reset((self.page == self.PAGE_VIEW_TIMER and self.timerStarted) and self.updateScreenTimer >= 1)
        self.updateScreen.mark(
            self.leftButtonHandled or self.middleButtonHandled or self.rightButtonHandled or
            (
                self.page == self.PAGE_CHANGE_STOVE or
                (self.page == self.PAGE_VIEW_TIMER and self.timerStarted)
            ) and self.updateScreenTimer < 0.02
        )
        self.cycleCounter.set(self.cycleCounter + 1)
