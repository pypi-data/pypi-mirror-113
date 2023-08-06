
python gwemopt_run --doEfficiency --telescopes ZTF --doSchedule --doSkymap --doPlots --modelType file --lightcurveFiles  '../lightcurves/Bulla_mejdyn0.005_mejwind0.010_phi45_45.6.dat' --skymap '../data/Leo/86_flatten.fits' --gpstime 1016751410  -o ../output/O4/86.0/ZTF_-14.0_bulla1 --doTiles --doSingleExposure --filters g,r --exposuretimes 20.0,20.0 --powerlaw_cl 0.900 --do3D --doAlternatingFilters --doBalanceExposure --Tobs 0.0,1.0 --timeallocationType absmag --absmag -14.0

python gwemopt_run --doEfficiency --telescopes ZTF --doSchedule --doSkymap --doPlots --modelType file --lightcurveFiles '../lightcurves/Bulla_mejdyn0.005_mejwind0.010_phi45_45.6.dat' --skymap '../data/Leo/86_flatten.fits' --gpstime 1016751410 -o ../output/O4/86.0/ZTF_590.0_bulla1 --doTiles --doSingleExposure --filters g,r --exposuretimes 590.0,590.0 --powerlaw_cl 0.900 --do3D --doAlternatingFilters --doBalanceExposure --Tobs 0.0,1.0 --scheduleType greedy_slew

