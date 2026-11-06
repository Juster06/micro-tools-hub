"""Explicit later-batch allowance for historical preservation reconstructions."""
IDS={'hashtag-counter','html-formatter','css-minifier','javascript-minifier','html-to-markdown','html-previewer'}
COUNTS={'RELEASED':68,'TESTED':6,'READY':0,'PLANNED':18,'BLOCKED':1}

def assert_transition(case,old,new):
    case.assertIn(old['id'],IDS)
    case.assertEqual((old['status'],new['status']),('PLANNED','TESTED'))
    case.assertEqual(new['testing_status'],'REQUIRED_PASSED')
    case.assertIsNone(new['verification']['publication'])
    for key in ['id','name','category','description','directory_path','priority','implementation_complexity','required_features','related_tools','sequence_rank']:
        case.assertEqual(old[key],new[key],key)

def without_cards(case,source,Homepage):
    for tid in sorted(IDS):
        cards=[c for c in Homepage(source).cards if c['attrs'].get('data-tool-id')==tid]
        case.assertEqual(len(cards),1)
        card=cards[0]
        case.assertEqual(card['attrs']['href'],tid+'/index.html')
        case.assertEqual(card['attrs']['data-availability'],'tested')
        case.assertIn('Tested · publication pending',source[card['start']:card['end']])
        case.assertEqual(source[card['start']-2:card['start']],'  ')
        case.assertEqual(source[card['end']:card['end']+7],'\n      ')
        source=source[:card['start']-2]+source[card['end']+7:]
    return source
