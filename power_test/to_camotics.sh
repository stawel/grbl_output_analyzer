
cat $1 | sed 's/^\(X.*\)S\(.*\)/Z0.\2\n\1/' > gcode_camotics.gcode

camotics gcode_camotics.gcode
