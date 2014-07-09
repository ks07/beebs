#include <support.h>
#include <avr/io.h>

void initialise_board()
{
  PIN_INIT(C, 0);
  PIN_CLEAR(C, 0);

  /* Testing timer */
  /* Based on http://www.avrfreaks.net/index.php?name=PNphpBB2&file=viewtopic&t=50106 */
  TCCR1B |= ((1 << CS10) | (1 << CS12)); // Set up timer at Fcpu/1024 
  for (;;)
  {
    if (TCNT1 >= 32000)
    //if (TCNT1 >= 15624)
      break;
  }
}

void start_trigger()
{
  PIN_SET(C, 0);
}

void stop_trigger()
{
  PIN_CLEAR(C, 0);
}
