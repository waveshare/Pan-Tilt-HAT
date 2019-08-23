#ifndef _TSL2581_H_
#define _TSL2581_H_

#include "DEV_Config.h"



//extern UWORD Channel_0, Channel_1;	 
#define Write_success 1
#define Write_fail 0;	 
	 
	 
// I2C address options
#define ADDR_LOW          0x29
#define ADDR_FLOAT        0x39   // Default address (pin left floating)
#define ADDR_HIGH         0x49


#define Light I2C Addr ADDR_FLOAT
	 
//---------------------------------------------------
// x       xx      xxxxx 
//CMD TRANSACTION ADDRESS

#define COMMAND_CMD   0x80   
#define TRANSACTION 0x40    // read/write block protocol.
#define TRANSACTION_SPECIAL 0X60
//ADDRESS
#define CONTROL   	0x00
#define TIMING    	0x01
#define INTERRUPT 	0X02
#define THLLOW 		0x03
#define THLHIGH 	0X04
#define THHLOW 		0x05
#define THHHIGH 	0X06
#define ANALOG 		0X07

#define ID 			0X12
#define DATA0LOW 	0X14	// 1 10 1 0010 
#define DATA0HIGH 	0X15
#define DATA1LOW 	0X16
#define DATA1HIGH 	0X17
//---------------------------------------------------

#define ADC_EN				0X02
#define CONTROL_POWERON   	0x01
#define CONTROL_POWEROFF  	0x00
#define INTR_TEST_MODE 		0X30
#define INTR_INTER_MODE 	0X18//At least 8 cycles to stabilize, otherwise the interrupt will continue to maintain 0 

//TRANSACTION_SPECIAL
#define SPECIAL_FUN_RESER1 		0X00
#define SPECIAL_FUN_INTCLEAR 	0X01
#define SPECIAL_FUN_STOPMAN 	0X02
#define SPECIAL_FUN_STARTMAN 	0X03
#define SPECIAL_FUN_RESER2 		0X0F

//INTERRUPT
#define INTEGRATIONTIME_Manual 	0x00
#define INTEGRATIONTIME_2Z7MS 	0xFF
#define INTEGRATIONTIME_5Z4MS 	0xFE
#define INTEGRATIONTIME_51Z3MS 	0xED
#define INTEGRATIONTIME_100MS 	0xDB
#define INTEGRATIONTIME_200MS 	0xB6
#define INTEGRATIONTIME_400MS 	0x6C
#define INTEGRATIONTIME_688MS 	0x01

//ANALOG
#define GAIN_1X 	0x00
#define GAIN_8X 	0x01
#define GAIN_16X 	0x02
#define GAIN_111X 	0x03


#define LUX_SCALE 16 // scale by 2^16
#define RATIO_SCALE 9 // scale ratio by 2^9
//---------------------------------------------------
// Integration time scaling factors
//---------------------------------------------------
#define CH_SCALE 16 // scale channel values by 2^16

// Nominal 400 ms integration. 
// Specifies the integration time in 2.7-ms intervals
// 400/2.7 = 148
#define NOM_INTEG_CYCLE 148
//---------------------------------------------------
// Gain scaling factors
//---------------------------------------------------
#define CH0GAIN128X 107 // 128X gain scalar for Ch0
#define CH1GAIN128X 115 // 128X gain scalar for Ch1

//---------------------------------------------------
#define K1C 0x009A // 0.30 * 2^RATIO_SCALE
#define B1C 0x2148 // 0.130 * 2^LUX_SCALE
#define M1C 0x3d71 // 0.240 * 2^LUX_SCALE

#define K2C 0x00c3 // 0.38 * 2^RATIO_SCALE
#define B2C 0x2a37 // 0.1649 * 2^LUX_SCALE
#define M2C 0x5b30 // 0.3562 * 2^LUX_SCALE

#define K3C 0x00e6 // 0.45 * 2^RATIO_SCALE
#define B3C 0x18ef // 0.0974 * 2^LUX_SCALE
#define M3C 0x2db9 // 0.1786 * 2^LUX_SCALE

#define K4C 0x0114 // 0.54 * 2^RATIO_SCALE
#define B4C 0x0fdf // 0.062 * 2^LUX_SCALE
#define M4C 0x199a // 0.10 * 2^LUX_SCALE

#define K5C 0x0114 // 0.54 * 2^RATIO_SCALE
#define B5C 0x0000 // 0.00000 * 2^LUX_SCALE
#define M5C 0x0000 // 0.00000 * 2^LUX_SCALE
//---------------------------------------------------

void Init_TSL2581(void);
void Reload_register(void);
void SET_Interrupt_Threshold(UWORD min, UWORD max);
void Read_Channel(void);
UBYTE Read_ID();
UDOUBLE calculateLux(UWORD iGain, UWORD tIntCycles);

#endif


