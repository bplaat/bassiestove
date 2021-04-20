/*
Copyright (C) 2013 - 2020 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicence for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your licence.
*/

#include <LiquidCrystal_I2C.h>

// LCD helper functions
#define LCD_WIDTH 20
#define LCD_HEIGHT 4
LiquidCrystal_I2C lcd(0x27, LCD_WIDTH, LCD_HEIGHT);

void print_centered(uint8_t y, const char* text) {
    lcd.setCursor((LCD_WIDTH - strlen(text)) / 2, y);
    lcd.print(text);
}

void print_columns_centered(uint8_t y, uint8_t count, const char* column, ...) {
    va_list columns;
    va_start(columns, column);

    uint8_t column_width = LCD_WIDTH / count;
    uint8_t x = 0;

    lcd.setCursor(x + (column_width - strlen(column)) / 2, y);
    lcd.print(column);
    x += column_width;

    if (LCD_WIDTH % count > 0) {
        x += 1;
    }

    for (uint8_t i = 0; i < count - 1; i++) {
        const char *column = va_arg(columns, const char*);
        lcd.setCursor(x + (column_width - strlen(column)) / 2, y);
        lcd.print(column);
        x += column_width;

        if (i == 0 && LCD_WIDTH % count == 2) {
            x += 1;
        }
    }

    va_end(columns);
}

// Pins
#define STOVE_1_LED_PIN 3
#define STOVE_2_LED_PIN 5
#define STOVE_3_LED_PIN 6
#define STOVE_4_LED_PIN 9

#define BEEPER_BIN 10

#define LEFT_BUTTON_PIN 2
#define MIDDLE_BUTTON_PIN 4
#define RIGHT_BUTTON_PIN 7

void setup() {
    Serial.begin(9600);

    // Init constants
    PAGE_LOCK = 0;
    PAGE_MAIN = 1;
    PAGE_SELECT_STOVE = 2;
    PAGE_CHANGE_STOVE = 3;
    PAGE_VIEW_TIMER = 4;
    PAGE_CHANGE_TIMER = 5;

    LOCK_COUNT = 5;

    STOVE_COUNT = 4;
    STOVE_TEMP_MAX = 350;
    STOVE_TEMP_INC = 10;

    TIMER_MAX = 60 * 60 - 1;
    TIMER_INC = 5;

    page = PAGE_LOCK;
    randSeed = random(0, 3600);

    // Init pins
    pinMode(STOVE_1_LED_PIN, OUTPUT);
    pinMode(STOVE_2_LED_PIN, OUTPUT);
    pinMode(STOVE_3_LED_PIN, OUTPUT);
    pinMode(STOVE_4_LED_PIN, OUTPUT);

    pinMode(BEEPER_BIN, OUTPUT);

    pinMode(LEFT_BUTTON_PIN, INPUT_PULLUP);
    pinMode(MIDDLE_BUTTON_PIN, INPUT_PULLUP);
    pinMode(RIGHT_BUTTON_PIN, INPUT_PULLUP);

    // Init lcd
    lcd.init();
    lcd.backlight();
}

