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

import simpylc as sp # BUG in SimPyLC 😢
import random

class Constants:
    PAGE_LOCK = 0
    PAGE_MAIN = 1
    PAGE_SELECT_STOVE = 2
    PAGE_CHANGE_STOVE = 3
    PAGE_VIEW_TIMER = 4
    PAGE_CHANGE_TIMER = 5

    LOCK_COUNT = 5

    STOVE_COUNT = 4
    STOVE_TEMP_MAX = 350
    STOVE_TEMP_INC = 10

    TIMER_MAX = 60 * 60 - 1
    TIMER_INC = 5

    def __init__(self):
        bassiestove = sp.world.bassieStove

        bassiestove.PAGE_LOCK.set(self.PAGE_LOCK)
        bassiestove.PAGE_MAIN.set(self.PAGE_MAIN)
        bassiestove.PAGE_SELECT_STOVE.set(self.PAGE_SELECT_STOVE)
        bassiestove.PAGE_CHANGE_STOVE.set(self.PAGE_CHANGE_STOVE)
        bassiestove.PAGE_VIEW_TIMER.set(self.PAGE_VIEW_TIMER)
        bassiestove.PAGE_CHANGE_TIMER.set(self.PAGE_CHANGE_TIMER)

        bassiestove.LOCK_COUNT.set(self.LOCK_COUNT)

        bassiestove.STOVE_COUNT.set(self.STOVE_COUNT)
        bassiestove.STOVE_TEMP_MAX.set(self.STOVE_TEMP_MAX)
        bassiestove.STOVE_TEMP_INC.set(self.STOVE_TEMP_INC)

        bassiestove.TIMER_MAX.set(self.TIMER_MAX)
        bassiestove.TIMER_INC.set(self.TIMER_INC)

        bassiestove.page.set(self.PAGE_LOCK)
        bassiestove.randSeed.set(random.randint(0, 3600))
