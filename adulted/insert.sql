Are we adding?
    address2
    gender
    ss
    pob
    middle_name
    previous_name
    employer
    position
    reimbursement
    major
    minor
    cert


<!--- create unifying id number --->
INSERT INTO apptmp_rec (add_date,add_tm,app_source,stat,reason_txt)
       VALUES ("#now_date#",
               "#now_time#",
               "AEA",
               "P",
               "#temp_uuid#")

<!--- get unifying id (uid) --->
SELECT apptmp_no
       FROM apptmp_rec
       WHERE reason_txt = "#temp_uuid#"

<!--- personal information (name, address, contact info) --->
INSERT INTO app_idtmp_rec
       (id, firstname, lastname, addr_line1, city, st, zip, ctry, phone,
        aa, add_date, ofc_add_by, upd_date, purge_date, 
        prsp_no, name_sndx, correct_addr, decsd, valid)
       VALUES ("#lookup_apptmp_no.apptmp_no#",
               "#form.first_name#",
               "#form.last_name#",
               "#form.perm_line1#",
            "#form.perm_city#",
            "#form.perm_st#",
            "#form.perm_zip#",
            "#form.perm_ctry#",
            "#library.format_phone_number(form.home_phone)#",
            "PERM",
            "#now_date#",
            "ADLT",
            "#now_date#",
            "#purge_date#",
            "0",
            "",
            "Y",
            "N",
            "Y"
)

<!--- not sure what this does, but it's probably important --->
INSERT INTO app_sitetmp_rec
           (id, home, site, beg_date)
       VALUES ("#lookup_apptmp_no.apptmp_no#",
                "Y",
                "CART",
                "#now_date#"
                )

 <!--- decode programs, subprograms, plan_enr_sess and plan_enr_yr --->
    <cfif listFind("1,2,5,6,7",form.educationalgoal) GT 0>
        <cfset program4="UNDG" />
        <cfif form.program EQ "7week">
            <cfset subprogram="7WK" />
        <cfelse>
            <cfset subprogram="PTSM" />
        </cfif>
    <cfelseif form.educationalgoal EQ 3>
        <cfset program4="GRAD" />
        <cfset subprogram="MED" />
    <cfelseif form.educationalgoal EQ 4>
        <cfset program4="ACT" />
        <cfset subprogram="ACT" />
    </cfif>

    <cfif !IsNull(form.start)>
        <cfset plan_enr_sess = ListGetAt(form.start, 2, "-") />
        <cfset plan_enr_yr = ListGetAt(form.start, 3, "-") />
        <cfset start_session = ListGetAt(form['start'], 2, "-") />
        <cfset start_year = ListGetAt(form['start'], 3, "-") />
    <cfelse>
        <cfset plan_enr_sess = "" />
        <cfset plan_enr_yr = "" />
        <cfset start_session = "" />
        <cfset start_year = "" />
    </cfif>

    <cfif IsNull(program4)>
        <cfset program4 = "" />
    </cfif>
    <cfif IsNull(subprogram)>
        <cfset subprogram = "" />
    </cfif>

    <cfif !IsNull(form.start)>
        <cfquery name="q_create_adm" datasource="#application.dsn#">
            INSERT INTO app_admtmp_rec
                   (id, primary_app, plan_enr_sess, plan_enr_yr, intend_hrs_enr,
                    add_date, parent_contr, enrstat, rank, emailaddr,
                    prog, subprog, upd_uid, add_uid, upd_date, act_choice, stuint_wt, jics_candidate)
            VALUES ("#lookup_apptmp_no.apptmp_no#",
                    "Y",
                    "#start_session#",
                    "#start_year#",
                    "4",

                    "#now_date#",
                    "0.00",
                    "",
                    "0",
                    <cfif IsValid("email", form['email']) AND len(form['email']) LT 33>
                        "#form['email']#",
                    <cfelse>
                        "",
                    </cfif>

                    "#program4#",
                    "#subprogram#",
                    "0",
                    "0",
                    "#now_date#",
                    "",
                    "0",
                    "N"
                   )
        </cfquery>
    </cfif>
    <!--- birthday --->
    <cfquery name="q_create_prof" datasource="#application.dsn#">
        INSERT INTO app_proftmp_rec
               (id, birth_date, church_id, prof_last_upd_date)
        VALUES ("#lookup_apptmp_no.apptmp_no#",
                "#birthdate#",
                "0",
                "#now_date#"
                )
    </cfquery>

    <!--- schools loop --->
    <cfloop from="1" to="#form.schoolcount#" index="i">
        <cfset formtest = 'school_name' & i />
        <cfif StructKeyExists(form,formtest)>
            <cfset tmp="#form['school_name' & i]#">
            <cftry>
                <cfset attend_from = CreateDate(form['att_from_year' & i], form['att_from_month' & i], 1) />
                <cfcatch type="any"><cfset attend_from = CreateDate(1900,1,1) /></cfcatch>
            </cftry>
            <cftry>
                <cfset attend_to = CreateDate(form['att_to_year' & i], form['att_to_month' & i], 1) />
                <cfcatch type="any"><cfset attend_to = CreateDate(1900,1,1) /></cfcatch>
            </cftry>
            <cftry>
                <cfset gradDate = CreateDate(form['grad_year' & i], form['grad_month' & i], 1) />
                <cfcatch type="any"><cfset gradDate = CreateDate(1900,1,1) /></cfcatch>
            </cftry>

            <cfquery name="add_school" datasource="#application.dsn#">
                INSERT INTO app_edtmp_rec
                    (id, ceeb, fullname, city, st, enr_date, dep_date, grad_date,
                    stu_id, sch_id, app_reltmp_no, rel_id,priority, zip, aa,
                        ctgry)
                VALUES(
                    '#lookup_apptmp_no.apptmp_no#',
                    '#form["school_code" & i]#',
                    '#form["school_name" & i]#',
                    '#form["school_city" & i]#',
                    '#form["school_state" & i]#',
                    '#attend_from#',
                    '#attend_to#',
                    '#gradDate#',
                    0,0,0,0,0,"", "ac","COL")
            </cfquery>
        </cfif>
    </cfloop>

    <cfcatch type="any">
        error handling
    </cfcatch>
</cftry>

   <!--- record payment information to Informix --->
    <cfquery name="q_payment" datasource="#application.dsn#">
        UPDATE apptmp_rec
        SET 
            payment_method = "#form.payment_type#",
            stat = "H"
        WHERE 
            apptmp_no = "#lookup_apptmp_no.apptmp_no#"
    </cfquery>

