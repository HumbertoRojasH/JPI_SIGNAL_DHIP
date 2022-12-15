import pandas as pd
from eqsig.single import AccSignal

class Data:
    file = None
    acc = None
    df_nw = None

    def baseline_filtering(self):
        self.acc_signal_2 = AccSignal(self.acc[0:self.n]*self.fac,self.dt,smooth_freq_range=(0.01, (1/self.dt)/2))
        if Data.fil:
            self.acc_signal_2.butter_pass(cut_off=(self.frq1,self.frq2))
        else:pass

        if Data.bl == True:
            if self.type == "Linear":
                degree = 1
            elif self.type == "Quadratic":
                degree = 2
            elif self.type == "Cubic":
                degree = 3
            self.acc_signal_2.remove_poly(poly_fit=degree)
        else:pass

        self.df_c = pd.DataFrame()
        self.acc_signal_2.generate_displacement_and_velocity_series()
        self.df_c["Time"] = self.acc_signal_2.time
        self.df_c["Acc"] = self.acc_signal_2.values
        self.df_c["Vel"] = self.acc_signal_2.velocity
        self.df_c["Dis"] = self.acc_signal_2.displacement
