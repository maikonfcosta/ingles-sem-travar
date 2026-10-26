from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / 'artifacts'
ARTIFACTS.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto((ROOT / 'index.html').as_uri())
    assert page.locator('.day').count() == 28
    totals = page.locator('.day').evaluate_all("cards => cards.map(c => [...c.querySelectorAll('[data-min]')].reduce((n, el) => n + Number(el.dataset.min), 0))")
    assert totals == [30] * 28, totals
    assert page.locator('.check').count() == 4
    page.get_by_role('checkbox', name='Concluir dia 1', exact=True).check()
    page.locator('#notes-0').fill('Teste de persistência: confiança 3/5.')
    page.reload()
    assert page.get_by_role('checkbox', name='Concluir dia 1', exact=True).is_checked()
    assert 'confiança 3/5' in page.locator('#notes-0').input_value()
    with page.expect_download() as download:
        page.get_by_role('button', name='Exportar progresso').click()
    data = json.loads(Path(download.value.path()).read_text(encoding='utf-8'))
    assert data['done']['1'] is True
    page.get_by_role('checkbox', name='Concluir dia 1', exact=True).uncheck()
    page.once('dialog', lambda dialog: dialog.accept())
    page.locator('#file').set_input_files({'name': 'progress.json', 'mimeType': 'application/json', 'buffer': json.dumps(data).encode()})
    page.wait_for_function("document.querySelector('[data-done=\"1\"]').checked")
    page.get_by_role('button', name='02 · Descrever').click()
    assert page.locator('.week:visible').count() == 1
    page.emulate_media(media='print')
    assert page.locator('.week:visible').count() == 4
    assert page.locator('.day:visible').count() == 28
    assert 'confiança 3/5' in page.locator('.printed-notes').first.inner_text()
    page.emulate_media(media='screen')
    page.get_by_role('button', name='Todas as semanas').click()
    page.set_viewport_size({'width': 390, 'height': 844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.screenshot(path=str(ARTIFACTS / 'mobile.png'), full_page=True)
    page.evaluate('localStorage.clear()')
    page.reload()
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.screenshot(path=str(ARTIFACTS / 'desktop.png'), full_page=True)
    page.emulate_media(media='print')
    page.pdf(path=str(ARTIFACTS / 'ingles-sem-travar.pdf'), prefer_css_page_size=True, print_background=True)
    assert not errors, errors
    browser.close()
print('PASS: 28 days × 30 min; four checks; persistence; export/import; filters; print; mobile; no JS errors.')
