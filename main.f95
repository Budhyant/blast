! blast load calculator, BLC
! By Joshua Hojung Chung
! "Airblast Parameters from TNT Spherical Air Burst & Hemispherical Surface Burst" by Charles N Kingerey & Gerald Bulmash, Tech Report ARBRL-TR-02555 dated April 1984.

program main
  implicit none

  integer:: re_i
  real :: distance, quantity, TNTequiv, scaled_distance         !input parameters
  real:: Pso, Iso, Pr, Ir, U, Ta, T_po                          !output parameters for air burst
  real:: s_Pso, s_Iso, s_Pr, s_Ir, s_U, s_Ta, s_T_po            !output parameters for surface burst

  !input data from GUI software
  !distance, stand off distance, [m]
  !quantity, required TNT amount, [kg]
  !TNTequiv, equivalent TNT coefficient, [m]
  open(unit=10, file="input.txt")
  read(10,*) distance, quantity, TNTequiv
  close(10)

  scaled_distance = distance/((quantity*TNTequiv)**(1./3.))

  !Air burst outputs
  Pso  = Ps_calc(scaled_distance)                                                                                       !Peak incident pressure         [kPa]
  Iso  = (Is_f1_calc(scaled_distance)+Is_F2_calc(scaled_distance))*quantity**(1./3.)                                    !Incident impulse               [kPa.msec]
  Pr   = Pr_calc(scaled_distance)                                                                                       !Peak reflected pressure        [kPa]
  Ir   = Ir_calc(scaled_distance)*quantity**(1./3.)                                                                     !Reflected impulse              [kPa.msec]
  U    = U_calc(scaled_distance)                                                                                        !Shock front velocity           [m/msec]
  Ta   = Ta_calc(scaled_distance)*quantity**(1./3.)                                                                     !Arrival time                   [msec]
  T_po = (T_f1_calc(scaled_distance)+T_f2_calc(scaled_distance)+T_f3_calc(scaled_distance))*quantity**(1./3.)           !Positive Phase Duration (T+)   [msec]

  !surface burst outputs
  s_Pso = s_Ps_calc(scaled_distance)                                                                                    !Peak incident pressure         [kPa]
  s_Iso = (s_Is_f1_calc(scaled_distance)+s_Is_F2_calc(scaled_distance))*quantity**(1./3.)                               !Incident impulse               [kPa.msec]
  s_Pr  = s_Pr_calc(scaled_distance)                                                                                    !Peak reflected pressure        [kPa]
  s_Ir  = s_Ir_calc(scaled_distance)*quantity**(1./3.)                                                                  !Reflected impulse              [kPa.msec]
  s_U   = s_U_calc(scaled_distance)                                                                                     !Shock front velocity           [m/msec]
  s_Ta  = s_Ta_calc(scaled_distance)*quantity**(1./3.)                                                                  !Arrival time                   [msec]
  s_T_po = (s_T_f1_calc(scaled_distance)+s_T_f2_calc(scaled_distance)+s_T_f3_calc(scaled_distance))*quantity**(1./3.)   !Positive Phase Duration (T+)   [msec]

  !TEST Results
  Print*, Pso, Iso, Pr, Ir, U, Ta, T_po
  Print*, s_Pso, s_Iso, s_Pr, s_Ir, s_U, s_Ta, s_T_po

  !txt output
  open(unit=11, file="output.txt")
  write(11,*)Pso, Iso, Pr, Ir, U, Ta, T_po
  write(11,*)s_Pso, s_Iso, s_Pr, s_Ir, s_U, s_Ta, s_T_po
  close(11)

  re_i = system("pause")

