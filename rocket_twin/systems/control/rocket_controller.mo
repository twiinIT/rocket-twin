model rocket_controller
  input Boolean flying;    // Whether the rocket is mid-flight or not
  input Real weight_1;     // Stage 1 fuel mass
  input Real weight_2;     // Stage 2 fuel mass
  input Real weight_3;     // Stage 3 fuel mass
  output Real is_on_1;     // Whether the stage 1 is on or not
  output Real is_on_2;     // Whether the stage 2 is on or not
  output Real is_on_3;     // Whether the stage 3 is on or not
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
