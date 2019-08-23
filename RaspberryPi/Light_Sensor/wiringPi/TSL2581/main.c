#include <stdio.h>      //printf()
#include <stdlib.h>     //exit()
#include <signal.h>

#include "DEV_Config.h"
#include "TSL2581.h"

void  Handler(int signo)
{
    //System Exit
    printf("\r\nHandler:Program stop\r\n"); 
    
    DEV_ModuleExit();

    exit(0);
}

int main(int argc, char **argv)
{
	int  lux;

	if (DEV_ModuleInit()==1)return 1;
    // Exception handling:ctrl + c
    signal(SIGINT, Handler);
	//because The lower four bits are the silicon version number
	printf("READ ID = 0x%02X\n\t", Read_ID() & 0xf0);
	
	printf("---- i2c sensor init ----\n");
    //TSL2581 initialization
	Init_TSL2581();
	
	while(1)
	{		
		lux  =  calculateLux(1, NOM_INTEG_CYCLE);
		printf("lux = %d \r\n", lux);
		DEV_Delay_ms(500);
	}

	DEV_ModuleExit();
    return 0; 
}