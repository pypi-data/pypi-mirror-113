# mod_land.py - Moderation Landing UI, rcampbel, March 2021
#from IPython.core.debugger import Pdb; Pdb().set_trace() # breakpoint

import itertools
import ipywidgets as ipyw

PRED_MIN = 2
COV_MIN = 0
PRED_MAX = 5
COV_MAX = 20
LEVEL_MIN = 2
LEVEL_MAX = 6
BIG_BETA = u'𝛽'
LITTLE_BETA = u'𝑏'
CONT = 'Continuous'
CATG = 'Categorical'
CONT_CATG_OPTS = [CONT, CATG]
TOTAL_COV_OPTS = [('No covariates'       , 0),('One covariat'        , 1),
                  ('Two covariates'      , 2),('Three covariates'    , 3),
                  ('Four covariates'     , 4),('Five covariates'     , 5),
                  ('Six covariates'      , 6),('Seven covariates'    , 7),
                  ('Eight covariates'    , 8),('Nine covariates'     , 9),
                  ('Ten covariates'      ,10),('Eleven covariates'   ,11),
                  ('Twelve covariates'   ,12),('Thirteen covariates' ,13),
                  ('Fourteeen covariates',14),('Fifteen covariates'  ,15),
                  ('Sixteen covariates'  ,16),('Seventeen covariates',17),
                  ('Eighteen covariates' ,18),('Nineteen covariates' ,19),
                  ('Twenty covariates'   ,20)]
STD = 'Standardized'
UNSTD = 'Unstandardized'
LEVELS = 'Levels:'
PROP_MIN = 0
PROP_MAX = 1
FLOAT_TEXT_STEP = 0.01
DEFAULT_SD_VALUE = 1


class Variable:
    """A predictor or covariate"""
    INIT_LEVEL = 'Lvl'

    def __init__(self, name, observe_method):
        self.name =  ipyw.Text(value=name, layout=ipyw.Layout(width='100px'), continuous_update=False)
        self.type = ipyw.Dropdown(layout=ipyw.Layout(width='100px'), options=CONT_CATG_OPTS)
        self.sd = ipyw.FloatText(value=DEFAULT_SD_VALUE, step=FLOAT_TEXT_STEP)
        self.slope = ipyw.FloatText(step=FLOAT_TEXT_STEP)
        self.cur_value = None

        # Levels - if categorical

        self.count = ipyw.Dropdown(description=LEVELS, layout=ipyw.Layout(width='97px'),
                                   style={'description_width': '50px'},
                                   options=[i for i in range(LEVEL_MIN, LEVEL_MAX+1)])

        self.levels = []  # Names for each level
        self.props = []  # Proportions for each level
        self.slopes = []  # Slopes for each level
        self.cur_values = []  # Current values for each level

        for i in range(LEVEL_MAX):
            self.levels.append(ipyw.Text(layout=ipyw.Layout(width='100px'), value=name + self.INIT_LEVEL + str(i+1)))
            self.props.append(ipyw.BoundedFloatText(min=PROP_MIN, max=PROP_MAX, step=FLOAT_TEXT_STEP))
            self.slopes.append(ipyw.FloatText(step=FLOAT_TEXT_STEP))
            self.cur_values.append(None)

        self.count.observe(observe_method, 'value')
        self.name.observe(observe_method, 'value')
        self.type.observe(observe_method, 'value')


