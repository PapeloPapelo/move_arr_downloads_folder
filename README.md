For Windows/NFTS.
_____________________________________________________________________________________________________
Assumptions: 

-One Drive has both, a '/Torrent/Movies' and a '/Media/Movies' folder as recommended by *arr guides.

-The '/Media' folder contains the cleaned up movies, Hardlinked by *arr. All movies/files which are not Hardlinked will be copied, make sure that *arr has processed all movies before running the script.

_____________________________________________________________________________________________________
<b> Goal </b> of the script is to move the '/Torrents' folder to another Drive without copying the full sized movies but instead creating symlinks for them,
and only copy small non hardlinked, non movie files aka bloat to the destination drive / folder.

Afterwards you can point QBIT to the new Drive and keep seeding while the old drive won't have any bloat anymore. Old drive of course needs to run in order to seed.
New Drive can be much smaller since no full sized movies will be copied. Which should allow to have the bloat of multiple drives combined into one seed / bloat drive.

_____________________________________________________________________________________________________

1. Start script as Admin, needed to create Symlinks.

2. Pick source location e.g. H:\Torrents
3. Pick empty destination location e.g. J:\Torrents, for hardlinked files symlinks will be created, all other files will be copied
   
   Watch the copy process in the cmd, if it slows down or seems to copy large files look at the destination what is being copied,
   you might have missed to import a movie with *arr (not hardlinked thats why its being copied), if so interrupt the process Ctrl+C, delete the copied folder (destination) or at least the one big file you missed,    handle the import of the movie with *arr then run it again.

5. Point Q-Bit to new bloat drive / destination location
6. Test if it works

7. If it works, source location (H:\Torrents) can be deleted, only H:\Media with cleaned names should remain.

Info: As long as one Hardlink remains the file will exist.
