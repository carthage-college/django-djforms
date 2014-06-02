# -*- coding: utf-8 -*-
from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.admissions.admitted.models import *

GENDER_CHOICES = (
    ('Female (女)','Female (女)'),
    ('Male (男)','Male (男)'),
)
LEVEL_CHOICES = (
    ('Undergraduate Freshman','Undergraduate Freshman'),
    ('Undergraduate Transfer','Undergraduate Transfer'),
    ('Graduate Student','Graduate Student'),
)
HELP_CHOICES = (
    ('I am interested in scheduling an admission and scholarship interview in China',
     'I am interested in scheduling an admission and scholarship interview in China',),
    ('I am interested in scheduling a musical theatre audition in China',
     'I am interested in scheduling a musical theatre audition in China'),
    ('I would like to receive more information about your programs',
     'I would like to receive more information about your programs',)
)
UNDERGRADUATE_DEGREES = (
    ('Accounting','Accounting 会计学'),
    ('Art - Art History','Art - Art History 艺术—艺术史'),
    ('Art - Studio Art','Art - Studio Art 艺术—室内艺术'),
    ('Asian Studies','Asian Studies 亚洲研究'),
    ('Athletic Training','Athletic Training 运动训练学'),
    ('Biology','Biology 生物学'),
    ('Business','Business 商学'),
    ('Chemistry','Chemistry 化学'),
    ('Chinese','Chinese 中文'),
    ('Classical Archaeology','Classical Archaeology 古典考古学'),
    ('Classical Foundations','Classical Foundations 古典基础'),
    ('Classical Studies','Classical Studies 古典文学研究'),
    ('Communication','Communication 通讯'),
    ('Computer Science','Computer Science 计算机科学'),
    ('Criminal Justice','Criminal Justice 刑事司法'),
    ('Economics','Economics 经济学'),
    ('Education - Special Education (Grades K-12)','Education - Special Ed. (Grades K-12) 教育学—特殊教育 (K-12 年级)'),
    ('Education - Elementary/Middle Education (Grades 1-8)','Education - Elementary/Middle Ed. (Grades 1-8) 教育学—小学/初中教育（1-8年级)'),
    ('Education - Middle/Secondary Education (Grades 6-12)','Education - Middle/Secondary Ed. (Grades 6-12) 教育学—初中/高中教育（6-12年级)'),
    ('English','English 英文'),
    ('English with emphasis in Creative Writing','English with emphasis in Creative Writing 英文创意写作'),
    ('Environmental Science','Environmental Science 环境科学'),
    ('Finance','Finance 金融'),
    ('French','French 法文'),
    ('Geography & Earth Science','Geography & Earth Science 地理和地球科学'),
    ('German','German 德文'),
    ('Graphic Design','Graphic Design 平面设计'),
    ('Great Ideas','Great Ideas 经典思想研究'),
    ('History','History 历史学'),
    ('International Political Economy','International Political Economy 国际政治经济学'),
    ('Japanese','Japanese 日文'),
    ('Management','Management 管理学'),
    ('Marketing','Marketing 市场营销学'),
    ('Mathematics','Mathematics 数学'),
    ('Music','Music 音乐'),
    ('Music - Church Music','Music - Church Music 音乐—教会音乐学'),
    ('Music - Instrumental Music Education','Music - Instrumental Music Education 器乐教育学'),
    ('Music - Jazz Studies','Music - Jazz Studies 音乐—爵士乐研究'),
    ('Music - Performance','Music - Performance 音乐—表演'),
    ('Music - Piano Pedagogy','Music - Piano Pedagogy 音乐—钢琴教育学'),
    ('Music - Vocal Music Education','Music - Vocal Music Education 音乐—声乐教育学'),
    ('Music Theatre','Music Theatre 音乐剧'),
    ('Neuroscience','Neuroscience 神经科学'),
    ('Philosophy','Philosophy 哲学'),
    ('Physical Education','Physical Education 体育教育学'),
    ('Physical Education, Sport and Fitness Instruction','Physical Education, Sport and Fitness Instruction 体育教育学、运动与健身指导'),
    ('Physics','Physics 物理学'),
    ('Political Science','Political Science 政治学'),
    ('Psychology','Psychology 心理学'),
    ('Public Relations','Public Relations 公共关系'),
    ('Religion','Religion 宗教研究'),
    ('Social Science','Social Science 社会科学'),
    ('Social Work','Social Work 社会福利工作'),
    ('Sociology','Sociology 社会学'),
    ('Spanish','Spanish 西班牙文'),
    ('Theatre','Theatre 戏剧'),
    ('Theatre - Performance','Theatre - Performance 戏剧—表演'),
    ('Theatre - Technical Production and Design','Theatre - Technical Production and Design 戏剧—技术制作与设计'),
    ('Self-Designed Major','Self-Designed Major 自定主修'),
)
GRADUATE_DEGREES = (
    ('Business (MBA)','Business (MBA) 商学（工商管理硕士)'),
    ('Education','Education 教育学'),
)

class InterestForm(forms.Form):
    last_name = forms.CharField(
        label="Last name (姓)"
    )
    first_name = forms.CharField(
        label="First name (名)"
    )
    dob = forms.DateField(
        label="Birthday (出生日)",
        help_text="(MM/DD/YYYY) (月月／日日／年年年年)"
    )
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES,widget=forms.RadioSelect()
    )
    address = forms.CharField(
        label='Home address (家庭地址)',
        max_length=255,widget=forms.TextInput()
    )
    city = forms.CharField(
        label='City (城市)',max_length=128,
        widget=forms.TextInput()
    )
    postal_code = forms.CharField(
        label='Postal code (邮政编码)', max_length='6'
    )
    country = forms.CharField(
        label='Country (国家)',max_length=128
    )
    email = forms.EmailField(
        label='Email address (电子邮件信箱)'
    )
    phone = forms.CharField(
        label='Telephone number (电话)',max_length=18
    )
    mobile = forms.CharField(
        label='Cell phone number (手机号码)',max_length=18,required=False
    )
    level = forms.TypedChoiceField(
        label="Entering level",choices=LEVEL_CHOICES,
        widget=forms.RadioSelect()
    )
    how_help = forms.MultipleChoiceField(
        label="How may we help you? Check all that apply.",
        choices=HELP_CHOICES,widget=forms.CheckboxSelectMultiple()
    )
    undergrad = forms.MultipleChoiceField(
        label="Undergraduate degree interest 本科学位课程. Check all that apply.",
        choices=UNDERGRADUATE_DEGREES,
        widget=forms.CheckboxSelectMultiple()
    )
    graduate = forms.MultipleChoiceField(
        label="Graduate degrees 研究生学位课程. Check all that apply.",
        choices=GRADUATE_DEGREES,
        widget=forms.CheckboxSelectMultiple()
    )