class Interactions:
    """Mange list of interactions for calculation and user selection (include/exclude)"""

    def __init__(self, label, grid, callback):
        self.label = label  # widget, title of ckbox area
        self.grid = grid  # ckbox output widget
        self.callback = callback  # UI refresh method to be called after ckbox change
        self.ckboxes = {}  # Dict of ckboxes indexed by term ("*X1*X2")
        self.slopes = {}  # Dict of texts indexed by term
        self.var_lists = {}  # Dict of tuples (<pred>,<is_level>,<level>) indexed by term

    def reset(self):
        self.ckboxes = {}
        self.slopes = {}
        self.var_lists = {}

    def add(self, term, var_list):
        desc = term.replace('*','',1)  # Remove leading "*" from term
        ckbox = ipyw.Checkbox(value=True, indent=False, description=desc,
                              layout=ipyw.Layout(width='max-content', margin='0 0 0 0'))
        ckbox.observe(self.on_checkbox, 'value')
        self.ckboxes[term] = ckbox
        self.slopes[term] = ipyw.FloatText(step=FLOAT_TEXT_STEP, description=desc)
        self.var_lists[term] = var_list

    def included(self, term):
        return self.ckboxes[term].value

    def render(self, show_ckboxes):

        if self.ckboxes and show_ckboxes:
            widgets = []

            for ckbox in self.ckboxes.values():
                widgets.append(ckbox)

            self.grid.children = widgets
            self.label.layout.visibility = 'visible'
        else:
            self.grid.children = []
            self.label.layout.visibility = 'hidden'

    def on_checkbox(self, change):
        """Higher order terms depend on the inclusion of lower order terms)"""
        changed = change['owner']
        order_level = changed.description.count('*')

        for ckbox in self.ckboxes.values():
            ckbox.unobserve(None, 'value')  # Temporarily disable ckbox's callback

            if changed.value and ckbox.description.count('*') < order_level:
                ckbox.value = True  # Force inclusion of lower order term

            elif not changed.value and ckbox.description.count('*') > order_level:
                ckbox.value = False  # Force exclusion of higher order term

            ckbox.observe(self.on_checkbox, 'value')  # Re-enable ckbox's callback

        self.callback(ckbox_activity=True)


class Equation:
    """Display equation"""
    EMPTY = u''
    SPACE = u'\u2004'
    EQUAL = u'='
    PLUS = u'+'
    EPSILON = u'𝜀'

    def __init__(self,left,right,max=106):  # max=112, 150
        self.left = left  # Left side output widget
        self.right = right  # Right side output widget
        self.max = max  # Maximum line length
        self.line = None  # Output buffer, string
        self.slope_index = None  # Next slope subscript, integer
        self.beta = None  # Beta character, string
        self.sub = str.maketrans("Bb0123456789",
                                 u"𝛽𝑏₀₁₂₃₄₅₆₇₈₉")
        self.ital = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  u"𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝘩𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝘴𝑡𝑢𝑣𝑤𝑥𝑦𝑧")

    def set_left(self, dep_var):
        """Left side uses LaTeX to enable hat stretch over variable"""
        self.left.children = (ipyw.HTMLMath('$\hat{' + dep_var + '} = $'),)

    def start_right(self, big_beta):
        """Right side uses Unicode characters for speed"""
        self.beta = 'B' if big_beta else 'b' # will be translated to small beta
        self.slope_index = 0  # for building equation
        self.right.clear_output()
        self.line = self.next_slope()

    def next_slope(self):
        slope = self.beta + str(self.slope_index)
        self.slope_index += 1
        return slope.translate(self.sub)

    def add(self,term):
        additional = self.SPACE + self.PLUS + self.SPACE + self.next_slope() + term.replace('*','').translate(self.ital)

        if len(self.line + additional) > self.max:
            self.flush_right()

        self.line += additional  # buffer output

    def flush_right(self):# ,force=False):
        """Flush output buffer, start new line"""

        if not self.line == self.EMPTY:

            if len(self.line) > 0 and self.line[0] == self.SPACE:
                self.line = self.line[1:]

            with self.right:
                print(self.line)
                self.line = self.EMPTY

    def end_right(self):
        self.flush_right()
        self.line = self.SPACE + self.PLUS + self.SPACE + self.EPSILON
        self.flush_right()


