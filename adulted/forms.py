from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField, USSocialSecurityNumberField

from djforms.core.models import GENDER_CHOICES, STATE_CHOICES, COUNTRIES, BINARY_CHOICES, PAYMENT_CHOICES
from djforms.processors.models import Contact
from jenzabar import INFORMIX_EARL_TEST

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

NOW    = datetime.now()
MONTH  = int(NOW.month)
YEAR   = int(NOW.year)
YEAR7  = YEAR
YEAR14 = YEAR

UNI_YEARS1 = [x for x in reversed(xrange(1926,date.today().year + 1))]
UNI_YEARS2 = [x for x in reversed(xrange(1926,date.today().year + 3))]

EDUCATION_GOAL = (
    (1,"I would like to earn my first bachelor's degree."),
    (2,"I would like to earn my first bachelor's degree and also become certified to teach."),
    (3,"I would like to apply to the Master of Education program."),
    (4,"I would like to apply to the Accelerated Certification for Teachers program."),
    (5,"I already have a bachelor's degree and now would like to earn certification to teach."),
    (6,"I already have a bachelor's degree and now would like to complete an additional major."),
    (7,"I would like to take classes for my own personal interest."),
)

PROGRAM_CHOICES = (
    ("7","7 week format"),
    ("14","14 week Undergraduate or Graduate"),
)

# 7 week years
if MONTH >= 8:
    YEAR7 += 1

# 14 week years
if MONTH > 2 and MONTH < 10:
    YEAR14 += 1

SESSION7 = (
    ("7-AG-%s" % YEAR7, "January %s" % YEAR7),
    ("7-AK-%s" % YEAR7, "February %s" % YEAR7),
    ("7-AM-%s" % YEAR7, "April %s" % YEAR7),
    ("7-AS-%s" % YEAR7, "May %s" % YEAR7),
    ("7-AT-%s" % YEAR7, "July %s" % YEAR7),
)
if MONTH < 9:
    YEAR7 = YEAR
SESSION14 = (
    ("14-A-%s" % YEAR14, "September %s" % YEAR7),
    ("14-C-%s" % YEAR14, "February %s" % YEAR14),
)

class ContactForm(forms.ModelForm):
    """
    Contact form based on the generic processor model
    """
    previous_last_name  = forms.CharField(max_length=128, required=False, label="Previous Last Name")
    phone               = USPhoneNumberField(max_length=12, help_text="Format: XXX-XXX-XXXX")
    state               = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    postal_code         = USZipCodeField(label="Zip")

    class Meta:
        model = Contact
        exclude = ('country',)

    def __init__(self,*args,**kwargs):
        super(ContactForm,self).__init__(*args,**kwargs)
        self.fields['state'].widget.attrs['class'] = 'required'

class PersonalForm(forms.Form):
    """
    personal data
    """
    gender              = forms.TypedChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    ss_num              = USSocialSecurityNumberField(label="Social security number")
    dob                 = forms.DateField(label = "Date of birth", help_text="Format: dd/mm/yyyy")
    pob                 = forms.CharField(label = "Place of birth", help_text="City, state, zip, country", max_length=255)

class EmploymentForm(forms.Form):
    """
    employment history
    """
    # current employment
    employer            = forms.CharField(max_length=128, required=False)
    position            = forms.CharField(max_length=128, required=False)
    tuition_reimburse   = forms.TypedChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect(), label="Does your employer offer tuition reimbursement?")

class EducationGoalsForm(forms.Form):

    educationalgoal     = forms.TypedChoiceField(choices=EDUCATION_GOAL, widget=forms.RadioSelect(), label="What degree are you intending to pursue?")
    program             = forms.TypedChoiceField(choices=PROGRAM_CHOICES, widget=forms.RadioSelect(), label="Choose the scheduling format")
    session7            = forms.TypedChoiceField(choices=SESSION7, widget=forms.RadioSelect(), label="Upcoming 7 Week Sessions", required=False)
    session14           = forms.TypedChoiceField(choices=SESSION14, widget=forms.RadioSelect(), label="Upcoming 14 Week Sessions", required=False)
    intended_major      = forms.CharField(max_length=128, required=False)
    intended_minor      = forms.CharField(max_length=128, required=False)
    certificiation      = forms.CharField(max_length=128, label="Intended certification", required=False)

    def clean(self):
        if not self.cleaned_data.get('session7') and not self.cleaned_data.get('session14'):
            self._errors["session7"] = self.error_class(["Choose either a 7 or 14 week upcoming session"])
        return self.cleaned_data

class ApplicationFeeForm(forms.Form):
    """
    Application Fee form
    """
    amount              = forms.CharField(widget=forms.HiddenInput(), initial="$10.00")
    payment_type        = forms.TypedChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())


