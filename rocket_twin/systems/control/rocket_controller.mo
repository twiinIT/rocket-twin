model rocket_controller
  input Real ti;
  input Real weight;
  parameter Real weight_max;
  parameter Real t0;
  output Real w;
  output Real flying;
equation
  if (ti > t0) then
    flying = 1;
  else
    flying = 0;
  end if;

  if (weight > 0. and flying > 0.5) then
    w = 1.;
  else
    w = 0.;
  end if;

end rocket_controller;
