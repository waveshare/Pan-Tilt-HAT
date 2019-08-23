#ifndef _SERVO_H_
#define _SERVO_H_


#include "DEV_Config.h"

#define SUBADR1          0x02
#define SUBADR2          0x03
#define SUBADR3          0x04
#define MODE1            0x00
#define MODE2            0x01
#define PRESCALE         0xFE
#define LED0_ON_L        0x06
#define LED0_ON_H        0x07
#define LED0_OFF_L       0x08
#define LED0_OFF_H       0x09
#define ALLLED_ON_L      0xFA
#define ALLLED_ON_H      0xFB
#define ALLLED_OFF_L     0xFC
#define ALLLED_OFF_H     0xFD

#define PWM_I2C_Addr 	 0x40
#define PWM_I2C_Hz 	 	 50

void PCA9685_setServoPulse(UBYTE channel, UWORD value);
void Init_PCA9685();
void PCA9685_setPWM(UBYTE channel, UWORD on, UWORD off);
void PCA9685_Set_Rotation_Angle(UBYTE channel, UBYTE Angle);
#endif
