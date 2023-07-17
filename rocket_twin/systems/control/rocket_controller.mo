model rocket_controller
  input Real ti;
  output Real w;
equation
  if (5. < ti and ti < 15.) then
    w = 1.;
  else
    w = 0.;
  end if;

end rocket_controller;
