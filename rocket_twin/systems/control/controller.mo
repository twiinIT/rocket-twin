model controller
  input Real ti;
  output Real f;
  output Real wg;
  output Real wr;
equation
  if (ti < 5.) then
    f = 0.;
    wr = 0.;
    wg = 1.;
  elseif (ti < 15.) then
    f = 1.;
    wr = 1.;
    wg = 0.;
  else
    f = 0.;
    wr = 0.;
    wg = 0.;
  end if;

end controller;
