/*******************************************************************************
  MPLAB Harmony Application Source File
  
  Company:
    Microchip Technology Inc.
  
  File Name:
    app.c

  Summary:
    This file contains the source code for the MPLAB Harmony application.

  Description:
    This file contains the source code for the MPLAB Harmony application.  It 
    implements the logic of the application's state machine and it may call 
    API routines of other MPLAB Harmony modules in the system, such as drivers,
    system services, and middleware.  However, it does not call any of the
    system interfaces (such as the "Initialize" and "Tasks" functions) of any of
    the modules in the system or make any assumptions about when those functions
    are called.  That is the responsibility of the configuration-specific system
    files.
 *******************************************************************************/

// DOM-IGNORE-BEGIN
/*******************************************************************************
Copyright (c) 2013-2014 released Microchip Technology Inc.  All rights reserved.

Microchip licenses to you the right to use, modify, copy and distribute
Software only when embedded on a Microchip microcontroller or digital signal
controller that is integrated into your product or third party product
(pursuant to the sublicense terms in the accompanying license agreement).

You should refer to the license agreement accompanying this Software for
additional information regarding your rights and obligations.

SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF
MERCHANTABILITY, TITLE, NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.
IN NO EVENT SHALL MICROCHIP OR ITS LICENSORS BE LIABLE OR OBLIGATED UNDER
CONTRACT, NEGLIGENCE, STRICT LIABILITY, CONTRIBUTION, BREACH OF WARRANTY, OR
OTHER LEGAL EQUITABLE THEORY ANY DIRECT OR INDIRECT DAMAGES OR EXPENSES
INCLUDING BUT NOT LIMITED TO ANY INCIDENTAL, SPECIAL, INDIRECT, PUNITIVE OR
CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, COST OF PROCUREMENT OF
SUBSTITUTE GOODS, TECHNOLOGY, SERVICES, OR ANY CLAIMS BY THIRD PARTIES
(INCLUDING BUT NOT LIMITED TO ANY DEFENSE THEREOF), OR OTHER SIMILAR COSTS.
 *******************************************************************************/
// DOM-IGNORE-END


// *****************************************************************************
// *****************************************************************************
// Section: Included Files 
// *****************************************************************************
// *****************************************************************************

#include "app.h"
#include "debug.h"
#include "app_public.h"
// *****************************************************************************
// *****************************************************************************
// Section: Global Data Definitions
// *****************************************************************************
// *****************************************************************************

// *****************************************************************************
/* Application Data

  Summary:
    Holds application data

  Description:
    This structure holds the application's data.

  Remarks:
    This structure should be initialized by the APP_Initialize function.
    
    Application strings and buffers are be defined outside this structure.
*/

APP_DATA appData;

QueueHandle_t queue1 = 0;

// *****************************************************************************
// *****************************************************************************
// Section: Application Callback Functions
// *****************************************************************************
// *****************************************************************************

/* TODO:  Add any necessary callback functions.
*/

// *****************************************************************************
// *****************************************************************************
// Section: Application Local Functions
// *****************************************************************************
// *****************************************************************************


/* TODO:  Add any necessary local functions.
*/


// *****************************************************************************
// *****************************************************************************
// Section: Application Initialization and State Machine Functions
// *****************************************************************************
// *****************************************************************************

/*******************************************************************************
  Function:
    void APP_Initialize ( void )

  Remarks:
    See prototype in app.h.
 */

void APP_Initialize ( void )
{
    // Initialize ADC
    DRV_ADC_Open();
    DRV_ADC_Start();
    
    /* Place the App state machine in its initial state. */
    appData.state = APP_STATE_INIT;
    appData.heartbeatTimer = DRV_HANDLE_INVALID;
    appData.heartbeatCount = 0;
    appData.heartbeatToggle = false;

    queue1 = xQueueCreate(30, sizeof(unsigned int));
    
    /* TODO: Initialize your application's state machine and other
     * parameters.
     */
    SYS_PORTS_Clear( PORTS_ID_0, PORT_CHANNEL_D, 0xFF );
    SYS_PORTS_Write( PORTS_ID_0, PORT_CHANNEL_D, '0' );
}

