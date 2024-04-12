clear,clc
%Datos Constantes
t = 0.10;
q = 15:10:95;
phi = 0.90;
eu = 0.003;
et = 0.005;
%Datos Variables
b_min = 200; b_max = 400;
b = b_min:25:b_max;
fc = 20:7:40;
fy = 400;
Mu = 100:20:2000;

%Matrices vacías
B = [] ; FC = [] ; MU = []; Q = [];
P_OPT =[] ; R_OPT = [] ; D_OPT = [] ; AS_OPT = []; A_S_OPT = [];

%Calculando
for z = 1:length(q)
    for i = 1:length(b)
        for j = 1:length(fc)
            for k = 1:length(Mu)
                %Almacenamiento de los Datos de Entrada
                B = [B,b(i)];
                FC = [FC,fc(j)];
                MU = [MU,Mu(k)];
                Q = [Q,q(z)];
                %Cálculo del Beta 1
                if fc(j)>=17 & fc(j)<=28
                    beta1 = 0.85;
                else
                    if fc(j)>28 & fc(j)<55
                        beta1 = 0.85-0.05*(fc(j)-28)/7;
                    else
                        if fc(j)>=55
                            beta1 = 0.65;
                        end
                    end
                end

                %Límites
                    %Cuantía Mínima
                    p1 = max(1.4/fy,0.25*sqrt(fc(j))./fy);
                    Ru = 1./sqrt(p1.*fy*(1-p1*fy./(1.7*fc(j))));
                    %Cuantía Máxima
                    pu = 0.85*beta1*fc(j)*eu/(fy*(eu+et));
                    R1 = 1./sqrt(pu.*fy*(1-pu*fy./(1.7*fc(j))));
                %Resultados Óptimos
                p_opt = (pu*q(z)*(pu*fy/(0.425*fc(j))-(3+t))+(1-t)*(1+t))/(2*q(z)*(1-t));
                R_opt = 1./sqrt(fy*(pu*(1-pu*fy/(1.7*fc(j)))+p_opt*(1-t)));
                if p_opt>p1 & p_opt<pu
                    p_opt = p_opt;
                    R_opt = R_opt;
                else
                    if p_opt<=p1
                        p_opt = p1;
                        R_opt = Ru;
                    else
                        if p_opt>=pu
                            p_opt = pu;
                            R_opt = R1;
                        end
                    end
                end
                P_OPT = [P_OPT,p_opt];
                R_OPT = [R_OPT,R_opt];

                d_opt = R_opt*sqrt((Mu(k)/phi)/b(i));
                D_OPT = [D_OPT,d_opt*100];
                As_opt = (pu+p_opt)*b(i)*d_opt;
                AS_OPT = [AS_OPT,As_opt*10];
                A_s_opt = p_opt*b(i)*d_opt;
                A_S_OPT = [A_S_OPT,A_s_opt*10];
            end
        end
    end
end

DATA = horzcat(Q',B',FC',MU',P_OPT',R_OPT',D_OPT',AS_OPT',A_S_OPT');
Resumen = table(Q',B',FC',MU',P_OPT',R_OPT',D_OPT',AS_OPT',A_S_OPT');
Resumen.Properties.VariableNames = {'q','b (mm)','fc (MPa)','Mu (Kn.m)','p_opt','R_opt','d_opt (cm)','As (cm^2)','A_s (cm^2)'};

writetable(Resumen, 'miArchivo_v6.xlsx');