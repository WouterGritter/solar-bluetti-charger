# Solar bluetti charger

This utility allows you to charge your bluetti from wall-power (230v) using only power that would otherwise
be redelivered to your power utility company. If you have a bluetti sitting idle, and you don't get
paid as much for redelivering power as you pay for delivered power, this might just be the perfect
solution for you.

This utility monitors the incoming/outgoing power and decides whether to charge your bluetti device, with
an emergency override if the bluetti charge gets too low (for on winter nights, for example). This ensures
continuous power output.

If you connect stuff like a server/computer or fridges to the bluetti, you will essentially run them on
solar power only (if you have enough solar panels of course). This also has the added bonus of acting
like a UPS for power failures, which can be handy for servers/computers and fridges.

# The repository

The repository uses abstraction to allow you to implement your own 'adapter code' for your
bluetti/power-station and smart meter, so the usages aren't limited to bluetti devices only.

# My setup

Right now the code implements connectivity to bluetti through bluetooth, and I wrote an adapter for
my custom smart meter interface. I use a Tapo P110 plug for turning the charger on and off, which has
the added bonus of including power monitoring as well. Needless to say, the code can be adapted to connect
to any power-station you might have. You can also run the software on a Raspberry Pi, and (dis)connect
the charger through a relay connected to the Pi, if you wish to do so. If you write a bridge for your
own setup, feel free to open a pull request. If many bridges are written, I might look into a way to
configure it easily without modifying the code.

# Simulation

I've also implemented bridges for simulating a bluetti device, if this is something you'd like to do.
