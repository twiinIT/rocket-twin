model station_controller
  input Boolean fueling;
  output Real w;
equation
  if (fueling == true) then
    w = 1.;
  else
    w = 0.;
  end if;
end station_controller;