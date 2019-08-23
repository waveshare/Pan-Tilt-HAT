#include "PCA9685.h"


/******************************************************************************
function:	
	Set duty cycle
parameter	:
	channel : Channel number
	on      : Drive output turn-on time 
	off     : PWM duty cycle 
******************************************************************************/
void PCA9685_setPWM(UBYTE channel, UWORD on, UWORD off)
{


    IIC_Write(LED0_ON_L + 4 * channel, on & 0xFF);
    IIC_Write(LED0_ON_H + 4 * channel, on >> 8);
    IIC_Write(LED0_OFF_L + 4 * channel, off & 0xFF);
    IIC_Write(LED0_OFF_H + 4 * channel, off >> 8);
}

/******************************************************************************
function:	
	Set duty cycle
parameter	:
	channel : Channel number
	value   : Set value 500 - 2500 
******************************************************************************/
void PCA9685_setServoPulse(UBYTE channel, UWORD value)
{
	value = value * 4096 / 20000;
    PCA9685_setPWM(channel, 0, value);
}


void PCA9685_Set_Rotation_Angle(UBYTE channel, UBYTE Angle)
{
    UWORD temp;
    if(Angle < 0  &&  Angle >180){
        printf("Angle out of range \n");
    }
    else{
        temp = Angle * (2000 / 180) + 500;
        PCA9685_setServoPulse(channel, temp);
    }
}

/******************************************************************************
function:	
	PCA9685 initialization 
******************************************************************************/
void Init_PCA9685()
{
	UDOUBLE prescaleval,oldmode;
	
	IIC_Write( MODE1, 0x00);
	prescaleval = 25000000;   
	prescaleval /= 4096;      
	prescaleval /= PWM_I2C_Hz;
	prescaleval -= 1.0;
	
	prescaleval=prescaleval+3;

	oldmode=IIC_Read( MODE1);
	IIC_Write( MODE1,  (oldmode & 0x7F) | 0x10);
	IIC_Write( PRESCALE, prescaleval);
	IIC_Write( MODE1, oldmode);
	DEV_Delay_ms(200);
	IIC_Write( MODE1, oldmode | 0x80);
    IIC_Write(MODE2, 0x04);

	PCA9685_setServoPulse(0, 1500);
	PCA9685_setServoPulse(1, 1500);
}

