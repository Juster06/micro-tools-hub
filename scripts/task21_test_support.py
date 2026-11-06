"""Explicit later-batch allowance for historical preservation reconstructions."""
IDS={'hashtag-counter','html-formatter','css-minifier','javascript-minifier','html-to-markdown','html-previewer'}
from task22_test_support import COUNTS,without_task22

def assert_transition(case,old,new):
    case.assertIn(old['id'],IDS)
    case.assertEqual((old['status'],new['status']),('PLANNED','RELEASED'))
    case.assertEqual(new['testing_status'],'REQUIRED_PASSED')
    v=new['verification'];publication=v['publication']
    case.assertEqual(v['source_revision'],'9fa032140639550abd9a0449ed7ef5198354bd40')
    case.assertEqual(publication['url'],'https://everydaydigitalbox.com/'+new['directory_path']+'/')
    case.assertEqual(publication['http_status'],200);case.assertIs(publication['source_matches'],True)
    case.assertTrue(publication['checked_at']);case.assertTrue(v['evidence_path'].endswith('_RELEASE_VERIFICATION.json'))
    for key in ['id','name','category','description','directory_path','priority','implementation_complexity','required_features','related_tools','sequence_rank']:
        case.assertEqual(old[key],new[key],key)

def without_cards(case,source,Homepage):
    source=without_task22(case,source,Homepage)
    for tid in sorted(IDS):
        cards=[c for c in Homepage(source).cards if c['attrs'].get('data-tool-id')==tid]
        case.assertEqual(len(cards),1)
        card=cards[0]
        case.assertEqual(card['attrs']['href'],tid+'/index.html')
        case.assertEqual(card['attrs']['data-availability'],'released')
        case.assertEqual(source[card['start']:card['end']].count('Live'),1)
        case.assertEqual(source[card['start']-2:card['start']],'  ')
        case.assertEqual(source[card['end']:card['end']+7],'\n      ')
        source=source[:card['start']-2]+source[card['end']+7:]
    return source
