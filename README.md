# OptionsAnalyzer

Always improving.  Built for python 3.5+

Short program that will allow up to 8 options legs and show profit/loss graph for all entered.  Utilizes Black-Scholes modeling from mibian.  Symbols are based on YAHOO Finance symbol list.<br>
Index symbols can be mapped as follows:<br>
{"DJIA":"^DJI", "SPX":"^GSPC", "NDX":"^NDX", "RUT":"^RUT", "VIX":"^VIX"}

Number of legs is scalable if you wish to download.  Simply add another leg after line 78, include a new row as an argument, and also add the leg to line 101.  Limited by screen size for myself.

Currently in the works...looking for suggestions... Looking for a better way to calculate each individual line.  Recalculates the entire system each time "Calculate" is pressed.  Would like to be able to check if/what data has changed and only recalculate based on that.  i.e. change days forward, only 1 line needs to be recalculated, others are the same.
