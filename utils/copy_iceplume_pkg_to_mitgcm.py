


import os
import shutil
import argparse

######################################################################
# All of these functions are for adding the pkg into the boot sequence

def add_new_lines(lines,indicator,skip_line,add_lines):
    for ll in range(len(lines)):
        line = lines[ll]
        if line[:len(indicator)] == indicator:
            line_split_number = ll + skip_line + 1
    new_lines = lines[:line_split_number] + add_lines + lines[line_split_number:]
    return(new_lines)

def update_PARAMS(inc_dir, code_path):

    if 'PARAMS.h' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(inc_dir,'PARAMS.h'),
                        os.path.join(code_path,'PARAMS.h'))

    f=open(os.path.join(code_path,'PARAMS.h'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'useICEPLUME' in line:
            pkg_already_added = True

    if not pkg_already_added:
        print('      - Adding iceplume pkg to PARAMS.h')
        # add the note to the chain
        indicator = '      LOGICAL useICEFRONT'
        skip_line = 0
        add_lines = ['      LOGICAL useICEPLUME']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the note to the chain
        indicator = '     &        useStreamIce, useICEFRONT, useThSIce, useLand,'
        skip_line = 0
        add_lines = ['     &        useICEPLUME,']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'PARAMS.h'),'w')
        g.write(output)
        g.close()
    else:
        print('      - Skipping addition to PARAMS.h - already implemented')

    return(pkg_already_added)

def update_packages_boot(src_dir, code_path):

    if 'packages_boot.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'packages_boot.F'),
                        os.path.join(code_path,'packages_boot.F'))

    f=open(os.path.join(code_path,'packages_boot.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ALLOW_ICEPLUME' in line:
            pkg_already_added = True

    if not pkg_already_added:

        # add the note to the chain
        indicator = '     &          useICEFRONT,'
        skip_line = 0
        add_lines = ['     &          useIceplume,']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the note to the chain
        indicator = '      useICEFRONT     =.FALSE.'
        skip_line = 0
        add_lines = ['      useIceplume     =.FALSE.']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '      CALL PACKAGES_PRINT_MSG( useICEFRONT'
        skip_line = 1
        add_lines = ['#ifdef ALLOW_ICEPLUME',
                     '      CALL PACKAGES_PRINT_MSG( useIceplume,   \'Iceplume\',    \' \' )',
                     '#endif']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'packages_boot.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to packages_boot - already implemented')

def update_packages_check(src_dir, code_path):

    if 'packages_check.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'packages_check.F'),
                        os.path.join(code_path,'packages_check.F'))

    f=open(os.path.join(code_path,'packages_check.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME_CHECK' in line:
            pkg_already_added = True

    if not pkg_already_added:

        # add the note to the chain
        indicator = 'C       |-- ICEFRONT_CHECK'
        skip_line = 0
        add_lines = ['C       |','C       |-- ICEPLUME_CHECK']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '      IF (useICEFRONT) CALL ICEFRONT_CHECK( myThid )'
        skip_line = 3
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF (useICEPLUME) CALL ICEPLUME_CHECK( myThid )',
                     '#else',
                     '      IF (useICEPLUME) CALL PACKAGES_ERROR_MSG(\'ICEPLUME\',\' \',myThid)',
                     '#endif']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'packages_check.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to packages_readparms - already implemented')

def update_packages_init_fixed(src_dir, code_path):

    if 'packages_init_fixed.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'packages_init_fixed.F'),
                        os.path.join(code_path,'packages_init_fixed.F'))

    f=open(os.path.join(code_path,'packages_init_fixed.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME_INIT_FIXED' in line:
            pkg_already_added = True

    if not pkg_already_added:
        # add the note to the chain
        indicator = 'C       |-- ICEFRONT_INIT_FIXED'
        skip_line = 1
        add_lines = ['C       |-- ICEPLUME_INIT_FIXED','C       |']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '        CALL ICEFRONT_INIT_FIXED( myThid )'
        skip_line = 2
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF (useIceplume) THEN',
                     '        CALL ICEPLUME_INIT_FIXED( myThid )',
                     '      ENDIF',
                     '#endif',]
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'packages_init_fixed.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to packages_init_fixed - already implemented')