Contains
!Air Burst
  function Ps_calc(Z)
    real:: Ps_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x = -0.214362789151+(1.35034249993*logZ)
    fx = 1.69012801396*x
    fx2 = 0.00804973591951*(x**2)
    fx3 = 0.336743114941*(x**3)
    fx4 = 0.00516226351334*(x**4)
    fx5 = 0.0809228619888*(x**5)
    fx6 = 0.00478507266747*(x**6)
    fx7 = 0.00793030472242*(x**7)
    fx8 = 0.0007684469735*(x**8)

    Y = 2.611368669-fx+fx2+fx3-fx4-fx5-fx6+fx7+fx8

    IF (Z<0.0531) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    IF (anti_log_Y==0) then
        Print*, "none" !need to revise
        else
            Ps_calc = anti_log_Y
    END IF

  End function Ps_calc

  function Is_F1_calc(z)
    real:: Is_F1_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x = 2.34723921354+3.24299066475*logZ
    fx = -0.443749377691*x
    fx2 = 0.168825414684*(x**2)
    fx3 = 0.0348138030308*(x**3)
    fx4 = -0.010435192824*(x**4)
    fx5 = 0*(x**5)
    fx6 = 0*(x**6)
    fx7 = 0*(x**7)
    fx8 = 0*(x**8)

    Y = 2.38830516757+fx+fx2+fx3+fx4

    IF (Z<0.0531) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>0.792)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    Is_F1_calc=anti_log_Y

  end function Is_F1_calc

  function Is_F2_calc(z)
      real:: Is_F2_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x = -1.75305660315+2.30629231803*logZ
    fx = -0.40463292088*x
    fx2 = -0.0142721946082*(x**2)
    fx3 = 0.00912366316617*(x**3)
    fx4 = -0.0006750681404*(x**4)
    fx5 = -0.00800863718901*(x**5)
    fx6 = 0.00314819515931*(x**6)
    fx7 = 0.00152044783382*(x**7)
    fx8 = -0.0007470265899*(x**8)

    Y = 1.55197227115+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8

    IF (Z<0.792) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    Is_F2_calc=anti_log_Y

  end function Is_F2_calc

  function Pr_calc(z)
    real:: Pr_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x = -0.214362789151+1.35034249993*logZ
    fx = -2.21400538997*x
    fx2 = 0.035119031446*(x**2)
    fx3 = 0.657599992109*(x**3)
    fx4 = 0.0141818951887*(x**4)
    fx5 = -0.243076636231*(x**5)
    fx6 = -0.0158699803158*(x**6)
    fx7 = 0.0492741184234*(x**7)
    fx8 = 0.00227639644004*(x**8)
    fx9 = -0.00397126276058*(x**9)

    Y = 3.22958031387+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9

    IF (Z<0.0531) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    IF (anti_log_Y==0) then
        Print*, "none" !need to revise
        else
            Pr_calc = anti_log_Y
    END IF
  end function Pr_calc

  function Ir_calc(z)
    real:: Ir_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x = -0.204004553231+1.37882996018*logZ
    fx = -0.903118886091*x
    fx2 = 0.101771877942*(x**2)
    fx3 = -0.0242139751146*(x**3)
    fx4 = 0*(x**4)
    fx5 = 0*(x**5)
    fx6 = 0*(x**6)
    fx7 = 0*(x**7)
    fx8 = 0*(x**8)
    fx9 = 0*(x**9)

    Y = 2.55875660396+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9

    IF (Z<0.0531) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    Ir_calc = anti_log_Y

  end function Ir_calc

  function U_calc(z)
    real:: U_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x = -0.214362789151+1.35034249993*logZ
    fx = -0.650507560471*x
    fx2  = 0.291320654009*(x**2)
    fx3  = 0.307916322787*(x**3)
    fx4  = -0.183361123489*(x**4)
    fx5  = -0.197740454538*(x**5)
    fx6  = 0.0909119559768*(x**6)
    fx7  = 0.098926178054*(x**7)
    fx8  = -0.0287370990248*(x**8)
    fx9  = -0.0248730221702*(x**9)
    fx10 = 0.00496311705671*(x**10)
    fx11 = 0.00372242076361*(x**11)
    fx12 = -0.0003533736952*(x**12)
    fx13 = -0.0002292913709*(x**13)

    Y = -0.144615443471+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.0531) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    IF (anti_log_Y==0) then
        Print*, "none" !need to revise
        else
            U_calc = anti_log_Y
    END IF
  end function U_calc

  function Ta_calc(z)
    real:: Ta_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -0.253273111999+1.37407043777*logZ
    fx   = 1.36456871214*x
    fx2  = -0.0570035692784*(x**2)
    fx3  = -0.182832224796*(x**3)
    fx4  = 0.0118851436014*(x**4)
    fx5  = 0.0432648687627*(x**5)
    fx6  = -0.0007997367834*(x**6)
    fx7  = -0.00436073555033*(x**7)
    fx8  = 0*(x**8)
    fx9  = 0*(x**9)
    fx10 = 0*(x**10)
    fx11 = 0*(x**11)
    fx12 = 0*(x**12)
    fx13 = 0*(x**13)

    Y = 0.0720707787637+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.0531) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    Ta_calc = anti_log_Y

  end function Ta_calc

  function T_f1_calc(z)
    real:: T_f1_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = 2.26367268496+5.11588554305*logZ
    fx   = 0.164953518069*x
    fx2  = 0.127788499497*(x**2)
    fx3  = 0.00291430135946*(x**3)
    fx4  = 0.0018795744922*(x**4)
    fx5  = 0.017341396254*(x**5)
    fx6  = 0.0026973975804*(x**6)
    fx7  = -0.00361976502798*(x**7)
    fx8  = -0.00100926577934*(x**8)
    fx9  = 0.*(x**9)
    fx10 = 0.*(x**10)
    fx11 = 0.*(x**11)
    fx12 = 0.*(x**12)
    fx13 = 0.*(x**13)

    Y = -0.686608550419+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.147) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>=0.888)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    T_f1_calc = anti_log_Y

  end function T_f1_calc

  function T_f2_calc(z)
    real:: T_F2_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -1.33361206714+9.2996288611*logZ
    fx   = -0.0297944268969*x
    fx2  = 0.0306329542941*(x**2)
    fx3  = 0.018340557407*(x**3)
    fx4  = -0.0173964666286*(x**4)
    fx5  = -0.00106321963576*(x**5)
    fx6  = 0.0056206003128*(x**6)
    fx7  = 0.0001618217499*(x**7)
    fx8  = -0.0006860188944*(x**8)
    fx9  = 0*(x**9)
    fx10 = 0*(x**10)
    fx11 = 0*(x**11)
    fx12 = 0*(x**12)
    fx13 = 0*(x**13)

    Y = 0.23031841078+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.888) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>2.28)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    T_F2_calc = anti_log_Y

  end function T_f2_calc

  function T_f3_calc(z)
    real:: T_f3_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -3.13005805346+3.1524725364*logZ
    fx   = 0.0967031995552*x
    fx2  = -0.00801302059667*(x**2)
    fx3  = 0.00482705779732*(x**3)
    fx4  = 0.00187587272287*(x**4)
    fx5  = -0.00246738509321*(x**5)
    fx6  = -0.000841116668*(x**6)
    fx7  = 0.0006193291052*(x**7)
    fx8  = 0*(x**8)
    fx9  = 0*(x**9)
    fx10 = 0*(x**10)
    fx11 = 0*(x**11)
    fx12 = 0*(x**12)
    fx13 = 0*(x**13)

    Y = 0.621036276475+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z <= 2.28) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    T_f3_calc = anti_log_Y

  end function T_f3_calc

