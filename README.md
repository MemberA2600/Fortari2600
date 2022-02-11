<h1><b>Fortari 2600</b></h1><h5><i>A new way to develop your own Atari 2600 games</i></h5>
<img src="https://www.pngkit.com/png/full/222-2221121_all-things-printed-recorded-atari-2600.png" alt="Atari2600" width=75%> 
 
<h3><u>I. Introduction</u></h3>
<p align="justify">The Atari 2600. This is the main reason I left my original life as a social worker and became a developer. It's so simple, yet hard to master. It's bulky, but you have full control and only your skills can define what you can do with it.</p>
<p align="justify">We all know that with all these retro consoles, you have to be familiar with the CPU's byte codes and also the registers where the other chips can find the data they work with it and back in their golden era, that was it.</p>
<p align="justify">The Atari 2600 was not different. For a long time, the only way to make you own games was via 6502 asm and DASM.</p>

<p align="justify">In 2007, Batari Basic came and changed this situations. Most of the fans had some experience with old 8bit computers, so they propably knew Basic as I was messing around with my Commodore 64 as a kid. Batari Basic was simple, I could handle many bankswithcing methods, had two kind of kernels to offer (one customizable one with two sprites and one really static with 1 + 5 sprites).</p>
<p align="justify">Batari Basic was really sequential, so the only way to change the flow of the code was via goto, you only had really simple if-then-else statements and it wasted the ROM since it couldn't manage the sprite and playfield data, just copied it over and over it you tried to use it twice. But it had a nice, simple playfield and sprite editor, also a really, I mean, really basic music editor.</p>
<p align="justify">So, what did bB offer?</p>
<ul>
<li>Many cartridge formats (up to the 64K EF with SARA support)</li>
<li>Some basic edit tools</li>
<li>A really "basic Basic"</li>
<li>One customizable 2 sprites kernel</li>
<li>One multisprite kernel</li>
<li>The option to include a mini kernel to place items under the game screen and also a partion of vblank</li>
<li>A really "basic Basic"</li>
<li>A titlescreen editor (supporting only one screen)</li>
</ul>
<p align="justify"><a href = "https://github.com/batari-Basic/batari-Basic">Access batari Basic project here</a></p>
<p align="justify">The other option is the CDFJ bankswitching + Melody cartridge. This hold a different philosophy, from professionals for professionals.</p>
<p align="justify">CDFJ is ARM based, supports 32k cartridges with Bus Stuffing and has a clear structure, where you have six banks for C code and 4K for 6507 assembly.
<p align="justify"><a href = "https://atariage.com/forums/topic/297759-part-1-cdfj-overview/">Access CDFJ project here</a></p>
</p>
<img src="https://github.com/MemberA2600/Fortari2600/blob/master/others/img/Loading.png" alt="Fortari Logo" width=75%> 
<h3><u>II. What is Fortari and why another one?</u></h3>
<p align="justify">I had a different phylosophy in mind. CDFJ really want to expand the consoles power by adding the arm support in the cartridge, while bB tries to be the Basic you would expect for the console in the early 80s.</p>
<u><h4>What can be said about Fortari in short:</h4></u>
<ul>
<li>It's heavily based on projects. First, you create a new project that has a fixed structure and from the editor, you access parts (the code is also seperated into units) and your resources (sprites, playfield, backgrounds, music data, etc.) are placed in the dedicated folders. (for example, bB is based around single code files)</li> 
<li>Mostly it works as an engine instead of being an IDE, so it's close to Unity in the way it's implemented. You have tools to manage the memory, create resources, convert files, etc.</li>  
<li>Mostly it works as an engine instead of being an IDE, so it's close to Unity in the way it's implemented. You have tools to manage the memory, create resources, convert files, etc.</li> 
<li>Fortari supports the 32k ROM + SARA superchip addon only. That means the code has 8 of 4K banks and 128 extra bytes of RAM. Bank1 has the game engine and the graphics data for the game section. Bank2 to Bank8 you have the same concept, Bank8 is different in the way it has the VBLANK section used by the game engine.</li> 
<li>The structure how you should design your game is based on the bank structure. One bank can contain a screen (titlescreen, gameover, a kind of level, the shop, etc.) with it's enter and leave section, it's own vblank code (not much, since a lot of calculations happen there to arrange game objects, overscan code (basically your game code) and your screentop and screenbottom elements. These have their data stored in the bank, as well the routines you include in your code.</li>
<li>Banks can have music or wave data instead of being a screen type. Music can take up to two banks while wave is limited to one. Music can be initialized, stopped and resumed during the gameplay, while the data itself is accessed at the end of overscan. Playing a wave will perform the wave playback, while all the game elements are disabled and returns to the point.</li> 
<li>Fortari has 3 levels of memory handling: Global, Bank and Subroutine. You cannot overwrite a global address with a bank one. Global and Bank memory addresses are handled in the Memory Manager, global variables are assigned to Bank1. There are 4 types of variables: bit, doublebit, nibble and byte. Also, you can create iterable pointer arrays to manage more variables with shorter code.</li> 
<li>Fortari supports subroutines and functions, they can be accessed from their own banks. This works with imported routines as well.</li> 
<li>There is no goto. Organize your code into functions and subroutines, believe me, it's a lot better.</li> 
<li>The environment have some "fake OOP" so you can access the game objects easier (like, playfield%color for setting the color of the pf)</li> 
</ul>
<h3><u>III. Development Machine and Utilites</u></h3>
The program is developed on a B350 + Ryzen5 2600 machine, with 32 GB RAM. I use a Sapphire 2600 XT for display (yeah, a little too much of 2600, you say?), using Windows 7 (in 2022 :D )

<p align="justify">Right now, there is no built version of the application since it is in a very early state. The program is built around Python 3.7 and Fortran 90, the Fortran applications are built since that's the easiest way to use them from Python.</p>

<h5>Applications included (not written by me):</h5>
<ul>
<li><a href="https://github.com/Malvineous/dro2midi">dro2midi</a> - Used to convert DosBox dump files to midi.</li> 
<li><a href="https://github.com/s-macke/SAM">sam</a> - This one is used to generate S.A.M. sound for wave generation</li> 
<li><a href="https://www.pouet.net/prod.php?which=56322">sid2midi</a> - If the python module fails, this one takes it's place.</li> 
<li><a href="https://vgmrips.net/wiki/VGM_Tools">vgm2mid</a> - Not used during the process, but you can convert your vgm to midi, then import that one</li> 
<li><a href="https://github.com/vgmrips/vgmtools/blob/master/vgm2txt.c">vgm2txt</a> - The VGM converter gets the databytes thru this program</li> 
</ul>

<h3><u>IV. Parts those are ready to go:</u></h3>
<ul>
<li><b>Project Manager:</b>
   <ol>
     <li>Create Project</li>
     <li>Open Project</li>
     <li>Save Project Part</li>
     <li>Save Whole Project</li>
   </ol>
 </li>
 <li><b>Memory Manager:</b>
   <ol>
     <li>Allocate Memory</li>
     <li>Create Pointer Arrays</li>
     <li>Manages Memory Locks</li>
   </ol>
 </li>
  <li><b>Playfield Editor:</b>
   <ol>
     <li>Draw a 0-255 tall playfield (the 4 pixels on each side are non-mirrored)</li>
     <li>Background and playfield can be colored line-by-line</li>
     <li>Converts images to a pf / bg combo</li>
     <li>Interactive testing</li> 
   </ol>
 </li>
   <li><b>Sprite Editor:</b>
   <ol>
     <li>Draw a 0-255 tall sprite, up to 15 frames</li>
     <li>The limitation is 255 bytes, so sprites taller than 17 points can't have 15 frames</li>
     <li>Player sprites can be colored line-by-line (submenu icons have gradient based on one color)</li>
     <li>Can be used for player sprites or for submenu icons</li>
     <li>Interactive testing (with choosen pf and bg)</li>
   </ol>
 </li>
    <li><b>Music Composer:</b>
   <ol>
    <li>Creates a semi-4 channel display</li>
    <li>Emulated TIA sound playback on keypress</li>
    <li>Interactive testing + Generating stand alone music ROMs</li>
    <li>Conversion of the following music formats:</li>
       <ul>
       <li>General Midi</li>
       <li>Commodore 64 SID file (converted to midi first)</li>
       <li>DRO, RDOS, IMF (converted to midi first)</li> 
       <li>Adlib VGM files</li> 
       </ul>
   </ol>
 </li>
  <li><b>64px Editor:</b>
   <ol>
     <li>Converts most of the known picture formats</li>
     <li>Let you edit the picture before saving</li>
     <li>The format has 64 pixels of sprites and one mirrored pf in the middle</li>
     <li>3 unique colors for each line</li>
   </ol>
 </li>
   <li><b>Sound Player:</b>
   <ol>
     <li>Converts wave to 4bit sample for the VCS</li>
     <li>You have three methods:</li>
       <ul>
       <li>Open Wave File</li>
       <li>Record your own sound</li>
       <li>Generate a speech sound with S.A.M.</li> 
       </ul>
   </ol>
 </li>
</ul>
