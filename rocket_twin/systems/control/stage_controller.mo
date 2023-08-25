model stage_controller
  input Boolean is_on;   // Whether the controller is on or not
  output Real w;         // Command flow
equation
  if (is_on == true) then
    w = 1.;
  else
    w = 0.;
  end if;
end stage_controller;
