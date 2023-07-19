model rocket_controller
  input Real ti;
  input Real weight;
  parameter Real weight_max;
  parameter Real t0;
  output Real w;
  output Boolean engine_on;
equation
  if (ti < t0) then
    engine_on = false;
  else
    engine_on = true;
  end if;

  if (weight > 0. and engine_on == true) then
    w = 1.;
  else
    w = 0.;
  end if;

end rocket_controller;