static void APP_TimerCallback ( uintptr_t context, uint32_t alarmCount )
{
    int to_send;
    
    dbgOutputLoc(ISR_ENTERED);
    
    BaseType_t *pxHigherPriorityTaskWoken = pdFALSE;
           
    appData.heartbeatCount++;
    if (appData.heartbeatCount >= APP_HEARTBEAT_COUNT_MAX)
    {
       appData.heartbeatCount = 0;
       appData.heartbeatToggle = true;
    }
    
    to_send = appData.heartbeatCount;
    
    dbgOutputLoc(ISR_BEFORE_SEND_RECEIVE_QUEUE);
    xQueueSendToBackFromISR(queue1, &to_send, pxHigherPriorityTaskWoken);
    dbgOutputLoc(ISR_AFTER_SEND_RECEIVE_QUEUE);
    
    // This must be the last thing that is done in the ISR
    portEND_SWITCHING_ISR(pxHigherPriorityTaskWoken);
    
    dbgOutputLoc(ISR_EXIT);
}

/******************************************************************************
  Function:
    void APP_Tasks ( void )

  Remarks:
    See prototype in app.h.
 */

void APP_Tasks ( void )
{
    dbgOutputLoc(TASK_ENTERED);
    
    int pvBuffer;
    
 /* Signal the application's heartbeat. */
    if (appData.heartbeatToggle == true)
    {
        SYS_PORTS_PinToggle(PORTS_ID_0, APP_HEARTBEAT_PORT,
        APP_HEARTBEAT_PIN);
        appData.heartbeatToggle = false;
    }
    /* Check the application's current state. */
    switch ( appData.state )
    {
        /* Application's initial state. */
        case APP_STATE_INIT:
        {
            appData.heartbeatTimer = DRV_TMR_Open( APP_HEARTBEAT_TMR,
                                                    DRV_IO_INTENT_EXCLUSIVE);
            if ( DRV_HANDLE_INVALID != appData.heartbeatTimer )
            {
                DRV_TMR_AlarmRegister(appData.heartbeatTimer,
                                        APP_HEARTBEAT_TMR_PERIOD,
                                        APP_HEARTBEAT_TMR_IS_PERIODIC,
                                        (uintptr_t)&appData,
                                        APP_TimerCallback);
                DRV_TMR_Start(appData.heartbeatTimer);
                appData.state = APP_STATE_IDLE;
            }
            break;
         }

        case APP_STATE_IDLE:
        {
            dbgOutputLoc(TASK_BEFORE_WHILE_LOOP);
            
            dbgOutputLoc(TASK_BEFORE_SEND_RECEIVE_QUEUE);
            xQueueReceive(queue1, &pvBuffer, portMAX_DELAY);
            dbgOutputLoc(TASK_AFTER_SEND_RECEIVE_QUEUE);
            
            dbgUARTVal(pvBuffer);
            
            dbgUARTVal('T');
            dbgUARTVal('e');
            dbgUARTVal('a');
            dbgUARTVal('m');
            dbgUARTVal('_');
            dbgUARTVal('5');

            SYS_PORTS_Clear( PORTS_ID_0, PORT_CHANNEL_E, 0xFF );
            dbgOutputVal('T');
            dbgOutputVal('e');
            dbgOutputVal('a');
            dbgOutputVal('m');
            dbgOutputVal('_');
            dbgOutputVal('5');
            
            break;
        }
    
        case APP_STATE_SERVICE_TASKS:
        {
        
            break;
        }

        /* TODO: implement your application state machine.*/
        

        /* The default state should never be executed. */
        default:
        {
            /* TODO: Handle error in application's state machine. */
            break;
        }
    }
}

/*******************************************************************************
 End of File
 */
