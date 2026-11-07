"""Strict Task22 allowance when reconstructing historical batch baselines."""
ID='markdown-converter-previewer'
COUNTS={'RELEASED':75,'TESTED':0,'READY':0,'PLANNED':17,'BLOCKED':1}
def assert_unchanged_or_task22(case,old,new):
    if old['id']!=ID:
        case.assertEqual(old,new,old['id']);return
    case.assertEqual((old['status'],new['status'],new['testing_status']),('PLANNED','RELEASED','REQUIRED_PASSED'))
    case.assertEqual(new['verification']['source_revision'],'64a19c6bc1ee2dfbd81cf9ffa6b1ca00f15c8140')
    publication=new['verification']['publication'];case.assertEqual(publication['http_status'],200);case.assertIs(publication['source_matches'],True);case.assertEqual(publication['url'],'https://everydaydigitalbox.com/'+ID+'/')
    case.assertEqual(new['verification']['evidence_path'],'audit/MARKDOWN_CONVERTER_PREVIEWER_RELEASE_VERIFICATION.json')
    for key in set(old)-{'status','testing_status','last_verification_date','dependencies','notes','verification'}:
        case.assertEqual(old[key],new[key],key)
def without_task22(case,source,Homepage):
    from task24_test_support import without_task24
    source=without_task24(source,Homepage)
    cards=[c for c in Homepage(source).cards if c['attrs'].get('data-tool-id')==ID]
    case.assertEqual(len(cards),1);card=cards[0]
    case.assertEqual(card['attrs']['href'],ID+'/index.html');case.assertEqual(card['attrs']['data-availability'],'released')
    case.assertEqual(source[card['start']:card['end']].count('Live'),1)
    case.assertEqual(source[card['start']-2:card['start']],'  ');case.assertEqual(source[card['end']:card['end']+7],'\n      ')
    source=source[:card['start']-2]+source[card['end']+7:]
    home=Homepage(source);start,end=home.counts[0];case.assertEqual(source[start:end],'75 tools ready to use')
    return source[:start]+'74 tools ready to use'+source[end:]