!surface burst
  function s_Ps_calc(z)
    real:: s_Ps_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -0.214362789151+1.35034249993*logZ
    fx   = -1.6958988741*x
    fx2  = -0.154159376846*(x**2)
    fx3  = 0.514060730593*(x**3)
    fx4  = 0.0988534365274*(x**4)
    fx5  = -0.293912623038*(x**5)
    fx6  = -0.0268112345019*(x**6)
    fx7  = 0.109097496421*(x**7)
    fx8  = 0.00162846756311*(x**8)
    fx9  = -0.0214631030242*(x**9)
    fx10 = 0.0001456723382*(x**10)
    fx11 = 0.00167847752266*(x**11)
    fx12 = 0*(x**12)
    fx13 = 0*(x**13)

    Y = 2.78076916577+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.064) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    IF (anti_log_Y==0) then
        Print*, "none" !need to revise
        else
            s_Ps_calc = anti_log_Y
    END IF
  end function s_Ps_calc

  function s_Is_F1_calc(z)
    real:: s_Is_F1_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = 2.06761908721+3.0760329666*logZ
    fx   = -0.502992763686*x
    fx2  = 0.171335645235*(x**2)
    fx3  = 0.0450176963051*(x**3)
    fx4  = -0.0118964626402*(x**4)
    fx5  = 0*(x**5)
    fx6  = 0*(x**6)
    fx7  = 0*(x**7)
    fx8  = 0*(x**8)
    fx9  = 0*(x**9)
    fx10 = 0*(x**10)
    fx11 = 0*(x**11)
    fx12 = 0*(x**12)
    fx13 = 0*(x**13)

    Y = 2.52455620925+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.0674) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>=0.955)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    s_Is_f1_calc = anti_log_Y

  end function s_Is_F1_calc

  function s_Is_F2_calc(z)
    real:: s_Is_F2_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -1.94708846747+2.40697745406*logZ
    fx   = -0.384519026965*x
    fx2  = -0.0260816706301*(x**2)
    fx3  = 0.00595798753822*(x**3)
    fx4  = 0.0145445261077*(x**4)
    fx5  = -0.00663289334734*(x**5)
    fx6  = -0.00284189327204*(x**6)
    fx7  = 0.0013644816227*(x**7)
    fx8  = 0*(x**8)
    fx9  = 0*(x**9)
    fx10 = 0*(x**10)
    fx11 = 0*(x**11)
    fx12 = 0*(x**12)
    fx13 = 0*(x**13)

    Y = 1.67281645863+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.955) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    s_Is_F2_calc = anti_log_Y

  end function s_Is_F2_calc

  function s_Pr_calc(z)
    real:: s_Pr_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -0.240657322658+1.3663771922*logZ
    fx   = -2.21030870597*x
    fx2  = -0.218536586295*(x**2)
    fx3  = 0.895319589372*(x**3)
    fx4  = 0.24989009775*(x**4)
    fx5  = -0.569249436807*(x**5)
    fx6  = -0.11791682383*(x**6)
    fx7  = 0.224131161411*(x**7)
    fx8  = 0.0245620259375*(x**8)
    fx9  = -0.0455116002694*(x**9)
    fx10 = -0.0019093073888*(x**10)
    fx11 = 0.00361471193389*(x**11)
    fx12 = 0*(x**12)
    fx13 = 0*(x**13)

    Y = 3.40283217581+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.0674) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    IF (anti_log_Y==0) then
        Print*, "none" !need to revise
        else
            s_Pr_calc = anti_log_Y
    END IF
  end function s_Pr_calc

  function s_Ir_calc(z)
    real:: s_Ir_calc
    real:: logZ
    real:: x, fx, fx2, fx3
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -0.246208804814+1.33422049854*logZ
    fx   = -0.949516092853*x
    fx2  = 0.112136118689*(x**2)
    fx3  = -0.0250659183287*(x**3)


    Y = 2.70588058103+fx+fx2+fx3

    IF (Z<0.0674) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    s_Ir_calc = anti_log_Y

  end function s_Ir_calc

  function s_U_calc(z)
    real:: s_U_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13, fx14
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -0.2024225716178+1.37784223635*logZ
    fx   = -0.698029762594*x
    fx2  = 0.158916781906*(x**2)
    fx3  = 0.4438112098136*(x**3)
    fx4  = -0.113402023921*(x**4)
    fx5  = -0.369887075049*(x**5)
    fx6  = 0.129230567449*(x**6)
    fx7  = 0.19857981197*(x**7)
    fx8  = -0.0867636217397*(x**8)
    fx9  = -0.0620391900135*(x**9)
    fx10 = 0.0307482926566*(x**10)
    fx11 = 0.0102657234407*(x**11)
    fx12 = -0.00546533250772*(x**12)
    fx13 = -0.000693180974*(x**13)
    fx14 = 0.0003847494916*(x**14)

    Y = -0.06621072854+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13+fx14

    IF (Z<0.0674) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    IF (anti_log_Y==0) then
        Print*, "none" !need to revise
        else
            s_U_calc = anti_log_Y
    END IF
  end function s_U_calc

  function s_Ta_calc(z)
    real:: s_Ta_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8, fx9, fx10, fx11, fx12, fx13
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -0.202425716178+1.37784223635*logZ
    fx   = 1.35706496258*x
    fx2  = 0.052492798645*(x**2)
    fx3  = -0.196563954086*(x**3)
    fx4  = -0.0601770052288*(x**4)
    fx5  = 0.0696360270891*(x**5)
    fx6  = 0.0215297490092*(x**6)
    fx7  = -0.0161658930785*(x**7)
    fx8  = -0.00232531970294*(x**8)
    fx9  = 0.00147752067524*(x**9)
    fx10 = 0*(x**10)
    fx11 = 0*(x**11)
    fx12 = 0*(x**12)
    fx13 = 0*(x**13)

    Y = -0.0591634288046+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8+fx9+fx10+fx11+fx12+fx13

    IF (Z<0.0674) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    IF (anti_log_Y==0) then
        Print*, "none" !need to revise
        else
            s_Ta_calc = anti_log_Y
    END IF
  end function s_Ta_calc

  function s_T_f1_calc(z)
    real:: s_T_f1_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = 1.92946154068+5.25099193925*logZ
    fx   = 0.130143717675*x
    fx2  = 0.134872511954*(x**2)
    fx3  = 0.0391574276906*(x**3)
    fx4  = -0.00475933664702*(x**4)
    fx5  = -0.00428144598008*(x**5)

    Y = -0.614227603559+fx+fx2+fx3+fx4+fx5
    IF (Z<0.178) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>=1.01)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    s_T_f1_calc = anti_log_Y

  end function s_T_f1_calc

  function s_T_f2_calc(z)
    real:: s_T_f2_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5, fx6, fx7, fx8
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -2.12492525216+9.2996288611*logZ
    fx   = -0.0297944268976*x
    fx2  = 0.030632954288*(x**2)
    fx3  = 0.0183405574086*(x**3)
    fx4  = -0.0173964666211*(x**4)
    fx5  = -0.00106321963633*(x**5)
    fx6  = 0.00562060030977*(x**6)
    fx7  = 0.0001618217499*(x**7)
    fx8  = -0.0006860188944*(x**8)

    Y = 0.315409245784+fx+fx2+fx3+fx4+fx5+fx6+fx7+fx8

    IF (Z<1.01) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>=2.78)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    s_T_f2_calc = anti_log_Y

  end function s_T_f2_calc

  function s_T_f3_calc(z)
    real:: s_T_f3_calc
    real:: logZ
    real:: x, fx, fx2, fx3, fx4, fx5
    real:: Y, lower_filter, upper_filter, check_sum, filtered_result, anti_log_Y
    real, intent(in) :: Z

    logz=log10(Z)

    x    = -3.53626218091+3.46349745571*logZ
    fx   = 0.0933035304009*x
    fx2  = -0.0005849420883*(x**2)
    fx3  = -0.0022688499501*(x**3)
    fx4  = -0.00295908591505*(x**4)
    fx5  = 0.00148029868929*(x**5)


    Y = 0.686906642409+fx+fx2+fx3+fx4+fx5

    IF (Z<2.78) then
        lower_filter = 0
        else
            lower_filter = Y
    END IF

    If (Z>40.)  then
        upper_filter =0
        else
            upper_filter = Y
    End If

    check_sum = lower_filter + upper_filter

    If (check_sum == 2*Y) then
        filtered_result = Y
        else
            filtered_result = 0
    End If

    If (filtered_result==0) then
        anti_log_Y = 0
        else
            anti_log_Y = 10**Y
    End If

    s_T_f3_calc = anti_log_Y

  end function s_T_f3_calc

end
