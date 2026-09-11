import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync, readdirSync} from 'node:fs';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
test('Salesforce API and source layout',()=>{assert.equal(JSON.parse(read('sfdx-project.json')).sourceApiVersion,'64.0'); assert.match(read('manifest/package.xml'),/<version>64.0<\/version>/);});
test('five exact requirements with limitations',()=>{const r=JSON.parse(read('requirements.json'));assert.equal(r.length,5);assert.ok(r.every(x=>x.acceptance_check));const m=JSON.parse(read('module.json'));assert.equal(m.platform,'Salesforce');assert.ok(m.blockers.length);});
test('Apex sharing and invocable entry point',()=>{const code=read('force-app/main/default/classes/UC23Service.cls');assert.match(code,/public with sharing class/);assert.match(code,/@InvocableMethod/);assert.match(code,/WITH USER_MODE|AccessLevel.USER_MODE|isAccessible/);});
