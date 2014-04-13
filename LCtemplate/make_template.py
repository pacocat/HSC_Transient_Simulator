#!/opt/local/bin/python"""# Written by Jun E. Okumura in 2014.02# contact paco.sci@gmail.com if you have any questions or comments.This code extends light curves generated by "lc_calculator.py".## NOTE ##To run this code, numpy should be installed. The author used version '1.8.0'See http://www.numpy.org/ if you do not have numpy."""import numpy as np### options ###camera_type = 0# [0:SC 1:HSC]object_type = 6# 0:SN Ia (Hsiao) 1:SN Ia (Nugent) 2:SN Ia-91bg (Nugent) 3:SN Ia-91T (Nugent)# 4:SN Ibc (Nugent) 5:SN IIL (Nugent) 6:SN IIP (Nugent) 7:SN IIn (Nugent)mlim = 30.0 # mag# the variable mlim is set to define the darkest edge of light curve.# In the author's template, mlim = 30 is set-uped. # For future deep survey, I suggest mlim larger than 30 mag. # set up directory nameif object_type == 0: targetdir = 'Hsiao_Ia'elif object_type == 1: targetdir = 'Nugent_Ia'elif object_type == 2: targetdir = 'Nugent_Ia91bg'elif object_type == 3: targetdir = 'Nugent_Ia91T'elif object_type == 4: targetdir = 'Nugent_Ibc'elif object_type == 5: targetdir = 'Nugent_IIL'elif object_type == 6: targetdir = 'Nugent_IIP'elif object_type == 7: targetdir = 'Nugent_IIn'else: print 'Please set correct number for \'object_type\':0-6'camera_name = 'SC' if camera_type == 0 else 'HSC'bands = ['B','V','R','i','z'] if camera_type == 0 else ['g','r','i','z','y']def lc_extrapolation_coefficient(x, y0, y1):    """    This function calculate the coefficient (a,b) for liniar extrapolation:    y = a*x + b    input parameters are:    - 1st argument: array [the last day, n-days before the last day]    - 2nd argument: array [5-band magnitudes at the last day]    - 3rd argument: array [5-band magnitudes at n-days before the last day]    'n' can be defined when you call this subroutine. For example, if you input [data[-1,0], data[-6,0]]    as 1st argument, this means n = 5.    """    co_a = (y0-y1)/(x[0]-x[1])    co_b = (y1*x[0]-y0*x[1])/(x[0]-x[1])    return co_a, co_b# start making template light curvesprint 'extrapolating %s SN %s templates in ./%s/%s/' % (targetdir.split('_')[0], targetdir.split('_')[0], camera_name, targetdir)for z in np.arange(0.0,2.01,0.05):    print 'making light curve template at z=%.2f' % (z)    # load light curve at redshift z    data = np.loadtxt('./%s/%s/z%03d.dat' % (camera_name,targetdir,z*100.1))    if camera_type == 0:        imax = min(data[:,19]) # maximum magnitude in i-band        # the day of max in i-band. Usually SN have different day of max for different filter.         # In this code, template's 0-day is defined from i-band because SXDS SN search is based on i-band.        daymax = data[np.where(data[:,19]==imax)[0][0]][0]    else:        imax = min(data[:,18])        daymax = data[np.where(data[:,18]==imax)[0][0]][0]    # open output files '_ext' represents extraporated light curve,    # and '_norm' represents normalized light curve.    # '_ext_norm' template is also corrected for day of i-band max to be 0.    fout_ext = open('./%s/%s/z%03d_ext.dat' % (camera_name,targetdir,z*100.1),'w')    fout_ext_norm = open('./%s/%s/z%03d_ext_norm.dat' % (camera_name,targetdir,z*100.1),'w')    # write header    fout_ext.write('#1 observer-frame phase [day]\n#2 %s %s mag (AB)\n#3 %s %s mag (AB)\n#4 %s %s mag (AB)\n#5 %s %s mag (AB)\n#6 %s %s mag (AB)\n' \    % (camera_name, bands[0], camera_name, bands[1], camera_name, bands[2], camera_name, bands[3], camera_name, bands[4]))    fout_ext_norm.write('#1 observer-frame phase [day]\n#2 %s %s mag (AB)\n#3 %s %s mag (AB)\n#4 %s %s mag (AB)\n#5 %s %s mag (AB)\n#6 %s %s mag (AB)\n' \    % (camera_name, bands[0], camera_name, bands[1], camera_name, bands[2], camera_name, bands[3], camera_name, bands[4]))    fout_ext.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (-200.0, mlim, mlim, mlim, mlim, mlim))    fout_ext.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (data[0,0], mlim, mlim, mlim, mlim, mlim))    fout_ext_norm.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (-200.0, mlim-imax, mlim-imax, mlim-imax, mlim-imax, mlim-imax))    fout_ext_norm.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (data[0,0]-daymax, mlim-imax, mlim-imax, mlim-imax, mlim-imax, mlim-imax))    # load each row    for i in range(1,len(data)):        # fill mlim if magnitude is fainter than mlim        mag = data[i,16:21]        # for j in range(5):        #     if mag[j] > mlim: mag[j] = mlim         fout_ext.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (data[i,0], mag[0], mag[1], mag[2], mag[3], mag[4]))        fout_ext_norm.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' \        % (data[i,0]-daymax, mag[0]-imax, mag[1]-imax, mag[2]-imax, mag[3]-imax, mag[4]-imax ))    # start extrapolation    # co_a and co_b are the coefficient for linear extrapolation:    # y = co_a * x + co_b    if targetdir.split('_')[1] in ['IIL', 'IIP']:        co_a, co_b = lc_extrapolation_coefficient([data[-1,0], data[-2,0]], data[-1,16:21], data[-2,16:21])    else:        co_a, co_b = lc_extrapolation_coefficient([data[-1,0], data[-6,0]], data[-1,16:21], data[-6,16:21])    # daylim is the day which light curve become equivalent with mlim    daylim = np.array([0.0, 0.0, 0.0, 0.0, 0.0])    for i in range(5):        daylim[i] = (mlim-co_b[i])/co_a[i] if co_a[i]!=0.0 else data[-1,0]    # sort daylim and output magnitudes for each daylim    daylim_index = np.argsort(daylim)    for j in daylim_index:        # in the condition below, additional -0.5 is added so that all daylim[j]        # can be captured. Otherwise, sometime the code miss the 'daylim[j] == data[-1,0]' cases.        if (daylim[j] > data[-1,0]-0.5):            mag = [0.0, 0.0, 0.0, 0.0, 0.0]            for i in range(5):                mag[i] = co_a[i] * daylim[j] + co_b[i]                if mag[i] > mlim: mag[i] = mlim            fout_ext.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (daylim[j], mag[0], mag[1], mag[2], mag[3], mag[4]))            fout_ext_norm.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (daylim[j]-daymax, mag[0]-imax, mag[1]-imax, mag[2]-imax, mag[3]-imax, mag[4]-imax))        else:            fout_ext.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (data[-1,0], data[-1,16], data[-1,17], data[-1,18], data[-1,19], data[-1,20]))            fout_ext_norm.write('%7.3f %7.4f %7.4f %7.4f %7.4f %7.4f\n' % (data[-1,0]-daymax, data[-1,16]-imax, data[-1,17]-imax, data[-1,18]-imax, data[-1,19]-imax, data[-1,20]-imax))    fout_ext.close()    fout_ext_norm.close()print 'That\'s all forks!'