# Repository for UC Davis Aerospace Science & Engineering Sr. Design Project

## Collaborators
* Thomas Greenhill
* Gloria Navarro
* Yihui Li
* Michael Puso
* Xuchang Tang

# Repository (Repo) Guidelines

## Creating and working from a branch
_Using branches ensures that you'll never be working on the same exact file as someone else at the same time as someone else._
1. Create your own branch by clicking "Current Branch" at the top of the desktop app. Name the branch first initial last name (i.e. TGreenhill)
1. Any time before you start coding:
    * Make sure your local files under the "main" and "FLastname" branches are both in sync with everyone else's work. 
        1. Switch to "main" as your current branch, then press "Fetch" and "Pull"
        1. Click on "Current Branch" in the desktop app, at the bottom click "Choose a branch to merge into FLastname". Choose main and click "Merge main into FLastname". 
    * Switch to your "FLastname" branch
1. While you are coding:
    * Commit to your branch often.
1. When you are done coding and you want everyone else to use your work:
    * Commit to your branch.
        - Add a brief summary of what you did (i.e. "Improved functionality of climbrate.m")
        - Add a description, your initials and date (i.e. "Added gear down option as an input to climbrate.m and modified dependent script performance.m TVG 02.01.2021")
    * Create a pull request, and someone will approve it.
        - If you want someone to review your code, just send a message on discord. 
        - You can always self-approve pull requests by going to the repo website: https://github.com/ThomasGreenhill/Sr_Design_Project/pulls


## Coding suggestions
1. Style
    - Please comment your code and add plenty of white space :P 
    - You can use MBeautify to autoformat your code if you want! If people actually use MBeautify, we can directly add it to the Repo.
1. Functions
    - Use functions, organize them in folders and put each function in its own .m file (i.e. climbrate.m has just one function inside; climbrate())
    - Inside the function mfile but before the function definition, comment in some information on the function. For example:
```matlab
%% stabderivs2ss.m
% Dimensional stability derivatives to state-space using the linear 6-DOF
% equations of motion for conventional forward flight. This model assumes
% completely decoupled longitudinal and lateral motion
%
%   Inputs:
%       Xderivs: struct of X-body axis force S&C derivatives
%       Yderivs: struct of Y-body axis force S&C derivatives
%       Zderivs: struct of Z-body axis force S&C derivatives
%       Lderivs: struct of roll axis moment S&C derivatives 
%       Mderivs: struct of pitch axis moment S&C derivatives
%       Nderivs: struct of yaw axis moment S&C derivatives
%       steady: trimmed state variables plus a couple of extra ones:
%           steady = [VTe gD game ae aT]'
%       gmi: struct of inertial properties
%           
%
%   Outputs: 
%       x: cell of state vector names
%       u: cell of control vector names
%       [A, B, C, D]: state-space matrices.
%       
%   Notes:
%       1. Stability derivatives should be dimensionalized!
%       2. game = thee - ae
%
%   History:
%       9/12/2020: Created and debugged. TVG
%

function [x, u, A, B, C, D, E] = stabderivs2ss(Xderivs, Yderivs, Zderivs,...
    Lderivs, Mderivs, Nderivs, steady, gmi)
```
1. Script Preamble:
    - Clear the workspace, close figures and clear the command line before writing your script :)
```matlab
clear; close all; clc;
```
1. Adding Paths
    - To call a function from a script while it is located in a different folder, you must add the function folder to path. For example:
```matlab
addpath("./Functions/");
```
1. Creating Directories 
```matlab
warning('off', 'all')
mkdir './Figures'
warning('on', 'all')
```
1. Figure Formatting
    - You guys can use my formatlatex() function for our design project if you want to. I'll put it under the "Utilities" folder. Call it with:
```matlab
formatlatex()
```
1. Saving Figures
    - Add this after your figure code to save it as "myfigure.jpg" within the "Figures" folder.
```
saveas(gcf,"./Figures/myfigure.jpg")
```