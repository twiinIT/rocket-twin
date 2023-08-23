model rocket_controller
  input Real ti;
  input Real weight_1;
  input Real weight_2;
  input Real weight_3;
  parameter Real tl;
  parameter Real weight_max_1;
  parameter Real weight_max_2;
  parameter Real weight_max_3;
  output Real is_on_1;
  output Real is_on_2;
  output Real is_on_3;
  output Real fueling;
  output Real flying;
equation
  if (flying < 0.5 and weight_3 < weight_max_3) then
    fueling = 1.;
  else
    fueling = 0.;
  end if;

  if (ti < tl) then
    flying = 0.;
  else
    flying = 1.;
  end if;

  if (flying < 0.5) then
    is_on_1 = 0.;
    is_on_2 = 0.;
    is_on_3 = 0.;
  else
    if (weight_1 >= 0.1) then
      is_on_1 = 1.;
      is_on_2 = 0.;
      is_on_3 = 0.;
    elseif (weight_2 >= 0.1) then
      is_on_1 = 0.;
      is_on_2 = 1.;
      is_on_3 = 0.;
    elseif (weight_3 >= 0.1) then
      is_on_1 = 0.;
      is_on_2 = 0.;
      is_on_3 = 1.;
    else
      is_on_1 = 0.;
      is_on_2 = 0.;
      is_on_3 = 0.;
    end if;
  end if;

end rocket_controller;
