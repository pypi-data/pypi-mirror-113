# mod_est.py - Moderation Estimates UI, rcampbel, March 2021
#from IPython.core.debugger import Pdb; Pdb().set_trace() # breakpoint

import functools
import ipywidgets as ipyw
from superpower_gui.views.mod_plot import ModerationPlot
from .mod_land import *

PROPORTIONS = 'Proportions of categorical variables:'
PROP_WARN = 'Warning: Proportions must sum to 1'
SD_LABEL = 'SDs:'
LATEX_NSUBT = '$N_{T}$'
UNICODE_SUBZERO = u'₀'
SIMPLE_SLOPES_AND_EFFECTS = 'Simple Slopes and Effects'
LOW = 'Low'
HIGH = 'High'
LC_LOW = 'low'
LC_HIGH = 'high'
SEP = ', '
LOW_HIGH = [LOW, HIGH]
PLOTS_DISABLED = '(Power custom effects)'  # TODO Finalize no-plots text
SIMPLE_EFFECT_OF_3 = 'Simple effect of %s on %s at %s'
SIMPLE_EFFECT_OF_4 = 'Simple effect of %s on %s at %s with %s'
SLOPE = ', slope = '


class PredValue:
    """Store a numeric value and associated info for a predictor or predictor level"""

    def __init__(self, value, pred, level=None):
        self.value = value
        self.pred = pred
        self.level = level

    def __str__(self):
        return str(self.value)

    def dump(self):
        if self.level is None:
            return self.pred.name.value + '=' + str(self.value)
        else:
            return self.pred.levels[self.level].value + '=' + str(self.value)


class Calculator:
    """Compute moderation values"""

    def __init__(self, out, land):
        self.out = out  # Output area for debugging
        self.land = land
        self.possible_values = {}  # Dict of PredVals (as lists), index by pred (a Variable)
        self.out.clear_output()

    def debug(self,str,end='\n'):
        with self.out:
            print(str,end=end)

    def clear_debug(self):
        self.out.clear_output()

    def build_possible_values(self):
        """Generate possible pred values"""
        self.possible_values = {}

        for pred in self.land.predictors[:self.land.num_pred.value]:
            possible = []

            if pred.type.value == CONT:  # Continuous
                    possible = [PredValue(-1,pred),PredValue(1,pred)]
            elif pred.count.value == 2:  # Categorical, dichotomous
                    possible = [PredValue(0,pred),PredValue(1,pred)]
            else: # Categorical, non-dichotomous: 0 and 1 for each level

                # TODO Confirm n vs n-1 (see below)

                #for i in range(pred.count.value-1):
                #    # Note: Below, a "-1" for i, and another "-1" to skip 1st level
                #    possible.append(([PredValue(0,pred,i)] * i) + [PredValue(1,pred,i)] + ([PredValue(0,pred,i)] * (pred.count.value - i - 1 - 1)))

                for i in range(pred.count.value):
                    # Note: Below, a "-1" for i
                    possible.append(([PredValue(0,pred,i)] * i) + [PredValue(1,pred,i)] + ([PredValue(0,pred,i)] * (pred.count.value - i - 1)))

            self.possible_values[pred] = possible

    def calculate(self, b0, plot, line_num, point_num):
        """Use moderation equation to calculate plot point (x,y)"""

        self.clear_debug()

        # Moderation equation:
        # <dep_var> = b0 + <slope_N * pred_N>... + <slope_N * inter_N>... + <slope_N * cov_N>... + E

        # TODO SD's?

        y = b0

        # Pred 1: X-axis value - NOTE assuming Pred 1 is CONT
        first_pred = self.land.predictors[0]
        first_pred.cur_value = self.possible_values[first_pred][point_num].value
        x = first_pred.cur_value
        y += first_pred.slope.value * first_pred.cur_value

        # Pred 2: current line
        second_pred = self.land.predictors[1]
        if second_pred.type.value == CONT or second_pred.count.value == 2:
            second_pred.cur_value = self.possible_values[second_pred][line_num].value
            y += second_pred.slope.value * second_pred.cur_value
        else:

            for level in range(second_pred.count.value):
                second_pred.cur_values[level] = 1 if level == line_num else 0
                y += second_pred.slopes[level].value * second_pred.cur_values[level]

        # Preds 3 and onward - NOTE Assuming order of plot values match land's predictors!
        for pred_index, pred in enumerate(self.land.predictors[2:self.land.num_pred.value]):

            if pred.type.value == CONT or pred.count.value == 2:
                pred.cur_value = plot.values[pred_index].value
                y += pred.slope.value * pred.cur_value
            else:

                for level in range(pred.count.value):
                    pred.cur_values[level] = plot.values[pred_index][level].value
                    y += pred.slopes[level].value * pred.cur_values[level]

        # Interactions
        for term in self.land.interactions.var_lists.keys():
            term_value = 1.0

            for pred,is_level,level in self.land.interactions.var_lists[term]:

                if is_level:
                    term_value *= pred.cur_values[level]
                else:
                    term_value *= pred.cur_value

            y += self.land.interactions.slopes[term].value * term_value

        # TODO Covariates
        # TODO e (?)

        return (x,y)

    def debug_interactions(self):
        self.clear_debug()

        for term in self.land.interactions.var_lists.keys():
            self.debug('Term: '+term)

            for pred,is_level,level in self.land.interactions.var_lists[term]:

                if is_level:
                    name = pred.levels[level].value
                    value = str(pred.cur_values[level])
                else:
                    name = pred.name.value
                    value = str(pred.cur_value)

                self.debug(' '+name+' L?='+str(is_level)+' l='+str(level)+ ' v='+value)


