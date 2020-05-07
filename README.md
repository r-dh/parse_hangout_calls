# Parse Hangout calls

Two simple Python scripts to extract and plot call data out of the Hangouts.json takeout file.

## Requirements

- bokeh
- pandas

Retrieve your Hangouts data here: https://takeout.google.com/settings/takeout

## Usage

Place the Hangouts.json file in the directory, then execute

```
python parse_data.py -n CONTACTNAME
```

or

```
python parse_data.py -i
```

This will generate a json file `hangout_calls_CONTACTNAME.json`



Plot the data using this file:

```
python plot_data.py -f hangout_calls_CONTACTNAME.json
```

The frequency can be adjusted to H, D, W, M,  Y

```
python plot_data.py -f hangout_calls_CONTACTNAME.json --frequency W
```



## Examples

Default setting, by day:
![bokeh_plot_day](.\examples\bokeh_plot_day.png)

Week:
![bokeh_plot_week](.\examples\bokeh_plot_week.png)

Month:
![bokeh_plot_month](.\examples\bokeh_plot_month.png)

