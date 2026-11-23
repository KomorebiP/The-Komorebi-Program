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
    assert.ok(first>0,'Catalan must have archived formula relations');
    assert.ok((await page.locator('#sn-results').innerText()).includes('Formula identity')||
              (await page.locator('#sn-results').innerText()).includes('Gauge transfer'));
    await page.selectOption('#sn-filter','gauge');
    assert.match(await page.locator('#sn-status').innerText(),/connections found/);
    await page.setViewportSize({width:390,height:844});
    await page.screenshot({path:path.join(output,'network-mobile.png')});
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