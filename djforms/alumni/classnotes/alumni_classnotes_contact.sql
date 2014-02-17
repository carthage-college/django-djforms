UPDATE alumni_classnotes_contact SET created_at = notesubmitteddate;
UPDATE alumni_classnotes_contact SET updated_at = created_at;
UPDATE alumni_classnotes_contact SET previous_name = maidenname;
UPDATE alumni_classnotes_contact SET classnote = pubtext where pubtext != '';

ALTER TABLE alumni_classnotes_contact DROP notesubmitteddate;
ALTER TABLE alumni_classnotes_contact DROP maidenname;
ALTER TABLE alumni_classnotes_contact DROP webpicname;
ALTER TABLE alumni_classnotes_contact DROP pubtext;

