#include <support.h>
#include <avr/io.h>

void initialise_board()
{
  PIN_INIT(B, 5);
}

void start_trigger()
{
  PIN_SET(B, 5);
}

void stop_trigger()
{
  PIN_CLEAR(B, 5);
}
