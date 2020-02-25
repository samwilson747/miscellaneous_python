import re, argparse
import sys
import matplotlib.pyplot as plt
import plistlib
import numpy as np

def plot_stats(fileName):
    #read in playlist
    plist = plistlib.readPlist(fileName)

    #get tracks from playlist
    tracks = plist['Tracks']
    #print(tracks)
    #create lists of song ratings and track durations
    sizes = []
    track_ids = []
    #iterate through tracks
    for track_id, track in tracks.items():
        #print(track_id)
        #print('done')
        #print(track['Track ID'])
        try:
            sizes.append(track['Size'])
            tack_ids.append(track['Track ID'])
        except:
            #ignore
            pass
    #ensure valid data was collected
    #if sizes == [] or track_ids == []:
        #print('No valid album rating / total time data in %s' % fileName)
        #return
    #with valid data, create scatter plot
    x = np.array(sizes, np.int32)
    #convert to minutes
    x = x/60000.0
    y = np.array(track_ids, np.int32)

#plotting collected data based on size and id number
    plt.subplot(2,1,1)
    plt.plot(x,y,'o')
    plt.axis([0,1.05*np.max(x), -1,110])
    plt.xlabel('Track sizes')
    plt.ylabel('Track ids')

    #plot histogram
    plt.subplot(2,1,2)
    plt.hist(x,bins=20)
    plt.xlabel('Track sizes')
    plt.ylabel('Count')

    #show plot
    plt.show()

def find_duplicates(fileName):
    #find duplicates in a given playlist
    print("finding duplicage tracks in %s..",fileName)

    play_list = plistlib.readPlist(fileName)
    tracks = play_list['Tracks'] #parse data tagged 'Tracks'
    track_names = {} #dictionary for parsed tracks

    for track_id, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            #check if entry exists already in the dictionary
            if name in trackNames:
                if duration//1000 == trackNames[name][0]//1000: #are the duration within the nearest second
                    count = track_names[name][1]
                    track_names[name] = (duration, count+1)
            else: #add to dictionary as new tuple
                track_names[name] = (duration,1)
        except:
            #ignore data that cannot be opened
            pass
    #store duplicates as (name, count) tuples
    dups = []
    for k, v in track_names.items():
        if v[1] > 1:
            dups.append((v[1], k))
    #save tuples to file
    if len(dups) > 0:
        print("found %d duplicates. track names saved to dup.txt" %len(dups))
    else:
        print("no duplicates found")
    f = open('duplicates.txt','w')
    for val in dups:
        f.write("[%d] %s\n"% (val[0],val[1]))
    f.close()

def main():
    #create xml parser
    descStr = """
    This program analyzes playlist files (.xml) exported from itunes
    """
    parser = argparse.ArgumentParser(description=descStr)

    #add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    #add expected groups
    group.add_argument('--common', nargs='*', dest='plFiles',required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD',required=False)
    #parse args
    args = parser.parse_args()

    #if args.plFiles:
        #find common tracks
        #find_common_tracks(args.plFiles)
    if args.plFile:
        plot_stats(args.plFile)
    else:
        print('these were not the tracks you were looking for')

if __name__ == '__main__':
    main()
