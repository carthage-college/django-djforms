
update communications_printrequest set user_id =  where user_id =
update communications_printrequest set updated_by_id =  where updated_by_id =

update scholars_presentation set user_id =  where user_id =
update scholars_presentation set updated_by_id=  where updated_by_id =

update committee_letter_evaluation set created_by_id = where created_by_id =
update committee_letter_evaluation set updated_by_id = where updated_by_id =

update green_pledge set user_id =  where user_id =

update core_userprofile set user_id =  where user_id = 

update auth_user_groups set user_id =  where user_id =
update auth_user set id =  where id = 

# celebration of scholars
./scholars/models.py:    user = models.ForeignKey(
./scholars/models.py:    updated_by = models.ForeignKey(
# promotion
./core/models.py:    user = models.ForeignKey(
# catering
./catering/models.py:    user = models.ForeignKey(
# choral tryouts
./music/ensembles/choral/models.py:    user = models.ForeignKey(
# LIS print request
./lis/copyprint/models.py:    user = models.ForeignKey(
./lis/copyprint/models.py:    updated_by = models.ForeignKey(
# writing curriculum
./writingcurriculum/models.py:    user = models.ForeignKey(
./writingcurriculum/models.py:    updated_by = models.ForeignKey(
# applicant
./prehealth/committee_letter/models.py:    created_by = models.ForeignKey(
./prehealth/committee_letter/models.py:    updated_by = models.ForeignKey(
# evaluation
./prehealth/committee_letter/models.py:    created_by = models.ForeignKey(
./prehealth/committee_letter/models.py:    updated_by = models.ForeignKey(
# characterquest
./characterquest/models.py:    profile = models.ForeignKey(UserProfile)
# jobs
./jobpost/models.py:    creator = models.ForeignKey(User, null=True, blank=True)
# green pledge
./sustainability/green/models.py:    user = models.ForeignKey(
# maintenance
./maintenance/models.py:    user = models.ForeignKey(
./maintenance/models.py:    updated_by = models.ForeignKey(
# print request
./communications/printrequest/models.py:    user = models.ForeignKey(
./communications/printrequest/models.py:    updated_by = models.ForeignKey(