class ModerationEstimatesView(ipyw.HBox):
    """Set up and run UI for moderation estimates view"""

    def __init__(self, land):
        super().__init__()
        self.land = land
        self.est_txt = ipyw.Layout(width='98%')
        self.est_lbl = {'description_width': '65%'}
        self.beta = land.get_beta()
        self.dep_var_sd = ipyw.FloatText(value=DEFAULT_SD_VALUE, step=FLOAT_TEXT_STEP, description=land.dep_var.value, layout=self.est_txt,
                                         style=self.est_lbl)
        self.nt = ipyw.FloatText(step=FLOAT_TEXT_STEP, description=LATEX_NSUBT, layout=self.est_txt, style=self.est_lbl)
        self.b0 = ipyw.FloatText(step=FLOAT_TEXT_STEP, description=self.beta + UNICODE_SUBZERO,
                                 layout=self.est_txt, style=self.est_lbl)
        self.prop_warn = ipyw.HTML(PROP_WARN)
        self.prop_warn.layout.visibility = 'hidden'
        self.num_lines = None  # Count of lines in ea plots (same for every plot)
        self.debug_out = ipyw.Output(layout=ipyw.Layout(width='90%', border='solid 0px',
                                                       overflow_y='auto', margin='0 0 0 5px'))
        self.calc = Calculator(self.debug_out, self.land)  # Computes moderations values
        widgets = []  # Holding area for widgets prior to placing in columns

        # Col. 1: Proportions of categorical vars (both predictors & covariates)
        for var in land.predictors[:land.num_pred.value] + land.covariates[:land.pow_cov.value]:

            if var.type.value == CATG:

                if not widgets:
                    widgets += [ipyw.HTML(PROPORTIONS),self.prop_warn]

                for i  in range(var.count.value):
                    self.fixup_text_widget(var.props[i], var.levels[i].value)
                    var.props[i].observe(functools.partial(self.on_prop, var), 'value')
                    widgets += [var.props[i]]

        # Col. 1: SDs - "... in the standardized version there are no SDs..." via email, 2021-02-19
        if land.standard.value == UNSTD:
            # Label and dependent variable
            widgets += [ipyw.Label(value=SD_LABEL),self.dep_var_sd]

            # Continuous predictors & covariates
            for var in land.predictors[:land.num_pred.value] + land.covariates[:land.pow_cov.value]:

                if var.type.value == CONT:
                    self.fixup_text_widget(var.sd, var.name.value)
                    widgets += [var.sd]

            widgets += [ipyw.Label()]  # Blank line as separator TODO Better way?

        # Col. 2: NT, b0,
        widgets += [self.nt,self.b0]
        self.b0.observe(self.on_slope_change, 'value')

        # Col. 2: Predictor slopes
        for pred,level,slope in self.get_var_slope(land.predictors,land.num_pred.value):

            if level:
                self.fixup_text_widget(slope, pred.levels[level].value, add_beta=True)
            else:
                self.fixup_text_widget(slope, pred.name.value, add_beta=True)

            widgets += [slope]
            slope.unobserve(None, 'value')  # Clear any prior registrations
            slope.observe(self.on_slope_change, 'value')

        # Col. 2: Interaction slopes

        inters = []

        for key in self.land.interactions.ckboxes.keys():

            # Only display interaction if its ckbox is checked
            if self.land.interactions.ckboxes[key].value:
                self.fixup_text_widget(self.land.interactions.slopes[key],
                             self.land.interactions.slopes[key].description, add_beta=True)
                inters.append(self.land.interactions.slopes[key])
                self.land.interactions.slopes[key].unobserve(None, 'value')  # Clear any prior registrations
                self.land.interactions.slopes[key].observe(self.on_slope_change, 'value')

        if inters:
             widgets += inters

        # Col2: Covariate slopes
        for cov,level,slope in self.get_var_slope(land.covariates,land.pow_cov.value):
            self.fixup_text_widget(slope, cov.name.value, add_beta=True)
            widgets += [slope]
            slope.unobserve(None, 'value')  # Clear any prior registrations
            slope.observe(self.on_slope_change, 'value')

        # Evenly distribute lines into two columns
        col1_box = ipyw.VBox(layout=ipyw.Layout(width='50%', overflow='visible'))
        col2_box = ipyw.VBox(layout=ipyw.Layout(width='50%', overflow='visible'))
        col1_box.children = tuple(widgets[:len(widgets)//2])
        col2_box.children = tuple(widgets[len(widgets)//2:])

        # Plot status
        self.plot_status = ipyw.Label(layout=ipyw.Layout(width='98%'))  # 'Simple effect of X1 on Y at low X2'
        exp_box = ipyw.Box(layout=ipyw.Layout(margin='15px 0 0 0'))
        exp_box.add_class('gray_box')
        exp_box.children += (ipyw.VBox([
                                ipyw.VBox([ipyw.Label(SIMPLE_SLOPES_AND_EFFECTS)],
                                       layout=ipyw.Layout(width='100%', display='flex', align_items='center')),
                                ipyw.VBox([self.plot_status],
                                       layout=ipyw.Layout(width='100%', display='flex', align_items='flex-start'))
                             ],layout=ipyw.Layout(width='100%')),)

        # Plots
        if all([ ckbox.value for ckbox in self.land.interactions.ckboxes.values() ]):
            # All interactions selected, show plots
            plot_outs = self.build_plots()
        else: # User deselected an interactions, do not show plots
            plot_outs = [ipyw.HTML(PLOTS_DISABLED)]

        plot_box = ipyw.VBox(plot_outs,layout=ipyw.Layout(border='solid 1px gray'))

        # Final assembly of widgets/containers
        self.children += (ipyw.HBox([col1_box, col2_box],
                                     layout=ipyw.Layout(width='38%', overflow='visible',margin='0 10px 0 0')),
                          ipyw.VBox([plot_box, exp_box, self.debug_out], layout=ipyw.Layout(width='62%', overflow='visible')))
        self.layout = ipyw.Layout(width='100%', overflow='visible')

        #self.calc.debug_interactions()

    def fixup_text_widget(self, widget, description, add_beta=False):
        """Modify properties of given ipywidget Text widget"""
        widget.description = description

        if add_beta and widget.description[-1] != BIG_BETA and \
                        widget.description[-1] != LITTLE_BETA :
             widget.description += ' ' + self.beta

        widget.layout = self.est_txt
        widget.style = self.est_lbl

    def on_prop(self, var, _):
        """Show or hide proportion valid total warning"""
        total = 0.0

        for i in range(var.count.value):
            total += var.props[i].value

        self.prop_warn.layout.visibility = 'hidden' if total == 1.00 else 'visible'

    def get_var_slope(_, vars, num_visible):
        ret = []

        for var in vars[:num_visible]:

            # Continuous or categorical-dichotomous
            if var.type.value == CONT or (var.type.value == CATG and var.count.value == 2):
                ret.append((var, None, var.slope))
                continue

            # Categorical, not dichotomous
            for i in range(1,var.count.value):
                ret.append((var, i, var.slopes[i]))

        return ret

    def on_plot_change(self, xvar=None, name=None, slope=None):
        """Callback for plot change event"""

        if xvar is None:
            self.plot_status.value = ''
        else:
            self.plot_status.value = SIMPLE_EFFECT_OF_3 % (xvar, self.land.dep_var.value, name[0].lower()+name[1:])

            # Demo code
            self.land.predictors[0].slope.value = '%.4f' % slope
            self.land.predictors[1].slope.value = '%.4f' % slope

    def on_plot_select(self, title, label, slope):

        # Change High --> high, Low --> low  TODO What if var names contain "High" or "Low"?
        title = title.replace(HIGH, LC_HIGH)
        title = title.replace(LOW, LC_LOW)
        label = label.replace(HIGH, LC_HIGH)
        label = label.replace(LOW, LC_LOW)

        # Update status text to reflect selected line
        if len(self.plots) == 1:
            # Single plot - has no title
            self.plot_status.value = SIMPLE_EFFECT_OF_3 % (self.land.predictors[0].name.value,
                                                            self.land.dep_var.value, label)
        else:
            self.plot_status.value = SIMPLE_EFFECT_OF_4 % (self.land.predictors[0].name.value,
                                                            self.land.dep_var.value, label, title)

        self.plot_status.value += SLOPE + str(slope)

        # Reset all line colors in all plots
        for plot in self.plots:
            plot.reset_colors()

    def build_plots(self):
        """Create and display interactive plot(s), return list of plot output areas"""
        plot_outs = []

        # Count lines and build list of names for line labels
        if self.land.predictors[1].type.value == CONT:
            self.num_lines = 2
            line_names = [LOW + ' ' + self.land.predictors[1].name.value,
                          HIGH + ' ' + self.land.predictors[1].name.value]
        else:  # CATG
            self.num_lines = self.land.predictors[1].count.value
            line_names = [self.land.predictors[1].levels[i].value for i in range(self.land.predictors[1].count.value)]

        # Create a plot mgr, with a mod plot object, for each combination of possible values

        self.plots = []
        self.cur_hbox = ipyw.HBox()

        # Ask calc to generate possible values for each pred
        # Get them as a list but exclude pred #1 & #2 since they're every plot's x-axis & lines
        self.calc.build_possible_values()
        possible_values_3rd_on = list(self.calc.possible_values.values())[2:]

        # Plot each combination of possible values of preds 3 onward

        for plot_num, combo in enumerate(itertools.product(*possible_values_3rd_on)):

            # Build plot title

            title = ''

            for item in combo:  # Ea. item is a PredValue (CONT) or list of PredValues (CATG)

                if isinstance(item, list):  # CATG, not dichotomous: Find "activated" level (value=1)

                    for pred_val in item:

                        if pred_val.value == 1:
                            title += pred_val.pred.levels[pred_val.level].value + SEP
                            break

                elif item.pred.type.value == CATG and item.pred.count.value == 2:  # CATG, dichotmous
                    title += item.pred.levels[item.value].value + SEP
                elif item.value == 1:  # CONT, high
                    title += HIGH + ' ' + item.pred.name.value + SEP
                else: # CONT, low
                    title += LOW + ' ' + item.pred.name.value + SEP

            title = title[:-len(SEP)]  # Remove final separator

            # Create output area for plot

            if not plot_num % 2:  # Two plots per row, new hbox on every other index
                # Need to create new row
                self.cur_hbox = ipyw.HBox(layout=ipyw.Layout(width='100%'))
                plot_outs.append(self.cur_hbox)

            if self.land.num_pred.value == LEVEL_MIN:
                out = ipyw.Output(layout=ipyw.Layout(width='100%'))  # Single plot
            else:
                out = ipyw.Output(layout=ipyw.Layout(width='50%'))  # Multiple plots

            self.cur_hbox.children += (out,)

            # Create plot object, assign to new plot manager

            mod_plot = ModerationPlot(out, title, self.land.predictors[0].name.value,
                                      line_names, self, combo, self.debug_out)
            self.plots.append(mod_plot)

        if self.land.num_pred.value == LEVEL_MIN:  # Only one plot - fix up width
            self.plots[0].set_layout(ipyw.Layout(width='100%'))

        return plot_outs

    def on_slope_change(self, _):
        """Callback for slope changes: re-calc points in every plot"""

        for plot in self.plots:  # Each plot
            lines = []

            for line_num in range(self.num_lines):  # Each line
                line = []

                for point_num in range(2):  # Each point, "2" = Assume only start pt & end pt
                    x,y = self.calc.calculate(self.b0.value, plot, line_num, point_num)
                    line.append([x,y])

                lines.append(line)

            plot.update(lines)
            plot.reset_colors()

        self.plot_status.value = ''
