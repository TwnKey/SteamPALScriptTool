Set of scripts to extract/reinsert dialogs from/to Chinese Paladin: Sword and Fairy.
# Instructions
## How to extract dialogs from the script files
The game stores the dialogs inside "talk.dat" files (located inside the game directory).  
You can extract the dialogs into a .csv file using the command  

`python PALDecomp.py <original talk.dat file path>`
  
The resulting file will contain the original dialog written in simplified chinese in the first column.  
The second column contains your translation.  
The next columns depend on the type of instruction used for the dialog. They hold the parameter values for each instruction. Things like the X position of the text, the Y position are written. The only value you might need to change is the maximum number of characters per line, which is 32 by default. You might want to increase it to make use of all the space available in the dialog box.
  
![image](https://user-images.githubusercontent.com/69110695/227636604-8f349c38-f393-4cd7-b40f-b0bdbfd177bd.png)

  
## How to reinsert dialogs from the csv files
Once the dialogs have been translated, you can run the following command:  

`python.exe PALRecomp.py <csv file containing your translations> <original talk.dat file used for the csv generation>`
  
and finally put the generated .dat file into the game directory (replace the name of the output .dat file accordingly)

# Demo
https://www.youtube.com/watch?v=3_FYB_OnEYk

# Custom letters
If you want to add language specific letters such as à é è, you will have to replace existing letters in the Resources/CS.ttf font file with your letters, then recompile your csv into a .dat applying a custom encoding that will do the mapping.
This is done as follows:
- First find letters in your .ttf font that you don't plan to use and which exists in the big5 encoding (see http://ash.jp/code/cn/big5tbl.htm); basically just pick random chinese characters in those tables, and write their corresponding encoding (example: 世 is A540)
- Use a tool like FontForge to copy the drawing of your letter é, à, etc, in the slot of your target big5 characters chosen in the previous step. Characters are ordered in unicode order in fontforge and you can jump to a specific unicode. unicode for 世 is 4E16 as indicated here https://www.compart.com/en/unicode/U+4E16
- Generate your ttf file and place the ttf in the Resources directory, replacing the base game one.
- Finally in the script CustomCodec.py, add the mapping between your desired character (for example, é) and the encoding it will take (A540) like in the picture below:  
![image](https://user-images.githubusercontent.com/69110695/227640333-88c87e17-8c71-489f-ae29-a9f9b9eaba35.png) 
- Recompile your scripts
