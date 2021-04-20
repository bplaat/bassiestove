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

        # ############# State #############
        self.group('Global state', True)
        self.randSeed = simpylc.Register()
        self.cycleCounter = simpylc.Register()

        self.group('Page state')
        self.page = simpylc.Register()
        self.lockCounter = simpylc.Register()
        self.selectedLock = simpylc.Register()
        self.selectedStove = simpylc.Register(1)
        self.updateScreen = simpylc.Marker()

        self.group('Timer state')
        self.timerTime = simpylc.Register()
        self.timerTimer = simpylc.Timer()
        self.timerRunning = simpylc.Marker()

        # ############# Locals #############
        self.group('Lock page locals')
        self.lock1ButtonTrigger = simpylc.Marker()
        self.lock2ButtonTrigger = simpylc.Marker()
        self.lock3ButtonTrigger = simpylc.Marker()

        self.group('Main page locals', True)
        self.changeButtonTrigger = simpylc.Marker()
        self.timerButtonTrigger = simpylc.Marker()
        self.lockButtonTrigger = simpylc.Marker()

        self.group('Select stove page locals')
        self.selectButtonTrigger = simpylc.Marker()
        self.newSelectedStove = simpylc.Register()
        self.leftButtonTrigger = simpylc.Marker()
        self.rightButtonTrigger = simpylc.Marker()

        self.group('Change stove page locals')
        self.backButtonTrigger = simpylc.Marker()
        self.newStove1Temperature = simpylc.Register()
        self.newStove2Temperature = simpylc.Register()
        self.newStove3Temperature = simpylc.Register()
        self.newStove4Temperature = simpylc.Register()
        self.downButtonTrigger = simpylc.Marker()
        self.upButtonTrigger = simpylc.Marker()

        self.group('View timer page locals')
        self.back2ButtonTrigger = simpylc.Marker()
        self.change2ButtonTrigger = simpylc.Marker()
        self.stopButtonTrigger = simpylc.Marker()

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

        # ############# State #############

        # Clear update screen
        self.updateScreen.mark(False)

        # Lock page
        self.selectedLock.set(((self.randSeed + self.cycleCounter) % 3) + 1, self.selectedLock == 0)

        self.lock1ButtonTrigger.mark(self.page == self.PAGE_LOCK and self.selectedLock == 1 and self.leftButtonOneshot and not self.leftButtonHandled)
        self.lockCounter.set(self.lockCounter + 1, self.lock1ButtonTrigger)
        self.selectedLock.set(0, self.lock1ButtonTrigger)
        self.leftButtonHandled.mark(self.lock1ButtonTrigger, self.lock1ButtonTrigger)

        self.lock2ButtonTrigger.mark(self.page == self.PAGE_LOCK and self.selectedLock == 2 and self.middleButtonOneshot and not self.middleButtonHandled)
        self.lockCounter.set(self.lockCounter + 1, self.lock2ButtonTrigger)
        self.selectedLock.set(0, self.lock2ButtonTrigger)
        self.middleButtonHandled.mark(self.lock2ButtonTrigger, self.lock2ButtonTrigger)

        self.lock3ButtonTrigger.mark(self.page == self.PAGE_LOCK and self.selectedLock == 3 and self.rightButtonOneshot and not self.rightButtonHandled)
        self.lockCounter.set(self.lockCounter + 1, self.lock3ButtonTrigger)
        self.selectedLock.set(0, self.lock3ButtonTrigger)
        self.rightButtonHandled.mark(self.lock3ButtonTrigger, self.lock3ButtonTrigger)

        self.selectedLock.set(((self.randSeed + self.cycleCounter) % 3) + 1, self.selectedLock == 0)

        self.page.set(self.PAGE_MAIN, self.lockCounter == self.LOCK_COUNT)
        self.lockCounter.set(0, self.lockCounter == self.LOCK_COUNT)

        # Main page
        self.changeButtonTrigger.mark(self.page == self.PAGE_MAIN and self.leftButtonOneshot and not self.leftButtonHandled)
        self.page.set(self.PAGE_SELECT_STOVE, self.changeButtonTrigger)
        self.leftButtonHandled.mark(self.changeButtonTrigger, self.changeButtonTrigger)

        self.timerButtonTrigger.mark(self.page == self.PAGE_MAIN and self.middleButtonOneshot and not self.middleButtonHandled)
        self.page.set(self.PAGE_VIEW_TIMER, self.timerButtonTrigger)
        self.middleButtonHandled.mark(self.timerButtonTrigger, self.timerButtonTrigger)

        self.lockButtonTrigger.mark(self.page == self.PAGE_MAIN and self.rightButtonOneshot and not self.rightButtonHandled)
        self.page.set(self.PAGE_LOCK, self.lockButtonTrigger)
        self.rightButtonHandled.mark(self.lockButtonTrigger, self.lockButtonTrigger)

        # Select stove page
        self.selectButtonTrigger.mark(self.page == self.PAGE_SELECT_STOVE and self.leftButtonOneshot and not self.leftButtonHandled)
        self.page.set(self.PAGE_CHANGE_STOVE, self.selectButtonTrigger)
        self.leftButtonHandled.mark(self.selectButtonTrigger, self.selectButtonTrigger)

        self.leftButtonTrigger.mark(self.page == self.PAGE_SELECT_STOVE and self.middleButtonOneshot and not self.middleButtonHandled)
        self.newSelectedStove.set(self.selectedStove - 1, self.selectedStove > 1, self.STOVE_COUNT)
        self.selectedStove.set(self.newSelectedStove, self.leftButtonTrigger)
        self.middleButtonHandled.mark(self.leftButtonTrigger, self.leftButtonTrigger)

        self.rightButtonTrigger.mark(self.page == self.PAGE_SELECT_STOVE and self.rightButtonOneshot and not self.rightButtonHandled)
        self.newSelectedStove.set(self.selectedStove + 1, self.selectedStove < self.STOVE_COUNT, 1)
        self.selectedStove.set(self.newSelectedStove, self.rightButtonTrigger)
        self.middleButtonHandled.mark(self.rightButtonTrigger, self.rightButtonTrigger)

        # Change stove page
        self.backButtonTrigger.mark(self.page == self.PAGE_CHANGE_STOVE and self.leftButtonOneshot and not self.leftButtonHandled)
        self.page.set(self.PAGE_MAIN, self.backButtonTrigger)
        self.leftButtonHandled.mark(self.backButtonTrigger, self.backButtonTrigger)

        self.downButtonTrigger.mark(self.page == self.PAGE_CHANGE_STOVE and self.middleButtonOneshot and not self.middleButtonHandled)

        self.newStove1Temperature.set(self.stove1Target - self.STOVE_TEMP_INC, self.stove1Target > 0, 0)
        self.stove1Target.set(self.newStove1Temperature, self.downButtonTrigger and self.selectedStove == 1)

        self.newStove2Temperature.set(self.stove2Target - self.STOVE_TEMP_INC, self.stove2Target > 0, 0)
        self.stove2Target.set(self.newStove2Temperature, self.downButtonTrigger and self.selectedStove == 2)

        self.newStove3Temperature.set(self.stove3Target - self.STOVE_TEMP_INC, self.stove3Target > 0, 0)
        self.stove3Target.set(self.newStove3Temperature, self.downButtonTrigger and self.selectedStove == 3)

        self.newStove4Temperature.set(self.stove4Target - self.STOVE_TEMP_INC, self.stove4Target > 0, 0)
        self.stove4Target.set(self.newStove4Temperature, self.downButtonTrigger and self.selectedStove == 4)

        self.middleButtonHandled.mark(self.downButtonTrigger, self.downButtonTrigger)

        self.upButtonTrigger.mark(self.page == self.PAGE_CHANGE_STOVE and self.rightButtonOneshot and not self.rightButtonHandled)

        self.newStove1Temperature.set(self.stove1Target + self.STOVE_TEMP_INC, self.stove1Target < self.STOVE_TEMP_MAX, self.STOVE_TEMP_MAX)
        self.stove1Target.set(self.newStove1Temperature, self.upButtonTrigger and self.selectedStove == 1)

        self.newStove2Temperature.set(self.stove2Target + self.STOVE_TEMP_INC, self.stove2Target < self.STOVE_TEMP_MAX, self.STOVE_TEMP_MAX)
        self.stove2Target.set(self.newStove2Temperature, self.upButtonTrigger and self.selectedStove == 2)

        self.newStove3Temperature.set(self.stove3Target + self.STOVE_TEMP_INC, self.stove3Target < self.STOVE_TEMP_MAX, self.STOVE_TEMP_MAX)
        self.stove3Target.set(self.newStove3Temperature, self.upButtonTrigger and self.selectedStove == 3)

        self.newStove4Temperature.set(self.stove4Target + self.STOVE_TEMP_INC, self.stove4Target < self.STOVE_TEMP_MAX, self.STOVE_TEMP_MAX)
        self.stove4Target.set(self.newStove4Temperature, self.upButtonTrigger and self.selectedStove == 4)

        self.rightButtonHandled.mark(self.upButtonTrigger, self.upButtonTrigger)

        # View timer page
        # self.back2ButtonTrigger.mark(self.page == self.PAGE_VIEW_TIMER and self.leftButtonOneshot and not self.leftButtonHandled)
        # self.page.set(self.PAGE_MAIN, self.back2ButtonTrigger)
        # self.leftButtonHandled.mark(self.back2ButtonTrigger, self.back2ButtonTrigger)

        # self.change2ButtonTrigger.mark(self.page == self.PAGE_VIEW_TIMER and self.middleButtonOneshot and not self.middleButtonHandled)
        # self.page.set(self.PAGE_CHANGE_TIMER, self.change2ButtonTrigger)
        # self.middleButtonHandled.mark(self.change2ButtonTrigger, self.change2ButtonTrigger)

        # Change timer page
        # TODO

        # Trigger update screen when a button was handled
        self.updateScreen.mark(self.leftButtonHandled or self.middleButtonHandled or self.rightButtonHandled)
        self.cycleCounter.set(self.cycleCounter + 1)
