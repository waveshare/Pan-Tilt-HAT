#include <stdio.h>      //printf()
#include <stdlib.h>     //exit()
#include <signal.h>

#include "DEV_Config.h"
#include "PCA9685.h"

void  Handler(int signo)
{
    //System Exit
    printf("\r\nHandler:Program stop\r\n"); 
    
    IIC_Write(MODE2,0x00);
    DEV_ModuleExit();

    exit(0);
}

int main(int argc, char **argv)
{
	int  i;
	if (DEV_ModuleInit() == 1)
		return 1;

    // Exception handling:ctrl + c
    signal(SIGINT, Handler);
    //PCA9685 initialization
	Init_PCA9685();

    PCA9685_Set_Rotation_Angle(0, 80);
	while(1)
	{
		for(i = 10; i < 170; i = i + 1){
            PCA9685_Set_Rotation_Angle(1, i);
            if(i < 80)
                PCA9685_Set_Rotation_Angle(0, i);
            DEV_Delay_ms(25);
		}
		for(i = 170; i > 10; i = i - 1){
            PCA9685_Set_Rotation_Angle(1, i);
            if(i < 80)
                PCA9685_Set_Rotation_Angle(0, i);
            DEV_Delay_ms(25);
		}        	
	}

	DEV_ModuleExit();
    return 0;
}