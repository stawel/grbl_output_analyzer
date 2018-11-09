# grbl_output_analyzer
visualize grbl output signals captured by a logic analyzer

## Logic analyzer (preferred sigrok pulseView)
connect your logic analizer to `X_dir`, `X_step`, `Y_dir`, `Y_step` inputs of your stepper motor drivers and 
to `PWM_output` (laser or spindle PWM). Set sampling frequency to 1MHz.

![pulseView inputs](/example/pulseView_grbl.png)

After capturing the signal save it as `Raw binary logic data` (simple 8 bit datastream) to file: `out.bin`

![pulseView menu](/example/pulseView_menu.png)


## Visualize captured data


Run:
```
$ python display_img.py
```

this should display an image of your PWM output (yellow) where eatch pixel is one stepper step (view in full resolution for best result):

![example output](/example/display_img_output.png)
