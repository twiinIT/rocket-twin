model controller
  input Real is_on;
  output Real w;
equation
  if (is_on > 0.5) then
    w = 1.;
  else
    w = 0.;
  end if;

end controller;
