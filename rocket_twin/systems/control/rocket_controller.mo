model rocket_controller
  input Boolean flying;
  input Real weight_1;
  input Real weight_2;
  input Real weight_3;
  output Real is_on_1;
  output Real is_on_2;
  output Real is_on_3;
equation
  if (flying == false) then
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
