/*
 * Copyright (c) 2009, Netconf Central, Inc.
 * 
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.    
 */
/*  FILE: yangdump_util.c

                
*********************************************************************
*                                                                   *
*                  C H A N G E   H I S T O R Y                      *
*                                                                   *
*********************************************************************

date         init     comment
----------------------------------------------------------------------
23-oct-09    abb      begun

*********************************************************************
*                                                                   *
*                     I N C L U D E    F I L E S                    *
*                                                                   *
*********************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

#include <xmlstring.h>

#ifndef _H_procdefs
#include  "procdefs.h"
#endif

#ifndef _H_log
#include  "log.h"
#endif

#ifndef _H_ncx
#include  "ncx.h"
#endif

#ifndef _H_status
#include  "status.h"
#endif

#ifndef _H_yangdump_util
#include  "yangdump_util.h"
#endif


/********************************************************************
*                                                                   *
*                       C O N S T A N T S                           *
*                                                                   *
*********************************************************************/

/********************************************************************
*                                                                   *
*                       V A R I A B L E S                            *
*                                                                   *
*********************************************************************/


/********************************************************************
* write_banner
*
* Write the yangdump startup banner 
*
*********************************************************************/
void 
    write_banner (void)
{
    status_t   res;
    xmlChar    versionbuffer[NCX_VERSION_BUFFSIZE];

    res = ncx_get_version(versionbuffer, NCX_VERSION_BUFFSIZE);
    if (res == NO_ERR) {
        log_write("\n\n*** Generated by yangdump %s",
                  versionbuffer);
        log_write("\n*** ");
        log_write(COPYRIGHT_STRING);
    } else {
        SET_ERROR(res);
    }

}   /* write_banner */

/********************************************************************
* write_banner_session
*
* Write the yangdump startup banner to a session
*
*********************************************************************/
void 
    write_banner_session (ses_cb_t *scb)
{
    status_t   res;
    xmlChar    versionbuffer[NCX_VERSION_BUFFSIZE];

#ifdef DEBUG
    if (scb == NULL) {
        SET_ERROR(ERR_INTERNAL_PTR);
    }
#endif

    res = ncx_get_version(versionbuffer, NCX_VERSION_BUFFSIZE);
    if (res == NO_ERR) {
        ses_putstr(scb, (const xmlChar *)"\n\n*** Generated by yangdump ");
        ses_putstr(scb, versionbuffer);
        ses_putstr(scb, (const xmlChar *)"\n*** ");
        ses_putstr(scb, (const xmlChar *)COPYRIGHT_STRING);
    } else {
        SET_ERROR(res);
    }

}   /* write_banner_session */


/********************************************************************
 * FUNCTION find_reference
 * 
 *   Find the next 'RFC' or 'draft-' string in the buffer
 *   Find the end of the RFC or draft name
 *
 * INPUTS:
 *   buffer == buffer containing reference clause to use
 *   ref == address of return start pointer
 *   reflen == addredd of return 'ref' length
 *
 * OUTPUTS:
 *   *ref == address of start of reference word
 *        == NULL if no RFC xxxx of draft- found
 *   *reflen == number of chars in *ref, or 0 if *ref is NULL
 *
 * RETURNS:
 *   total number of chars processed
 *********************************************************************/
uint32
    find_reference (const xmlChar *buffer,
                    const xmlChar **ref,
                    uint32 *reflen)
{
    const xmlChar  *str, *num, *p;
    uint32          numlen;

#ifdef DEBUG
    if (buffer == NULL || ref == NULL || reflen == NULL) {
        SET_ERROR(ERR_INTERNAL_PTR);
        return 0;
    }
#endif

    *ref = NULL;
    *reflen = 0;

    str = buffer;
    while (*str && xml_isspace(*str)) {
        str++;
    }

    /* check if the reference is to an RFC */
    if (!xml_strncmp(str, (const xmlChar *)"RFC ", 4)) {
        num = &str[4];
        p = num;
        while (*p && isdigit(*p)) {
            p++;
        }
        numlen = (uint32)(p - num);

        /* IETF RFC URLs are currently hard-wired 4 digit number */
        if (numlen > 0 && numlen <= 4) {
            *ref = str;
            *reflen = (uint32)(p - str);
        }
        return (uint32)(p - buffer);
    } else if (!xml_strncmp(str, (const xmlChar *)"draft-", 6)) {
        num = &str[6];
        while (*num && 
               (!xml_isspace(*num)) && 
               (*num != ';') && 
               (*num != ':') &&
               (*num != ',')) {
            num++;
        }

        /* make sure did not end on a dot char */
        if (num != &str[6] && *num == '.') {
            num--;
        }
        numlen = (uint32)(num-str);

        if (numlen > 0) {
            *ref = str;
            *reflen = (uint32)(num-str);
        }
        return (uint32)(num - buffer);
    } else {
        return (uint32)(str - buffer);
    }

}   /* find_reference */


/* END yangdump_util.c */



