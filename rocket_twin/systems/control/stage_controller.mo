model stage_controller
  input Boolean is_on;
  output Real w;
equation
  if (is_on == true) then
    w = 1.;
  else
    w = 0.;
  end if;
end stage_controller;