def update_packages_init_variables(src_dir, code_path):

    if 'packages_init_variables.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'packages_init_variables.F'),
                        os.path.join(code_path,'packages_init_variables.F'))

    f=open(os.path.join(code_path,'packages_init_variables.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME_INIT_VARIA' in line:
            pkg_already_added = True

    if not pkg_already_added:

        # add the note to the chain
        indicator = 'C       |-- ICEFRONT_INIT_VARIA'
        skip_line = 0
        add_lines = ['C       |','C       |-- ICEPLUME_INIT_VARIA']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '#endif /* ALLOW_ICEFRONT */'
        skip_line = 0
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF ( useICEPLUME ) THEN',
                     '        CALL ICEPLUME_INIT_VARIA( myThid )',
                     '      ENDIF',
                     '#endif /* ALLOW_ICEPLUME */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'packages_init_variables.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to packages_init_variables - already implemented')

def update_packages_readparms(src_dir, code_path):

    if 'packages_readparms.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'packages_readparms.F'),
                        os.path.join(code_path,'packages_readparms.F'))

    f=open(os.path.join(code_path,'packages_readparms.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME_READPARMS' in line:
            pkg_already_added = True

    if not pkg_already_added:

        # add the note to the chain
        indicator = 'C       |-- ICEFRONT_READPARMS'
        skip_line = 0
        add_lines = ['C       |','C       |-- ICEPLUME_READPARMS']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '      CALL ICEFRONT_READPARMS( myThid )'
        skip_line = 1
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     'C--   if useIceplume=T, set ICEPLUME parameters; otherwise just return',
                     '      CALL ICEPLUME_READPARMS( myThid )',
                     '#endif']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'packages_readparms.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to packages_readparms - already implemented')

def update_boot_sequence_files(mitgcm_path, code_path):

    inc_dir = os.path.join(mitgcm_path,'model','inc')
    src_dir = os.path.join(mitgcm_path, 'model', 'src')

    pkg_already_added = update_PARAMS(inc_dir, code_path)

    print('      - Adding a block to the package boot sequence')
    update_packages_boot(src_dir, code_path)

    # print('      - Adding a block to the package check sequence')
    update_packages_check(src_dir, code_path)

    # print('      - Adding a block to the package init_fixed sequence')
    update_packages_init_fixed(src_dir, code_path)

    # print('      - Adding a block to the package init_variables sequence')
    update_packages_init_variables(src_dir, code_path)

    # print('      - Adding a block to the package readparms sequence')
    update_packages_readparms(src_dir, code_path)

    return(pkg_already_added)


######################################################################
# All of these functions are for adding the pkg into other model files

def update_apply_forcing(src_dir, code_path):

    if 'apply_forcing.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'apply_forcing.F'),
                        os.path.join(code_path,'apply_forcing.F'))

    f=open(os.path.join(code_path,'apply_forcing.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME' in line:
            pkg_already_added = True

    if not pkg_already_added:
        print('      - Adding a block to the apply_forcing sequence')

        # theres two sections so doing this manually
        for ll in range(len(lines)):
            line = lines[ll]
            if line[:len('      SUBROUTINE APPLY_FORCING_T(')] == '      SUBROUTINE APPLY_FORCING_T(':
                apply_forcing_t_start = ll
            if line[:len('      SUBROUTINE APPLY_FORCING_S(')] == '      SUBROUTINE APPLY_FORCING_S(':
                apply_forcing_s_start = ll

        pre_lines = lines[:apply_forcing_t_start]
        t_lines = lines[apply_forcing_t_start:apply_forcing_s_start]
        s_lines = lines[apply_forcing_s_start:]

        # add the check code
        indicator = '#include "SURFACE.h"'
        skip_line = 0
        add_lines = ['#ifdef ALLOW_ICEPLUME',
                     '#include "ICEPLUME.h"',
                     '#endif /* ALLOW_ICEPLUME */']
        t_lines = add_new_lines(t_lines, indicator, skip_line, add_lines)
        s_lines = add_new_lines(s_lines, indicator, skip_line, add_lines)

        indicator = '#ifdef ALLOW_ADDFLUID'
        skip_line = 0
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF ( useICEPLUME ) THEN',
                     '       IF ( selectAddFluid.NE.0) THEN',
                     '        IF ( ( selectAddFluid.GE.1 .AND. nonlinFreeSurf.GT.0 )',
                     '     &      .OR. convertFW2Salt.EQ.-1. _d 0 ) THEN',
                     '         DO j=0,sNy+1',
                     '          DO i=0,sNx+1',
                     '           tmpVar(i,j)=',
                     '     &          addMass3Dplume(i,j,k,bi,bj)*mass2rUnit',
                     '     &          *(temp_addMass3Dplume(I,J,k,bi,bj)-theta(i,j,k,bi,bj))',
                     '     &          *recip_rA(i,j,bi,bj)',
                     '     &          *recip_drF(k)*_recip_hFacC(i,j,k,bi,bj)',
                     '           gT_arr(i,j) = gT_arr(i,j) + tmpVar(i,j)',
                     '          ENDDO',
                     '         ENDDO',
                     '       ELSE',
                     '         DO j=0,sNy+1',
                     '          DO i=0,sNx+1',
                     '           tmpVar(i,j)=',
                     '     &          addMass3Dplume(i,j,k,bi,bj)*mass2rUnit',
                     '     &          *( temp_addMass3Dplume(I,J,k,bi,bj) - tRef(k) )',
                     '     &          *recip_rA(i,j,bi,bj)',
                     '     &          *recip_drF(k)*_recip_hFacC(i,j,k,bi,bj)',
                     '           gT_arr(i,j) = gT_arr(i,j) + tmpVar(i,j)',
                     '          ENDDO',
                     '         ENDDO',
                     '        ENDIF',
                     '       ENDIF',
                     '      ENDIF',
                     '#else /* ALLOW_ICEPLUME */',
                     '']
        t_lines = add_new_lines(t_lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '#endif /* ALLOW_ADDFLUID */'
        skip_line = -1
        add_lines = ['#endif /* ALLOW_ICEPLUME */']
        t_lines = add_new_lines(t_lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '     &     CALL ICEFRONT_TENDENCY_APPLY_T('
        skip_line = 3
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF ( useICEPLUME )',
                     '     &     CALL ICEPLUME_TENDENCY_APPLY_T(',
                     '     U                   gT_arr,',
                     '     I                   iMin,iMax,jMin,jMax,',
                     '     I                   k, bi, bj, myTime, myIter, myThid )',
                     '#endif /* ALLOW_ICEPLUME */']
        t_lines = add_new_lines(t_lines, indicator, skip_line, add_lines)

        indicator = '#ifdef ALLOW_ADDFLUID'
        skip_line = 0
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF ( useICEPLUME ) THEN',
                     '       IF ( selectAddFluid.NE.0) THEN',
                     '        IF ( ( selectAddFluid.GE.1 .AND. nonlinFreeSurf.GT.0 )',
                     '     &      .OR. convertFW2Salt.EQ.-1. _d 0 ) THEN',
                     '         DO j=0,sNy+1',
                     '          DO i=0,sNx+1',
                     '           tmpVar(i,j) =',
                     '     &          addMass3Dplume(i,j,k,bi,bj)*mass2rUnit',
                     '     &          *( salt_addMass3Dplume(I,J,k,bi,bj)-salt(i,j,k,bi,bj) )',
                     '     &          *recip_rA(i,j,bi,bj)',
                     '     &          *recip_drF(k)*_recip_hFacC(i,j,k,bi,bj)',
                     '           gS_arr(i,j) = gS_arr(i,j) + tmpVar(i,j)',
                     '          ENDDO',
                     '         ENDDO',
                     '       ELSE',
                     '         DO j=0,sNy+1',
                     '          DO i=0,sNx+1',
                     '           tmpVar(i,j) =',
                     '     &          addMass3Dplume(i,j,k,bi,bj)*mass2rUnit',
                     '     &          *( salt_addMass3Dplume(I,J,k,bi,bj) - sRef(k) )',
                     '     &          *recip_rA(i,j,bi,bj)',
                     '     &          *recip_drF(k)*_recip_hFacC(i,j,k,bi,bj)',
                     '           gS_arr(i,j) = gS_arr(i,j) + tmpVar(i,j)',
                     '          ENDDO',
                     '         ENDDO',
                     '        ENDIF',
                     '       ENDIF',
                     '      ENDIF',
                     '#else /* ALLOW_ICEPLUME */',
                     '']
        s_lines = add_new_lines(s_lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '#endif /* ALLOW_ADDFLUID */'
        skip_line = -1
        add_lines = ['#endif /* ALLOW_ICEPLUME */']
        s_lines = add_new_lines(s_lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '     &     CALL ICEFRONT_TENDENCY_APPLY_S('
        skip_line = 3
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF ( useICEPLUME )',
                     '     &     CALL ICEPLUME_TENDENCY_APPLY_S(',
                     '     U                   gS_arr,',
                     '     I                   iMin,iMax,jMin,jMax,',
                     '     I                   k, bi, bj, myTime, myIter, myThid )',
                     '#endif /* ALLOW_ICEPLUME */']
        s_lines = add_new_lines(s_lines, indicator, skip_line, add_lines)

        lines = pre_lines+t_lines+s_lines

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'apply_forcing.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to apply_forcing - already implemented')

def update_external_forcing(src_dir, code_path):

    if 'external_forcing.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'external_forcing.F'),
                        os.path.join(code_path,'external_forcing.F'))

    f=open(os.path.join(code_path,'external_forcing.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME' in line:
            pkg_already_added = True

    if not pkg_already_added:
        print('      - Adding a block to the external_forcing sequence')

        # theres two sections so doing this manually
        for ll in range(len(lines)):
            line = lines[ll]
            if line[:len('      SUBROUTINE EXTERNAL_FORCING_T(')] == '      SUBROUTINE EXTERNAL_FORCING_T(':
                external_t_start = ll
            if line[:len('      SUBROUTINE EXTERNAL_FORCING_S(')] == '      SUBROUTINE EXTERNAL_FORCING_S(':
                external_s_start = ll

        pre_lines = lines[:external_t_start]
        t_lines = lines[external_t_start:external_s_start]
        s_lines = lines[external_s_start:]

        # add the check code
        indicator = '#include "SURFACE.h"'
        skip_line = 0
        add_lines = ['#ifdef ALLOW_ICEPLUME',
                     '#include "ICEPLUME.h"',
                     '#endif /* ALLOW_ICEPLUME */']
        t_lines = add_new_lines(t_lines, indicator, skip_line, add_lines)
        s_lines = add_new_lines(s_lines, indicator, skip_line, add_lines)

        indicator = '#ifdef ALLOW_ADDFLUID'
        skip_line = 0
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '       DO j=1,sNy',
                     '        DO i=1,sNx',
                     '         tmpVar(i,j)=0. _d 0',
                     '        ENDDO',
                     '       ENDDO',
                     '       IF ( useICEPLUME ) THEN',
                     '        IF ( selectAddFluid.NE.0 ) THEN',
                     '         IF ( ( selectAddFluid.GE.1 .AND. nonlinFreeSurf.GT.0 )',
                     '      &      .OR. convertFW2Salt.EQ.-1. _d 0 ) THEN',
                     '          DO j=1,sNy',
                     '           DO i=1,sNx',
                     '             tmpVar(i,j) =',
                     '      &        addMass3Dplume(i,j,kLev,bi,bj)*mass2rUnit',
                     '      &        *(temp_addMass3D(I,J,Klev,bi,bj)-theta(i,j,kLev,bi,bj) )',
                     '      &          *recip_rA(i,j,bi,bj)',
                     '      &          *recip_drF(kLev)*_recip_hFacC(i,j,kLev,bi,bj)',
                     '             gT(i,j,klev,bi,bj) = gT(i,j,klev,bi,bj) + tmpVar(i,j)',
                     '           ENDDO',
                     '          ENDDO',
                     '         ELSE',
                     '          DO j=1,sNy',
                     '           DO i=1,sNx',
                     '             tmpVar(i,j) = ',
                     '      &        addMass3Dplume(i,j,kLev,bi,bj)*mass2rUnit',
                     '      &          *( temp_addMass3D(I,J,Klev,bi,bj) - tRef(kLev) )',
                     '      &          *recip_rA(i,j,bi,bj)',
                     '      &          *recip_drF(kLev)*_recip_hFacC(i,j,kLev,bi,bj)',
                     '             gT(i,j,klev,bi,bj) = gT(i,j,klev,bi,bj) + tmpVar(i,j)',
                     '           ENDDO',
                     '          ENDDO',
                     '         ENDIF',
                     '        ENDIF',
                     '       ENDIF',
                     '#else /* ALLOW_ICEPLUME */',
                     '']
        t_lines = add_new_lines(t_lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '#endif /* ALLOW_ADDFLUID */'
        skip_line = -1
        add_lines = ['#endif /* ALLOW_ICEPLUME */']
        t_lines = add_new_lines(t_lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '     &     CALL ICEFRONT_TENDENCY_APPLY_T('
        skip_line = 3
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF ( useICEPLUME )',
                     '     &     CALL ICEPLUME_TENDENCY_APPLY_T(',
                     '     U                   gT(1-OLx,1-OLy,kLev,bi,bj),',
                     '     I                   iMin,iMax,jMin,jMax,',
                     '     I                   kLev, bi, bj, myTime, 0, myThid )',
                     '#endif /* ALLOW_ICEPLUME */']
        t_lines = add_new_lines(t_lines, indicator, skip_line, add_lines)

        indicator = '#ifdef ALLOW_ADDFLUID'
        skip_line = 0
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '       DO j=0,sNy+1',
                     '        DO i=0,sNx+1',
                     '         tmpVar(i,j)=0. _d 0',
                     '        ENDDO',
                     '       ENDDO',
                     '       IF ( useICEPLUME ) THEN',
                     '        IF ( selectAddFluid.NE.0 ) THEN',
                     '         IF ( ( selectAddFluid.GE.1 .AND. nonlinFreeSurf.GT.0 )',
                     '      &      .OR. convertFW2Salt.EQ.-1. _d 0 ) THEN',
                     '          DO j=1,sNy',
                     '           DO i=1,sNx',
                     '             tmpVar(i,j) = ',
                     '      &        addMass3Dplume(i,j,kLev,bi,bj)*mass2rUnit',
                     '      &        *( salt_addMass3D(I,J,Klev,bi,bj) - salt(i,j,kLev,bi,bj) )',
                     '      &        *recip_rA(i,j,bi,bj)',
                     '      &        *recip_drF(kLev)*_recip_hFacC(i,j,kLev,bi,bj)',
                     '             gS(i,j,klev,bi,bj)=gS(i,j,k,bi,bj) + tmpVar(i,j)',
                     '           ENDDO',
                     '          ENDDO',
                     '         ELSE',
                     '          DO j=1,sNy',
                     '           DO i=1,sNx',
                     '             tmpVar(i,j) =',
                     '      &        addMass3Dplume(i,j,kLev,bi,bj)*mass2rUnit',
                     '      &          *( salt_addMass3D(I,J,Klev,bi,bj) - sRef(kLev) )',
                     '      &          *recip_rA(i,j,bi,bj)',
                     '      &          *recip_drF(kLev)*_recip_hFacC(i,j,kLev,bi,bj)',
                     '             gS(i,j,klev,bi,bj)=gS(i,j,klev,bi,bj) + tmpVar(i,j)',
                     '           ENDDO',
                     '          ENDDO',
                     '         ENDIF',
                     '        ENDIF',
                     '       ENDIF',
                     '#else /* ALLOW_ICEPLUME */',
                     '']
        s_lines = add_new_lines(s_lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '#endif /* ALLOW_ADDFLUID */'
        skip_line = -1
        add_lines = ['#endif /* ALLOW_ICEPLUME */']
        s_lines = add_new_lines(s_lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '     &     CALL ICEFRONT_TENDENCY_APPLY_S('
        skip_line = 3
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF ( useICEPLUME )',
                     '     &     CALL ICEPLUME_TENDENCY_APPLY_S(',
                     '     U                   gS(1-OLx,1-OLy,kLev,bi,bj),',
                     '     I                   iMin,iMax,jMin,jMax,',
                     '     I                   kLev, bi, bj, myTime, 0, myThid )',
                     '#endif /* ALLOW_ICEPLUME */']
        s_lines = add_new_lines(s_lines, indicator, skip_line, add_lines)

        lines = pre_lines+t_lines+s_lines

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'external_forcing.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to external - already implemented')

def update_do_oceanic_phys(src_dir, code_path):

    if 'do_oceanic_phys.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'do_oceanic_phys.F'),
                        os.path.join(code_path,'do_oceanic_phys.F'))

    f=open(os.path.join(code_path,'do_oceanic_phys.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME' in line:
            pkg_already_added = True

    if not pkg_already_added:
        print('      - Adding a block to the do_oceanic_phys sequence')

        # add the check code
        indicator = '#endif /* ALLOW_ICEFRONT */'
        skip_line = 0
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF ( useICEPLUME .AND. fluidIsWater ) THEN',
                     '        CALL TIMER_START(\'ICEPLUME [DO_OCEANIC_PHYS]\', myThid)',
                     '        CALL ICEPLUME_CALC ( myTime, myIter, myThid )',
                     '        CALL TIMER_STOP (\'ICEPLUME [DO_OCEANIC_PHYS]\', myThid)',
                     '      ENDIF',
                     '#endif /* ALLOW_ICEPLUME */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'do_oceanic_phys.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to do_oceanic_phys - already implemented')

def update_exf_filter_runoffqsg(src_dir, code_path):
    print('Update me')
    print('exf_filter_runoffqsg.F should be updated when using iceplume with shelfice')
    print('also exf_set_fld.F')

def update_exf_getffields(exf_dir, code_path):

    if 'exf_getffields.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(exf_dir,'exf_getffields.F'),
                        os.path.join(code_path,'exf_getffields.F'))

    f=open(os.path.join(code_path,'exf_getffields.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME' in line:
            pkg_already_added = True

    if not pkg_already_added:
        print('      - Adding a block to the exf_getffields sequence')

        # add the check code
        indicator = '#include "EXF_FIELDS.h"'
        skip_line = 0
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '#include "ICEPLUME.h"',
                     '#endif /* ALLOW_ICEPLUME */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '#endif /* ALLOW_RUNOFTEMP */'
        skip_line = 0
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF (useICEPLUME) THEN',
                     '      CALL EXF_SET_FLD(',
                     '     I     \'runoffQsg\', runoffQsgfile, runoffQsgmask,',
                     '     I     runoffQsgStartTime, runoffQsgperiod, runoffQsgRepCycle,',
                     '     I     runoffQsg_inscal,',
                     '     I     runoffQsg_remov_intercept, runoffQsg_remov_slope,',
                     '     U     runoffQsg, runoffQsg0, runoffQsg1,',
                     '#ifdef USE_EXF_INTERPOLATION',
                     '     I     runoffQsg_lon0, runoffQsg_lon_inc,',
                     '     I     runoffQsg_lat0, runoffQsg_lat_inc,',
                     '     I     runoffQsg_nlon, runoffQsg_nlat, xC, yC, ',
                     '     I     runoffQsg_interpMethod,',
                     '#endif',
                     '     I     myTime, myIter, myThid )',
                     '      ENDIF',
                     '#endif /* ALLOW_ICEPLUME */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'exf_getffields.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to exf_getffields - already implemented')

def update_external_fields_load(src_dir, code_path):

    if 'external_fields_load.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'external_fields_load.F'),
                        os.path.join(code_path,'external_fields_load.F'))

    f=open(os.path.join(code_path,'external_fields_load.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME' in line:
            pkg_already_added = True

    if not pkg_already_added:
        print('      - Adding a block to the external_fields_load sequence')

        # add the check code
        indicator = '#include "DYNVARS.h"'
        skip_line = 0
        add_lines = ['#ifdef ALLOW_ICEPLUME',
                     '#include "ICEPLUME.h"',
                     '#endif /* ALLOW_ICEPLUME */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '         CALL READ_REC_XY_RS( pLoadFile, pLoad0,'
        skip_line = 5
        add_lines = ['',
                     '#ifdef ALLOW_ICEPLUME',
                     '      IF (useICEPLUME) THEN',
                     '       IF ( runoffQsgfile .NE. ' ') THEN',
                     '        CALL READ_REC_XY_RL(',
                     '     &     runoffQsgFile,runoffQsg0,inTime0,myIter,myThid)',
                     '        CALL READ_REC_XY_RL(',
                     '     &     runoffQsgFile,runoffQsg1,inTime1,myIter,myThid)',
                     '       ENDIF',
                     '      ENDIF',
                     '#endif /* ALLOW_ICEPLUME */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'external_fields_load.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to external_fields_load - already implemented')

def update_ini_parms(src_dir, code_path):

    if 'ini_parms.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(src_dir,'ini_parms.F'),
                        os.path.join(code_path,'ini_parms.F'))

    f=open(os.path.join(code_path,'ini_parms.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ICEPLUME' in line:
            pkg_already_added = True

    if not pkg_already_added:
        print('      - Adding a block to the ini_parms sequence')

        # add the check code
        indicator = 'C--   For backward compatibility, set temp_addMass and salt_addMass'
        skip_line = -1
        add_lines = ['',
                     '#ifndef ALLOW_ICEPLUME']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = 'C--   For backward compatibility, set temp_addMass and salt_addMass'
        skip_line = 3
        add_lines = ['#else',
                     '      temp_addMass = UNSET_RL',
                     '      salt_addMass = UNSET_RL',
                     '#endif /* ALLOW_ICEPLUME */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'ini_parms.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to ini_parms - already implemented')

def update_obcs_balance_flow(obcs_dir, code_path):

    if 'obcs_balance_flow.F' not in os.listdir(code_path):
        shutil.copyfile(os.path.join(obcs_dir,'obcs_balance_flow.F'),
                        os.path.join(code_path,'obcs_balance_flow.F'))

    f=open(os.path.join(code_path,'obcs_balance_flow.F'))
    lines = f.read()
    f.close()
    lines = lines.split('\n')

    pkg_already_added = False
    for line in lines:
        if 'ALLOW_ADDFLUID' in line:
            pkg_already_added = True

    if not pkg_already_added:
        print('      - Adding a block to the obcs_balance_flow sequence')

        # add the check code
        indicator = '      _RL shelfIceNetMassFlux'
        skip_line = 0
        add_lines = ['#ifdef ALLOW_ADDFLUID',
                     '      _RL addMassMassFlux',
                     '#endif /* ALLOW_ADDFLUID */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '#endif /* ALLOW_SHELFICE */'
        skip_line = 0
        add_lines = ['#ifdef ALLOW_ADDFLUID',
                     '      IF ( selectAddFluid.NE.0 ) THEN',
                     '       DO bj=myByLo(myThid),myByHi(myThid)',
                     '        DO bi=myBxLo(myThid),myBxHi(myThid)',
                     '           tileFlow(bi,bj) = 0.',
                     '           DO j=1,sNy',
                     '            DO i=1,sNx',
                     '             DO k=1,Nr ',
                     '             tileFlow(bi,bj) = tileFlow(bi,bj)',
                     '     &          + addMass(i,j,k,bi,bj) * maskInC(i,j,bi,bj)',
                     '             ENDDO',
                     '            ENDDO',
                     '           ENDDO',
                     '         ENDDO',
                     '        ENDDO',
                     '        CALL GLOBAL_SUM_TILE_RL( tileFlow, addMassMassFlux, myThid )',
                     '        IF ( debugLevel.GE.debLevC ) THEN',
                     '          WRITE(msgBuf,\'(A,I9,A,1P1E16.8)\') \'OBCS_balance (it=\'',
                     '     &       myIter, \' ) correct for addMassMassFlux:\',',
                     '     &       addMassMassFlux',
                     '          CALL PRINT_MESSAGE( msgBuf, standardMessageUnit,',
                     '     &       SQUEEZE_RIGHT, myThid )',
                     '        ENDIF',
                     '      ENDIF',
                     '#endif /* ALLOW_ADDFLUID */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        # add the check code
        indicator = '#ifdef ALLOW_SHELFICE'
        skip_line = 3
        add_lines = ['#ifdef ALLOW_ADDFLUID',
                     '         IF ( selectAddFluid.NE.0 )',
                     '     &        inFlow = inFlow + addMassMassFlux*mass2rUnit',
                     '#endif /* ALLOW_ADDFLUID */']
        lines = add_new_lines(lines, indicator, skip_line, add_lines)

        output = '\n'.join(lines)
        g = open(os.path.join(code_path,'obcs_balance_flow.F'),'w')
        g.write(output)
        g.close()

    else:
        print('      - Skipping addition to obcs_balance_flow - already implemented')

def update_model_src_files(mitgcm_path, code_path):

    src_dir = os.path.join(mitgcm_path, 'model', 'src')
    exf_dir = os.path.join(mitgcm_path, 'pkg', 'exf')
    obcs_dir = os.path.join(mitgcm_path, 'pkg', 'obcs')

    update_apply_forcing(src_dir, code_path)

    update_external_forcing(src_dir, code_path)

    update_do_oceanic_phys(src_dir, code_path)

    update_exf_filter_runoffqsg(src_dir, code_path)

    update_exf_getffields(exf_dir, code_path)

    update_external_fields_load(src_dir, code_path)

    update_ini_parms(src_dir, code_path)

    update_obcs_balance_flow(obcs_dir, code_path)


######################################################################
# This function is to add the new package files to the pkg dir

def add_iceplume_package_files(mitgcm_path):

    if 'iceplume' in os.listdir(os.path.join(mitgcm_path,'pkg')):
        shutil.rmtree(os.path.join(mitgcm_path,'pkg','iceplume'))

    os.mkdir(os.path.join(mitgcm_path,'pkg','iceplume'))

    for file_name in os.listdir(os.path.join('..','pkg','iceplume')):
        if file_name[-1]=='F':
            shutil.copyfile(os.path.join('..', 'pkg', 'iceplume', file_name),
                       os.path.join(mitgcm_path, 'pkg', 'iceplume', file_name))
        if file_name[-1]=='h':
            shutil.copyfile(os.path.join('..', 'pkg', 'iceplume', file_name),
                       os.path.join(mitgcm_path, 'pkg', 'iceplume', file_name))



######################################################################
# This function is the main utility

def copy_files_to_config(mitgcm_path, code_path):
    pwd = os.getcwd()
    pwd_short = pwd.split(os.path.sep)[-1]
    if pwd_short!='utils':
        raise ValueError('Run this code from within the utils dir')

    print(' - Updating the boot sequence files')
    # step 1: edit the old boot sequence files to add the new package
    update_boot_sequence_files(mitgcm_path, code_path)

    print(' - Updating model source files')
    # step 2: edit the other model source files
    update_model_src_files(mitgcm_path, code_path)

    print(' - Copying iceplume files into the pkg directory')
    # step 3: add the new iceplume package
    add_iceplume_package_files(mitgcm_path)

    print(' - Copy successful!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mitgcm_directory", action="store",
                        help="Path to the MITgcm directory.", dest="mitgcm_path",
                        type=str, required=True)

    parser.add_argument("-c", "--code_directory", action="store",
                        help="Path to the code directory of the configuration using iceplume.", dest="code_path",
                        type=str, required=True)

    args = parser.parse_args()
    mitgcm_path = args.mitgcm_path
    code_path = args.code_path

    copy_files_to_config(mitgcm_path, code_path)