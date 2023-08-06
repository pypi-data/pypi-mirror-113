
python gwemopt_run --doEfficiency --telescopes ZTF --doSchedule --doSkymap --doPlots --modelType file --lightcurveFiles  '../lightcurves/Bulla_mejdyn0.005_mejwind0.010_phi45_45.6.dat' --skymap '../data/Leo/23_flatten.fits' --gpstime 1013336748  -o ../output/O4/23.0/ZTF_-16.25_bulla1 --doTiles --doSingleExposure --filters g,r --exposuretimes 20.0,20.0 --powerlaw_cl 0.900 --do3D --doAlternatingFilters --doBalanceExposure --Tobs 0.0,1.0 --timeallocationType absmag --absmag -16.25

