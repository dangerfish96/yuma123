#include <libxml/xmlstring.h>
#include <string.h>
#include <assert.h>
#include "procdefs.h"
#include "dlq.h"
#include "ncx.h"
#include "ncxmod.h"
#include "ncxtypes.h"
#include "status.h"
#include "rpc.h"

status_t val_set_cplxval_obj(val_value_t *val, obj_template_t *obj, char* xmlstr);
status_t val_set_cplxval_obj_recursive(val_value_t *val, obj_template_t *obj, xmlDocPtr doc, xmlNode *top);
