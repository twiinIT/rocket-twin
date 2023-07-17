model controller
  input Real ti;
  output Real w;
equation
  if (ti < 5.) then
    w = 1.;
  else
    w = 0.;
  end if;

end controller;