void loop() {
    // Read buttons
    leftButton = !digitalRead(LEFT_BUTTON_PIN);
    middleButton = !digitalRead(MIDDLE_BUTTON_PIN);
    rightButton = !digitalRead(RIGHT_BUTTON_PIN);

    cycle();

    // Write beeper tone
    if (beeperFrequency != 0) {
        tone(BEEPER_BIN, beeperFrequency);
    } else {
        noTone(BEEPER_BIN);
    }

    // Write back stove values
    analogWrite(STOVE_1_LED_PIN, stove1Value / STOVE_TEMP_MAX * 255);
    analogWrite(STOVE_2_LED_PIN, stove2Value / STOVE_TEMP_MAX * 255);
    analogWrite(STOVE_3_LED_PIN, stove3Value / STOVE_TEMP_MAX * 255);
    analogWrite(STOVE_4_LED_PIN, stove4Value / STOVE_TEMP_MAX * 255);

    // Update screen when needed
    if (cycleCounter == 1 || updateScreen) {
        // Lock page
        if (page == PAGE_LOCK) {
            lcd.clear();
            print_centered(0, "BassieStove!");
            print_centered(1, "Your stove is locked");
            print_centered(2, "press the buttons");
            print_columns_centered(3, 3,
                selectedLock == 1 ? "PRESS" : "",
                selectedLock == 2 ? "PRESS" : "",
                selectedLock == 3 ? "PRESS" : ""
            );
        }

        // Main page
        if (page == PAGE_MAIN) {
            lcd.clear();
            print_centered(0, "BassieStove!");

            char stove1String[LCD_WIDTH];
            sprintf(stove1String, "%dC", (int)stove1Target);

            char stove2String[LCD_WIDTH];
            sprintf(stove2String, "%dC", (int)stove2Target);

            char stove3String[LCD_WIDTH];
            sprintf(stove3String, "%dC", (int)stove3Target);

            char stove4String[LCD_WIDTH];
            sprintf(stove4String, "%dC", (int)stove4Target);

            print_columns_centered(1, 4,
                stove1Target > 0 ? stove1String : "-",
                stove2Target > 0 ? stove2String : "-",
                stove3Target > 0 ? stove3String : "-",
                stove4Target > 0 ? stove4String : "-"
            );

            print_columns_centered(2, 4,
                selectedStove == 1 ? "[1]" : "1",
                selectedStove == 2 ? "[2]" : "2",
                selectedStove == 3 ? "[3]" : "3",
                selectedStove == 4 ? "[4]" : "4"
            );

            print_columns_centered(3, 3, "CHANGE", "TIMER", "LOCK");
        }

        // Select stove page
        if (page == PAGE_SELECT_STOVE) {
            lcd.clear();
            print_centered(0, "Select a stove:");

            char stove1String[LCD_WIDTH];
            sprintf(stove1String, "%dC", (int)stove1Target);

            char stove2String[LCD_WIDTH];
            sprintf(stove2String, "%dC", (int)stove2Target);

            char stove3String[LCD_WIDTH];
            sprintf(stove3String, "%dC", (int)stove3Target);

            char stove4String[LCD_WIDTH];
            sprintf(stove4String, "%dC", (int)stove4Target);

            print_columns_centered(1, 4,
                stove1Target > 0 ? stove1String : "-",
                stove2Target > 0 ? stove2String : "-",
                stove3Target > 0 ? stove3String : "-",
                stove4Target > 0 ? stove4String : "-"
            );

            print_columns_centered(2, 4,
                selectedStove == 1 ? "[1]" : "1",
                selectedStove == 2 ? "[2]" : "2",
                selectedStove == 3 ? "[3]" : "3",
                selectedStove == 4 ? "[4]" : "4"
            );

            print_columns_centered(3, 3, "SELECT", "LEFT", "RIGHT");
        }

        // Change stove page
        if (page == PAGE_CHANGE_STOVE) {
            lcd.clear();

            char tempString[LCD_WIDTH];
            sprintf(tempString, "Stove %d", (int)selectedStove);
            print_centered(0, tempString);

            if (selectedStove == 1) {
                sprintf(tempString, "Current: %dC", round(stove1Value));
            }
            if (selectedStove == 2) {
                sprintf(tempString, "Current: %dC", round(stove2Value));
            }
            if (selectedStove == 3) {
                sprintf(tempString, "Current: %dC", round(stove3Value));
            }
            if (selectedStove == 4) {
                sprintf(tempString, "Current: %dC", round(stove4Value));
            }
            print_centered(1, tempString);

            if (selectedStove == 1) {
                sprintf(tempString, "Target: %dC", (int)stove1Target);
            }
            if (selectedStove == 2) {
                sprintf(tempString, "Target: %dC", (int)stove2Target);
            }
            if (selectedStove == 3) {
                sprintf(tempString, "Target: %dC", (int)stove3Target);
            }
            if (selectedStove == 4) {
                sprintf(tempString, "Target: %dC", (int)stove4Target);
            }
            print_centered(2, tempString);

            print_columns_centered(3, 3, "BACK", "DOWN", "UP");
        }

        // View timer page
        if (page == PAGE_VIEW_TIMER) {
            lcd.clear();
            print_centered(0, "Timer");

            char tempString[LCD_WIDTH];
            int timeRemaining = timerTime - elapsed1(timerTimer);
            sprintf(tempString, "%02d:%02d remaining", (int)(timeRemaining / 60), (int)timeRemaining % 60);
            print_centered(1, timerStarted ? (timerFinished ? "Timer finished" : tempString) : "No timer is running");

            print_columns_centered(3, 3, "BACK", "", timerStarted ? "STOP" : "CREATE");
        }

        // Change timer page
        if (page == PAGE_CHANGE_TIMER) {
            lcd.clear();
            print_centered(0, "Create a timer:");

            char tempString[LCD_WIDTH];
            sprintf(tempString, "Time: %02d:%02d", (int)(timerTime / 60), (int)timerTime % 60);
            print_centered(1, tempString);

            print_columns_centered(3, 3, "START", "DOWN", "UP");
        }
    }
}
