model station_controller
  input Boolean fueling;       // Whether the system is in its fueling phase
  output Real w;               // Command flow
equation
  if (fueling == true) then
    w = 1.;
  else
    w = 0.;
  end if;
end station_controller;