def _insert(data):
    """
    private method to insert data into informix for adult education applications
    """

    DATE = datetime.now().strftime("%m/%d/%Y")
    YEAR = int(datetime.now().strftime("%Y"))
    MONTH = int(datetime.now().strftime("%m"))
    TIME = datetime.now().strftime("%H:%M:%S")
    PURGE_DATE = (date.today() + relativedelta( months = +2 )).strftime("%m/%d/%Y")

    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()


    # create unifying id number
    sql =   'INSERT INTO apptmp_rec (add_date,add_tm,app_source,stat) VALUES (%s, %s, "AEA", "P")' % (DATE,TIME)
    connection.execute(sql)
    # get unifying id (uid)
    sql =   "SELECT DISTINCT dbinfo('sqlca.sqlerrd1') FROM apptmp_rec"
    objects = connection.execute(sql)
    # retrieve the id
    for r in objects:
        apptmp_no = r[0]

    # personal information
    sql =   """
            INSERT INTO app_idtmp_rec (
                id, firstname, middlename, lastname, addr_line1, addr_line2, city, st, zip, ctry,
                phone, ss_no, aa, add_date, ofc_add_by, upd_date, purge_date,
                prsp_no, name_sndx, correct_addr, decsd, valid)
            VALUES (%s,"%s","%s","%s","%s","%s","%s","%s","%s","USA",
                    "%s","%s","PERM","%s","ADLT","%s","%s","0", "", "Y", "N", "Y")
            """ % (apptmp_no,data["contact"]["first_name"],data["contact"]["middle_name"],data["contact"]["last_name"],
                   data["contact"]["address1"],data["contact"]["address2"],data["contact"]["city"],data["contact"]["state"],
                   data["contact"]["postal_code"],data["contact"]["phone"],data["personal"]["ss_num"],DATE,DATE,PURGE_DATE)
    connection.execute(sql)

    # jenzabar freakiness
    sql =   """
            INSERT INTO app_sitetmp_rec
                (id, home, site, beg_date)
            VALUES (%s, "Y", "CART", "%s")
            """ % (apptmp_no, DATE)
    connection.execute(sql)

    # Education plans
    #
    # decode programs, subprograms, plan_enr_sess and plan_enr_yr
    if data["education"]["educationgoal"] in (1,2,5,6,7):
        program4 = "UNDG"
        if data["education"]["program"] == "7":
            subprogram = "7WK"
        else:
            subprogram="PTSM"
    elif data["education"]["educationgoal"] == "3":
        program4 = "GRAD"
        subprogram="MED"
    elif data["education"]["educationgoal"] == "4":
        program4 = "ACT"
        subprogram = "ACT"
    else:
        program4 = ""
        subprogram = ""

    # seesion info from code: e.g. 14-C-2013
    if data["education"]["program"] == "7":
        start = data["education"]["session7"].split('-')
    elif data["education"]["program"] == "14":
        start = data["education"]["session14"].split('-')
    if isinstance(start, list):
        plan_enr_sess = start[0]
        plan_enr_yr = start[2]
        start_session = start[0]
        start_year = start[2]
    else:
        plan_enr_sess = ""
        plan_enr_yr = ""
        start_session = ""
        start_year = ""

    sql =   """
            INSERT INTO app_admtmp_rec (
                id, primary_app, plan_enr_sess, plan_enr_yr, intend_hrs_enr,
                add_date, parent_contr, enrstat, rank, emailaddr,
                prog, subprog, upd_uid, add_uid, upd_date, act_choice, stuint_wt, jics_candidate)
            VALUES (%s,"Y", "%s", "%s", "4", "%s", "0.00", "", "0",
                "%s", "%s", "%s", "0", "0", "%s", "", "0", "N")
            """ % (apptmp_no,start_session,start_year,DATE,data["contact"]["email"], program4, subprogram,DATE)
    connection.execute(sql)

    # birthday
    sql =   """
            INSERT INTO app_proftmp_rec
                (id, birth_date, birthplace_city, sex, church_id, prof_last_upd_date)
            VALUES (%s,"%s","%s","%s","0","%s")
            """ % (apptmp_no, data["personal"]["dob"], data["personal"]["pob"], data["personal"]["gender"], DATE)
    connection.execute(sql)

    # schools
    for school in data["schools"]:
        # attended from
        try:
            attend_from = datetime(int(school.from_year),int(school.from_month), 1)
        except:
            attend_from = datetime(1900,1,1)
        # attende to
        try:
            attend_to = datetime(int(school.to_year),int(school.to_month), 1)
        except:
            attend_to = datetime(1900,1,1)
        # grad date
        try:
            grad_date = datetime(int(school.grad_year),int(school.grad_month), 1)
        except:
            grad_date = datetime(1900,1,1)

        sql =   """
                INSERT INTO app_edtmp_rec (
                    id, ceeb, fullname, city, st, enr_date, dep_date, grad_date,
                    stu_id, sch_id, app_reltmp_no, rel_id,priority, zip, aa, ctgry)
                VALUES (%s,"%s","%s","%s","%s","%s","%s","%s",0,0,0,0,0,"", "ac","COL")
                """ % (apptmp_no,
                    school.school_code, school.school_name, school.school_city,
                    school.school_state, attend_from, attend_to, grad_date)
        connection.execute(sql)

    # payment info
    sql =   """
            UPDATE
                apptmp_rec
            SET
                payment_method = "%s", stat = "H"
            WHERE
                apptmp_no = %s
            """ % (data["fee"]["payment_type"], apptmp_no)
    connection.execute(sql)
    connection.close()

