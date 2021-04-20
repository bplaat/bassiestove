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
from constants import Constants

class Timing(simpylc.Chart):
    def __init__(self):
        simpylc.Chart.__init__(self)

    def define(self):
        bassiestove = simpylc.world.bassieStove

        # State
        self.channel(bassiestove.page, simpylc.green, 0, Constants.PAGE_CHANGE_STOVE, 50)
        self.channel(bassiestove.lockCounter, simpylc.green, 1, 3, 50)
        self.channel(bassiestove.selectedLock, simpylc.green, 1, 3, 50)
        self.channel(bassiestove.selectedStove, simpylc.green, 1, Constants.STOVE_COUNT, 50)
        self.channel(bassiestove.updateScreen, simpylc.green, 0, 1, 50)

        # Stoves
        self.channel(bassiestove.stove1Value, simpylc.red, 0, Constants.STOVE_TEMP_MAX, 75)
        self.channel(bassiestove.stove2Value, simpylc.red, 0, Constants.STOVE_TEMP_MAX, 75)
        self.channel(bassiestove.stove3Value, simpylc.red, 0, Constants.STOVE_TEMP_MAX, 75)
        self.channel(bassiestove.stove4Value, simpylc.red, 0, Constants.STOVE_TEMP_MAX, 75)

        # Buttons
        self.channel(bassiestove.leftButton, simpylc.yellow, 0, 1, 50)
        self.channel(bassiestove.middleButton, simpylc.yellow, 0, 1, 50)
        self.channel(bassiestove.rightButton, simpylc.yellow, 0, 1, 50)
