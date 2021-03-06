double form_volume(double req_minor, double req_major, double rpolar);
double Iq(double q, double sld, double solvent_sld,
    double req_minor, double req_major, double rpolar);
double Iqxy(double qx, double qy, double sld, double solvent_sld,
    double req_minor, double req_major, double rpolar, double theta, double phi, double psi);

double form_volume(double req_minor, double req_major, double rpolar)
{
    return 1.333333333333333*M_PI*req_minor*req_major*rpolar;
}

double Iq(double q,
    double sld,
    double solvent_sld,
    double req_minor,
    double req_major,
    double rpolar)
{
    // if (req_minor > req_major || req_major > rpolar) return NAN;  // Exclude invalid region

    double sn, cn;
    // translate a point in [-1,1] to a point in [0, 1]
    const double zm = 0.5;
    const double zb = 0.5;
    double outer = 0.0;
    for (int i=0;i<76;i++) {
        //const double cos_alpha = (Gauss76Z[i]*(upper-lower) + upper + lower)/2;
        const double x = 0.5*(Gauss76Z[i] + 1.0);
        SINCOS(M_PI_2*x, sn, cn);
        const double acosx2 = req_minor*req_minor*cn*cn;
        const double bsinx2 = req_major*req_major*sn*sn;
        const double c2 = rpolar*rpolar;

        double inner = 0.0;
        for (int j=0;j<76;j++) {
            const double ysq = square(Gauss76Z[j]*zm + zb);
            const double t = q*sqrt(acosx2 + bsinx2*(1.0-ysq) + c2*ysq);
            const double fq = sph_j1c(t);
            inner += Gauss76Wt[j] * fq * fq ;
        }
        outer += Gauss76Wt[i] * 0.5 * inner;
    }
    // translate dx in [-1,1] to dx in [lower,upper]
    const double fqsq = outer*zm;
    const double s = (sld - solvent_sld) * form_volume(req_minor, req_major, rpolar);
    return 1.0e-4 * s * s * fqsq;
}

double Iqxy(double qx, double qy,
    double sld,
    double solvent_sld,
    double req_minor,
    double req_major,
    double rpolar,
    double theta,
    double phi,
    double psi)
{
    // if (req_minor > req_major || req_major > rpolar) return NAN;  // Exclude invalid region

    double stheta, ctheta;
    double sphi, cphi;
    double spsi, cpsi;

    const double q = sqrt(qx*qx + qy*qy);
    const double qxhat = qx/q;
    const double qyhat = qy/q;
    SINCOS(theta*M_PI_180, stheta, ctheta);
    SINCOS(phi*M_PI_180, sphi, cphi);
    SINCOS(psi*M_PI_180, spsi, cpsi);
    const double calpha = ctheta*cphi*qxhat + stheta*qyhat;
    const double cnu = (-cphi*spsi*stheta + sphi*cpsi)*qxhat + spsi*ctheta*qyhat;
    const double cmu = (-stheta*cpsi*cphi - spsi*sphi)*qxhat + ctheta*cpsi*qyhat;
    const double t = q*sqrt(req_minor*req_minor*cnu*cnu
                          + req_major*req_major*cmu*cmu
                          + rpolar*rpolar*calpha*calpha);
    const double fq = sph_j1c(t);
    const double s = (sld - solvent_sld) * form_volume(req_minor, req_major, rpolar);

    return 1.0e-4 * square(s * fq);
}

