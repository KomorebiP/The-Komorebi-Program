/* Integration smoke test of the real generated GitHub Pages Sequence Network.
   Run by sequence-library-checks.yml against the local production preview. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');

async function main(){
  const base=(process.argv[2]||'http://127.0.0.1:8846/').replace(/\/?$/,'/');
  const output=process.argv[3]||'.sequence-checks/reports/network-browser';
  fs.mkdirSync(output,{recursive:true});
  const browser=await chromium.launch({headless:true});
  const failures=[];
  try{
    const page=await browser.newPage({viewport:{width:1150,height:800}});
    page.on('pageerror',e=>failures.push(String(e)));
    const response=await page.goto(base+'sequence-network.html?q=A000108',{waitUntil:'domcontentloaded'});
    assert.equal(response.status(),200,'Generated Network page missing');
    await page.waitForFunction(()=>/connections found/.test(document.querySelector('#sn-status')?.textContent||''),null,{timeout:45000});
    const first=await page.locator('.sn-result').count();
    assert.equal(first,9,'An exact Catalan ID selects only direct transfer records');
    assert.equal(await page.locator('#sn-show-more').isVisible(),false);
    assert.match(await page.locator('.sn-profile').innerText(),/9 distinct direct records.*0 as target.*9 as input/s);
    assert.ok(await page.locator('.sn-profile a[href*="text%3AA000108"]').count());
    assert.ok(await page.locator('.sn-result h3 a[href*="sequence-network.html?q="]').count());
    assert.ok(await page.locator('.sn-result [data-math-latex]').count()>0,
      'At least one transfer must have a readable, accessible mathematical rendering');
    await page.waitForFunction(
      ()=>Boolean(document.querySelector('.sn-result .math-pair mjx-container')),null,{timeout:45000});
    const inspect=async width=>{
      await page.setViewportSize({width,height:844});
      const layout=await page.evaluate(()=>{
        const viewport=document.documentElement.clientWidth;
        const ids=['#sn-query','#sn-form button[type=submit]','#sn-filter','.sn-result'];
        return {viewport,boxes:ids.map(selector=>{
          const box=document.querySelector(selector)?.getBoundingClientRect();
          return {selector,left:box?.left,right:box?.right};
        })};
      });
      for(const box of layout.boxes){
        assert.ok(box.left>=-1 && box.right<=layout.viewport+1,
          'Reflow failed at '+width+'px for '+box.selector+': '+JSON.stringify(layout));
      }
    };
    for(const width of [320,390,768])await inspect(width);
    await page.setViewportSize({width:390,height:844});
    assert.ok(first>0,'Catalan must have archived formula relations');
    assert.ok((await page.locator('#sn-results').innerText()).includes('Formula identity')||
              (await page.locator('#sn-results').innerText()).includes('Gauge transfer'));
    assert.equal(await page.locator('#sn-source-formulas').isVisible(),true);
    await page.locator('#sn-source-load').focus();
    await page.keyboard.press('Enter');
    await page.waitForFunction(()=>document.querySelectorAll('#sn-source-results li').length>0,null,{timeout:45000});
    assert.equal(await page.locator('#sn-source-results li').first().evaluate(el=>document.activeElement===el),true,
      'keyboard focus follows the initial source-formula load');
    assert.match(await page.locator('#sn-source-status').innerText(),/unreviewed OEIS records/);
    assert.match(await page.locator('#sn-source-results').textContent(),/binomial/);
    assert.ok(await page.locator('#sn-source-results [data-math-latex]').count()>0);
    assert.ok(await page.locator('#sn-source-results .sn-copy').count()>0);
    assert.equal(await page.locator('#sn-source-results li').count(),25);
    await page.locator('#sn-source-results li').first().evaluate(el=>{el.dataset.keepOnPagination='yes';});
    await page.locator('#sn-source-more').focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#sn-source-results li').count(),50,
      'archival formula text continues in batches of 25');
    assert.equal(await page.locator('#sn-source-results li').first().getAttribute('data-keep-on-pagination'),'yes',
      'existing archival lines are not removed and recreated');
    assert.equal(await page.locator('#sn-source-results li').nth(25).evaluate(el=>document.activeElement===el),true,
      'keyboard focus follows the first newly disclosed archive line');
    const classes=await page.locator('#sn-source-type option').evaluateAll(options=>options.map(o=>o.value));
    assert.ok(classes.length>1);
    await page.selectOption('#sn-source-type',classes[1]);
    assert.ok((await page.locator('#sn-source-results .sn-source-kind').allTextContents()).every(kind=>kind===classes[1]));
    await page.selectOption('#sn-source-type','all');
    assert.equal(await page.locator('#sn-source-results li').count(),25);
    await page.selectOption('#sn-filter','gauge');
    await page.waitForFunction(()=>Boolean(document.querySelector('.sn-result .sn-definition')));
    const gauge=page.locator('.sn-result').first();
    await gauge.locator('.sn-record-details summary').click();
    assert.match(await gauge.locator('.sn-original').innerText(),/b\(t\)\/a\(t\)/,
      'The original unmodified archival specification remains available');
    assert.ok(await gauge.locator('.sn-parameters dd').count()>=5,
      'The gauge constants and offsets have accessible labels');
    assert.match(await page.locator('#sn-status').innerText(),/connections found/);
    await page.setViewportSize({width:390,height:844});
    await page.screenshot({path:path.join(output,'network-mobile.png')});
    const participant=gauge.locator('h3 a').first();
    const participantId=await participant.innerText();
    await participant.click();
    await page.waitForFunction(id=>document.querySelector('.sn-profile h3')?.textContent.includes(id),participantId,{timeout:45000});
    assert.match(new URL(page.url()).searchParams.get('q'),/^A\d{6}$/);
    assert.ok(await page.locator('.sn-profile').isVisible());
    await page.goto(base+'sequence-network.html?q=text%3AA000108',{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>/17 archived connections found/.test(document.querySelector('#sn-status')?.textContent||''),null,{timeout:45000});
    assert.equal(await page.locator('.sn-profile').count(),0);
    await page.goto(base+'sequence-network.html?q=binomial',{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>/331 archived connections found/.test(document.querySelector('#sn-status')?.textContent||''),null,{timeout:45000});
    assert.match(await page.locator('#sn-status').innerText(),/showing 12 of 331/);
    assert.equal(await page.locator('.sn-result').count(),12);
    await page.locator('#sn-show-more').focus();
    await page.keyboard.press('Enter');
    assert.match(await page.locator('#sn-status').innerText(),/showing 24 of 331/);
    assert.equal(await page.locator('.sn-result').count(),24);
    assert.equal(await page.locator('.sn-result').nth(12).evaluate(el=>document.activeElement===el),true,
      'newly revealed connection receives keyboard focus');
    await page.goto(base+'sequence-network.html?q=KFOR-CF-PAD-1',{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>/connections found/.test(document.querySelector('#sn-status')?.textContent||''),null,{timeout:45000});
    assert.match(await page.locator('#sn-handoffs').innerText(),/finite OEIS matches/);
    assert.ok(await page.locator('#sn-handoffs a[href*="q=A000931"]').count());
    await page.goto(base+'sequence-library.html',{waitUntil:'domcontentloaded'});
    assert.ok(await page.locator('#sl-network-gateway a[href*="sequence-network.html"]').count());
    await page.goto(base+'sequence-transfers.html',{waitUntil:'domcontentloaded'});
    assert.ok(await page.locator('#sl-network-gateway a[href*="sequence-network.html"]').count());
    assert.deepEqual(failures,[],'Uncaught browser errors');
    fs.writeFileSync(path.join(output,'report.json'),JSON.stringify({status:'passed',catalan_relations:first,
      local_handoff:'KFOR-CF-PAD-1 to A000931, finite label preserved',page_errors:failures},null,2));
    console.log('Network site browser checks passed: '+first+' Catalan links, indexed local handoff, primary and transfer navigation.');
  } finally {await browser.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