class ModerationLandingView(ipyw.Box):
    """Set up and run UI for moderation landing view"""

    INIT_DEPVAR = 'Y'
    INIT_PRED = 'X'
    INIT_COV = 'Cov'
    DEPENDENT_VARIABLE = 'Dependent variable:'
    PREDICTORS = 'Predictors:'
    POWER_COVARIATES = 'Power covariates?'
    POWER_CUSTOM_EFFECTS = 'Power custom effects:'

    def __init__(self):
        super().__init__()
        labelStyle = {'description_width': '135px', 'text-align': 'left'}  # 120px

        # Create one off widgets
        self.eq_left = ipyw.Box()
        # TODO Fixed eqation height (current) or allow height to vary with size of eq?
        self.eq_right = ipyw.Output(layout=ipyw.Layout(width='100%', max_height='200px', height='150px',
                                                       overflow_y='auto', margin='0 0 0 5px'))
        self.standard = ipyw.Dropdown(layout=ipyw.Layout(width='max-content', margin='0 0 20px 0'),
                                      options=[STD, UNSTD],
                                      value=UNSTD)
        self.dep_var = ipyw.Text(description=self.DEPENDENT_VARIABLE, style=labelStyle, value=self.INIT_DEPVAR,
                                 layout=ipyw.Layout(width='max-content'), continuous_update=False)  # 240px
        self.num_pred = ipyw.Dropdown(description=self.PREDICTORS,
                                      layout=ipyw.Layout(width='max-content'),
                                      style=labelStyle,
                                      options=[i for i in range(2, PRED_MAX + 1)])
        self.total_cov = ipyw.Dropdown(layout=ipyw.Layout(width='max-content'),options=TOTAL_COV_OPTS)
        self.pow_cov  = ipyw.Dropdown(description=self.POWER_COVARIATES,
                                      layout=ipyw.Layout(width='max-content',visibility = 'hidden'),
                                      style=labelStyle,
                                      options=[0])
        self.eq = Equation(self.eq_left,self.eq_right)  # Mgr for dynamic output of eqation

        # Watch for changes
        self.dep_var.observe(self.on_dep_var, 'value')
        self.standard.observe(self.on_standard, 'value')
        self.total_cov.observe(self.on_total_covariates, 'value')
        self.num_pred.observe(self.on_num_pred, 'value')
        self.pow_cov.observe(self.on_render_covariates, 'value')

        # Create lists of moderation variables
        self.predictors = [Variable(self.INIT_PRED + str(i+1), self.on_render_predictors)
                           for i in range(PRED_MAX)]
        self.covariates = [Variable(self.INIT_COV + str(i+1), self.on_render_covariates)
                           for i in range(COV_MAX)]

        # Create display widgets and storage for interactions
        self.pow_cust_eff_label = ipyw.Label(layout=ipyw.Layout(margin='10px 0 0 0'))
        self.custom_inter = ipyw.GridBox(layout=ipyw.Layout(grid_template_columns="repeat(4, 25%)"))
        self.interactions = Interactions(self.pow_cust_eff_label, self.custom_inter, self.update_equation_right)

        # Create output areas for variables
        self.pred_out = ipyw.Box()
        self.cov_out = ipyw.Box()

        # Lay out widgets
        self.layout = ipyw.Layout(width='100%')
        eq_box = ipyw.HBox([self.eq_left,self.eq_right], layout=ipyw.Layout(width='85%',
                                                                            margin='20px 0 20px 50px',
                                                                            padding='10px 10px 10px 10px',
                                                                            border='solid 1px LightGrey'))
        left_box = ipyw.VBox([self.dep_var, self.num_pred, self.pred_out],
                            layout=ipyw.Layout(width='50%'))
        right_box = ipyw.VBox([self.standard, self.total_cov, self.pow_cov, self.cov_out],
                             layout=ipyw.Layout(width='50%'))
        self.children = (ipyw.VBox([eq_box,ipyw.HBox([left_box, right_box]),
                                    self.pow_cust_eff_label, self.custom_inter],
                                    layout = ipyw.Layout(width='100%')),)

        self.on_dep_var(None)
        self.on_render_predictors(None)
        self.on_render_covariates(None)

    def get_beta(self):
        return BIG_BETA if self.is_big_beta() else LITTLE_BETA

    def on_dep_var(self, _):
        self.eq.set_left(self.dep_var.value)

    def on_num_pred(self, _):
        self.pow_cust_eff_label.value = self.POWER_CUSTOM_EFFECTS if int(self.num_pred.value) > 2 else ''
        self.on_render_predictors()

    def on_standard(self, _):
        self.update_equation_right()

    def on_total_covariates(self, _):

        if self.total_cov.value > 0:
            old = self.pow_cov.value
            self.pow_cov.options = [i for i in range(0, self.total_cov.value + 1)]
            self.pow_cov.value = min(old,max(self.pow_cov.options))
            self.pow_cov.layout.visibility = 'visible'
        else:
            self.pow_cov.value = 0
            self.pow_cov.layout.visibility = 'hidden'

    def on_render_predictors(self, _=None):
        self.render_variables(self.predictors, self.num_pred.value, self.pred_out)
        self.update_equation_right()

    def on_render_covariates(self, _):
        self.render_variables(self.covariates, self.pow_cov.value, self.cov_out)
        self.update_equation_right()

    def render_variables(_, var_list, num_visible, box):
        """Redraw given moderation variables in given output area"""
        var_box = ipyw.VBox()  # TODO Just use box instead?

        for (i, var) in enumerate(var_list):

            if i == num_visible:
                break

            lineBox = ipyw.HBox([var.name, var.type])
            var_box.children += (lineBox,)

            if var.type.value == CATG:
                lineBox.children += (var.count,)
                var_box.children += (ipyw.VBox([var.levels[j] for j in range(var.count.value)],
                                              layout=ipyw.Layout(margin='0 0 0 205px')),)

        box.children = (var_box,)

    def is_big_beta(self):
        return self.standard.value == STD

    def update_equation_right(self, ckbox_activity=False):
        """Redraw full equation using dep. variable, predictors, and covariates"""
        self.eq.start_right(self.is_big_beta())
        preds = []  # List of tuples: (name,pred#)

        # Fill special list of predictor tuples - just for interactions
        # Tuple: (name_as_str, id_as_int, is_level_as_bool, level_as_int) TODO Create class?
        for p,pred in enumerate(self.predictors[:self.num_pred.value]):

            # Continuous or categorical, dichotomous
            if pred.type.value == CONT or (pred.type.value == CATG and pred.count.value == 2):
                preds.append((pred.name.value,p,False,None))
                continue

            # Categorical, not dichotomous
            for i in range(1,pred.count.value):
                preds.append((pred.levels[i].value,p,True,i))

        if not ckbox_activity:
            self.interactions.reset()  # Rebuild interaction ckboxes

        self.eq.terms = []  # Rebuild list of terms, will be list of tuples of tuples)

        # Add terms, saving interactions along the way
        for combo_len in range(len(self.predictors)):

            for combo in itertools.combinations(preds, combo_len+1):
                term = ''
                var_list = []
                represented = []
                valid = True

                for name,id,is_level,level_index in combo:

                    if id in represented:
                        valid = False  # Exlude combos w/mult. vars from same predictor
                        break

                    term += '*' + name
                    var_list.append((self.predictors[id], is_level, level_index))  # New class?
                    represented.append(id)

                if not valid:  # Term includes multiple "level" vars from single predictor
                    continue

                if combo_len == 0:  # Base term (one var, no interaction) always appears in equation
                    self.eq.add(term)
                    continue

                if ckbox_activity:  # User is including/excluding interacations

                    if self.interactions.included(term):
                        self.eq.add(term)

                    continue

                # User is adding/removing predictors/covariates (default logic)
                self.eq.add(term)
                self.interactions.add(term, var_list)

            self.eq.flush_right()

        self.eq.flush_right()

        # Covariates

        for cov in self.covariates[:self.pow_cov.value]:

            if cov.type.value == CONT:
                self.eq.add(cov.name.value)
            else:

                for i in range(cov.count.value):
                    self.eq.add(cov.levels[i].value)

        # Error term (epsilon)
        self.eq.end_right()

        if not ckbox_activity:
            self.interactions.render(int(self.num_pred.value) > 2)
